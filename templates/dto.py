
from settings import PRIMARY_KEY

def dto_fields(table):
    result = ""
    for column in table["columns"]:
        if (column.type == 'character varying' or column.type == 'character' or column.type == 'text' or column.type == 'jsonb'  or column.type == 'json'):
            res = f"""
        [JsonProperty("{column.name_camel}")]
        public string {column.name_pascal} {{ get; set; }}
            """
        elif (column.type == 'integer'):
            res = f"""
        [JsonProperty("{column.name_camel}")]
        public int{"?" if column.nullable else ""} {column.name_pascal} {{ get; set; }}
            """
        elif (column.type == 'double precision' or column.type == 'numeric'):
            res = f"""
        [JsonProperty("{column.name_camel}")]
        public double{"?" if column.nullable else ""} {column.name_pascal} {{ get; set; }}
            """
        elif (column.type == 'boolean'):
            res = f"""
        [JsonProperty("{column.name_camel}")]
        public bool{"?" if column.nullable else ""} {column.name_pascal} {{ get; set; }}
            """
        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""
        [JsonProperty("{column.name_camel}")]
        public DateTime{"?" if column.nullable else ""} {column.name_pascal} {{ get; set; }}
            """
        elif (column.type == 'varbinary' or column.type == 'ARRAY'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    return result

def dto_map_get(table):
    result = ""
    for column in table["columns"]:
        res = f"""{column.name_pascal} = domain.{column.name_pascal},
                """
        result += res
    return result

def dto_map_create_update(table):
    result = ""
    for column in table["columns"]:
        res = f"""{column.name_pascal} = {column.name_pascal},
                """
        result += res
    return result