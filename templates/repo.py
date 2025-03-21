
from settings import PRIMARY_KEY

def remove_last_comma(s: str) -> str:
    last_comma_index = s.rfind(",")  # Найти индекс последней запятой
    if last_comma_index != -1 and last_comma_index < len(s) - 1:  
        return s[:last_comma_index] + s[last_comma_index + 1:]  # Удалить запятую
    return s

def repo_get_all_fields(table):
    result = ""
    for column in table["columns"]:
        res = f"""""{column.name}"" AS ""{column.name_pascal}"",
                        """
        result += res
    r =  remove_last_comma(result)
    return r


def template_repo_map_fields(table):
    result = ""
    for column in table["columns"]:
        res = f"""
                    {column.name} = domain.{column.name},"""
        result += res
    return result


def template_repo_create_fields(table):
    result = ""
    count = len(table["columns"])
    for column in table["columns"]:
        if (column.name == "id"):
            continue
        res = '""' + column.name + '"", '
        result += res
    return remove_last_comma(result)


def template_repo_create_fields_values(table):
    result = ""
    count = len(table["columns"])
    i = 0
    for column in table["columns"]:
        i += 1
        if (column.name == "id"):
            continue
        res = "@" + column.name_pascal + ", "
        result += res
    return result[:-2]


def template_repo_update_fields(table):
    result = ""
    count = len(table["columns"])
    i = 0
    for column in table["columns"]:
        if (column.name == "created_by" or column.name == "created_at"):
            continue
        i += 1
        res = '""' + column.name + '"" = @' + column.name_pascal + ", "
        result += res
    return result[:-2]


def template_repository(table):
    result = ""
    table_name = table['table']
    fields = repo_get_all_fields(table)
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = f"""
        public async Task<List<{column.table_name_pascal}>> GetBy{column.name_pascal}(int {column.name_pascal})
        {{
            try
            {{
                var sql = @"
                    SELECT 
                        {fields}
                    FROM ""{table_name}"" WHERE ""{column.name}"" = @{column.name_pascal}";
                var models = await _dbConnection.QueryAsync<{column.table_name_pascal}>(sql, new {{ {column.name_pascal} }}, transaction: _dbTransaction);
                return models.ToList();
            }}
            catch (Exception ex)
            {{
                throw new RepositoryException("Failed to get {table_name} by id", ex);
            }}
        }}
        """
            result += res
    return result

def repo_model_converter(table):
    result = ""
    for column in table["columns"]:
        res = f"""{column.name_pascal} = model.{column.name_pascal},
                """
        result += res
    r =  remove_last_comma(result)
    return r
