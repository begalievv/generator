import inflect
p = inflect.engine()


def table_name(table):
    return table["table"]


def table_name_plural(table):
    return p.plural(table["table"])


def template_dto(table):
    result = ""

    for column in table["columns"]:
        if (column.type == 'nvarchar' or column.type == 'varchar'):
            res = "public string " + column.name + " { get; set; }\n"

        elif (column.type == 'int'):
            if (column.nullable == True):
                if (column.is_foreign_key == True):
                    res = "public int? " + column.name + \
                        " { get; set; }\npublic string " + column.name + \
                        "NavName { get; set; }\n"
                else:
                    res = "public int? " + column.name + " { get; set; }\n"
            else:
                if (column.is_foreign_key == True):
                    res = "public int " + column.name + \
                        " { get; set; }\npublic string " + column.name + \
                        "NavName { get; set; }\n"
                else:
                    res = "public int " + column.name + " { get; set; }\n"

        elif (column.type == 'bit'):
            if (column.nullable == True):
                res = "public bool? " + column.name + " { get; set; }\n"
            else:
                res = "public bool " + column.name + " { get; set; }\n"

        elif (column.type == 'datetime'):
            if (column.nullable == True):
                res = 'public DateTime? ' + column.name + \
                    ' { get; set; }\n' + 'public string str' + \
                    column.name + '\n{\nget\n{\nreturn ' + column.name + '.HasValue ? ' + \
                    column.name + \
                    '.Value.ToString("yyyy-MM-dd HH:mm") : null;\n}\nset\n{\n' + column.name + \
                    ' = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);\n}\n}\n'
            else:
                res = 'public DateTime ' + column.name + \
                    ' { get; set; }\n' + 'public string str' + \
                    column.name + '\n{\nget\n{\nreturn ' + column.name + \
                    '.ToString("yyyy-MM-dd HH:mm");\n}\nset\n{\n' + column.name + \
                    ' = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);\n}\n}\n'
        else:
            raise Exception("Не могу найти тип -" + column.type)
        result += res
    return result


def template_service(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = "public List<" + table_name + "Dto> GetBy" + column.name + \
                '(int ' + column.name + \
                  ')\n{\n_accessService.CheckAccess(_sessionProvider.UserId, _sessionProvider.UserName, ReadMedtodKey);\nreturn _' + \
                table_name + 'Repository.GetBy' + \
                column.name + '(' + column.name + ');\n}\n'
            result += res
    return result


def template_repository(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = 'public List<' + table_name + 'Dto> GetBy' + column.name + \
                '(int ' + column.name + \
                  ')\n{\nreturn GetByFilter(x => x.' + column.name + \
                ' == ' + column.name + ');\n}\n'
            result += res
    return result


def template_repository_include(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = '.Include(x => x.' + column.name + 'Navigation)\n'
            result += res
    return result


def template_irepository(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = "List<" + table_name + "Dto> GetBy" + \
                column.name + "(int " + column.name + ");\n"
            result += res
    return result


def template_iservice(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = 'List<' + table_name + 'Dto> GetBy' + \
                column.name + '(int ' + column.name + ');\n'
            result += res
    return result


def template_toDto(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        res = column.name + ' = _' + table_name + '.' + column.name + ',\n'
        if (column.is_foreign_key == True):
            res += column.name + 'NavName = _' + table_name + \
                '.' + column.name + 'Navigation?.name,\n'
        result += res
    return result


def template_toEntity(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        res = column.name + ' = dto.' + column.name + ',\n'
        result += res
    return result


def template_controller(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = '[HttpGet]\npublic List<' + table_name + \
                'Dto> GetBy' + column.name + \
                '(int ' + column.name + ')\n{\nvar items = _' + \
                  table_name + 'Service.GetBy' + column.name + \
                '(' + column.name + ');\nreturn items;\n}\n'
            result += res
    return result


def template_converter(table):
    result = ""
    for column in table["columns"]:
        res = column.name + ' = model.' + column.name + ',\n'
        result += res
    return result


def template_model(table):
    result = ""
    for column in table["columns"]:
        if (column.type == 'nvarchar' or column.type == 'varchar'):
            res = "public string " + column.name + " { get; set; }\n"
        elif (column.type == 'int'):
            if (column.nullable == True):
                res = "public int? " + column.name + " { get; set; }\n"
            else:
                res = "public int " + column.name + " { get; set; }\n"
        elif (column.type == 'bit'):
            if (column.nullable == True):
                res = "public bool? " + column.name + " { get; set; }\n"
            else:
                res = "public bool " + column.name + " { get; set; }\n"
        elif (column.type == 'datetime'):
            if (column.nullable == True):
                res = 'public DateTime? ' + column.name + \
                    ' { get; set; }\npublic string str' + column.name + \
                    '\n{\nget\n{\nreturn ' + column.name + '.HasValue ? ' + \
                    column.name + \
                    '.Value.ToString("yyyy-MM-dd") : null;\n}\nset\n{\nDateTime date;\nif' + \
                    ' (DateTime.TryParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture, DateTimeStyles.None, out date))\n{\n' + \
                    column.name + '= null;\n}\n}\n}\n'
            else:
                res = 'public DateTime ' + column.name + \
                    ' { get; set; }\npublic string str' + column.name + \
                    '\n{\nget\n{\nreturn ' + column.name + \
                    '.ToString("yyyy-MM-dd");\n}\nset\n{\n' + column.name + \
                    ' = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);\n}\n}\n'
        else:
            raise Exception("Не могу найти тип -" + column.type)
        result += res
    return result


def template_diconverter(table):
    table_name = table['table']
    result = 'services.AddSingleton<IModelConverter<' + table_name + \
        'Model, ' + table_name + 'Dto>, ' + table_name + 'Converter>();\n\t\t\t'
    return result


def template_direpo(table):
    table_name = table['table']
    result = 'services.AddScoped<I' + table_name + \
        'Repository, ' + table_name + 'Repository>();\n\t\t\t'
    return result


def template_diservice(table):
    table_name = table['table']
    result = 'services.AddScoped<I' + table_name + \
        'Service, ' + table_name + 'Service>();\n\t\t\t'
    return result


TEMPLATE_FUNCS = {
    "template_dto": template_dto,
    "table_name_plural": table_name_plural,
    "table_name": table_name,
    "template_service": template_service,
    "template_irepository": template_irepository,
    "template_iservice": template_iservice,
    "template_repository": template_repository,
    "template_toDto": template_toDto,
    "template_toEntity": template_toEntity,
    "template_repository_include": template_repository_include,
    "template_controller": template_controller,
    "template_converter": template_converter,
    "template_model": template_model,
    "template_diconverter": template_diconverter,
    "template_direpo": template_direpo,
    "template_diservice": template_diservice,
}
