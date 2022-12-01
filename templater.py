

def table_name(table):
    return table["table"]

def template_1(table):
    "public string surName { get; set; }"
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
                res = "public DateTime? " + column.name + " { get; set; }\n" + "public string str" + column.name + \
                    "\n{\nget\n{\nreturn " + column.name + ".HasValue ? " + \
                    column.name + '.Value.ToString("yyyy-MM-dd") : null;\n}\nset\n{\n ' + column.name + \
                    ' = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);\n' + '}\n}\n'
            else:
                res = "public DateTime " + column.name + " { get; set; }\n" + "public DateTime? " + column.name + \
                    " { get; set; }\nget\n{\nreturn " + column.name + \
                    '.ToString("yyyy-MM-dd HH:mm");\n}\nset\n{\n' + column.name + \
                    ' = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);\n}\n}\n'
        else:
            raise Exception("Не могу найти тип -" + column.type)
        result += res
    return result

TEMPLATE_FUNCS = {"template_1": template_1, "table_name": table_name}