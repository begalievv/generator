import inflect
from settings import PRIMARY_KEY
from templates.dto import *
from templates.repo import *
import funcs

p = inflect.engine()


def table_name(table):
    return table["table"]
    
def table_name_camel(table):
    return table["table_camel_case_name"]

def table_name_pascal(table):
    return table["table_pascal_case_name"]


def get_main_column(table):
    return table["main_column"]


def table_name_plural(table):
    return funcs.convert_case(p.plural(table["table"]))[1]

def table_name_plural_str(table_name: str):
    return p.plural(table_name)


def to_plural(text):
    return p.plural(text)


def template_dto(table):
    result = ""

    for column in table["columns"]:
        if (column.type == 'character varying' or column.type == 'character' or column.type == 'text' or column.type == 'jsonb'  or column.type == 'json'):
            res = "public string " + column.name + " { get; set; }\n\t\t"

        elif (column.type == 'integer' or column.type == 'double precision' or column.type == 'numeric'):
            if (column.nullable == True):
                if (column.is_foreign_key == True):
                    res = "public int? " + column.name + \
                        " { get; set; }\n\t\tpublic string " + column.name + \
                        "NavName { get; set; }\n\t\t"
                else:
                    res = "public int? " + column.name + " { get; set; }\n\t\t"
            else:
                if (column.is_foreign_key == True):
                    res = "public int " + column.name + \
                        " { get; set; }\n\t\tpublic string " + column.name + \
                        "NavName { get; set; }\n\t\t"
                else:
                    res = "public int " + column.name + " { get; set; }\n\t\t"

        elif (column.type == 'boolean'):
            if (column.nullable == True):
                res = "public bool? " + column.name + " { get; set; }\n\t\t"
            else:
                res = "public bool " + column.name + " { get; set; }\n\t\t"

        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            if (column.nullable == True):
                res = 'public DateTime? ' + column.name + \
                    ' { get; set; }\n\t\t' + 'public string str' + \
                    column.name + '\n\t\t{\n\t\t\tget\n\t\t\t{\n\t\t\t\treturn ' + column.name + '.HasValue ? ' + \
                    column.name + \
                    '.Value.ToString("yyyy-MM-dd HH:mm") : null;\n\t\t\t}\n\t\t\tset\n\t\t\t{\n\t\t\t\t' + column.name + \
                    ' = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);\n\t\t\t}\n\t\t}\n\t\t'
            else:
                res = 'public DateTime ' + column.name + \
                    ' { get; set; }\n\t\t' + 'public string str' + \
                    column.name + '\n\t\t{\n\t\t\tget\n\t\t\t{\n\t\t\t\treturn ' + column.name + \
                    '.ToString("yyyy-MM-dd HH:mm");\n\t\t\t}\n\t\t\tset\n\t\t\t{\n\t\t\t\t' + column.name + \
                    ' = DateTime.ParseExact(value, "yyyy-MM-dd", CultureInfo.InvariantCulture);\n\t\t\t}\n\t\t}\n\t\t'
        elif (column.type == 'varbinary' or column.type == 'ARRAY'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    return result


def template_fields(table):
    result = ""

    for column in table["columns"]:
        if(column.name == "updated_at" or column.name == "updated_by" or column.name == "created_at" or column.name == "created_by"): continue

        if (column.type == 'character varying' or column.type == 'character' or column.type == 'text' or column.type == 'jsonb'  or column.type == 'json'):
            res = "public string " + column.name_pascal + " { get; set; }\n\t\t"

        elif (column.type == 'integer' or column.type == 'numeric'):
            if (column.nullable == True):
                res = "public int? " + column.name_pascal + " { get; set; }\n\t\t"
            else:
                res = "public int " + column.name_pascal + " { get; set; }\n\t\t"

        elif (column.type == 'double precision'):
            if (column.nullable == True):
                res = "public double? " + column.name_pascal + " { get; set; }\n\t\t"
            else:
                res = "public double " + column.name_pascal + " { get; set; }\n\t\t"

        elif (column.type == 'boolean'):
            if (column.nullable == True):
                res = "public bool? " + column.name_pascal + " { get; set; }\n\t\t"
            else:
                res = "public bool " + column.name_pascal + " { get; set; }\n\t\t"

        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            if (column.nullable == True):
                res = "public DateTime? " + \
                    column.name_pascal + " { get; set; }\n\t\t"
            else:
                res = "public DateTime " + column.name_pascal + " { get; set; }\n\t\t"
        elif (column.type == 'varbinary' or column.type == 'ARRAY'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    return result


def template_request_converter_without_id(table):
    result = ""
    for column in table["columns"]:
        if (column.name == 'id'):
            continue

        res = f"""
                {column.name} = requestDto.{column.name},"""
        result += res
    return result




def template_service(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = f"""
        public List<{table_name}Dto> GetBy{column.name}(int {column.name})
        {{
            _accessService.CheckAccess(_sessionProvider.UserId, _sessionProvider.UserName, ReadMedtodKey);
            return _{table_name}Repository.GetBy{column.name}({column.name});
        }}
        """
            # res = "public List<" + table_name + "Dto> GetBy" + column.name + \
            #     '(int ' + column.name + \
            #       ')\n{\n_accessService.CheckAccess(_sessionProvider.UserId, _sessionProvider.UserName, ReadMedtodKey);\nreturn _' + \
            #     table_name + 'Repository.GetBy' + \
            #     column.name + '(' + column.name + ');\n}\n'
            result += res
    return result



def template_repository_include(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = '.Include(x => x.' + column.name + 'Navigation)\n\t\t\t'
            result += res
    return result


def template_irepository(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = f"""
        Task<List<{column.table_name_pascal}>> GetBy{column.name_pascal}(int {column.name_pascal});"""
            result += res
    return result


def template_iservice(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = 'List<' + table_name + 'Dto> GetBy' + \
                column.name + '(int ' + column.name + ');\n\t\t'
            result += res
    return result


def template_toDto(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        res = column.name + ' = _' + table_name + '.' + column.name + ',\n\t\t\t\t'
        if (column.is_foreign_key == True):
            res += column.name + 'NavName = _' + table_name + \
                '.' + column.name + 'Navigation?.name,\n\t\t\t\t'
        result += res
    return result


def template_toEntity(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        res = column.name + ' = dto.' + column.name + ',\n\t\t\t\t'
        result += res
    return result


def template_controller(table):
    result = ""
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = f"""
        [HttpGet]
        [Route("GetBy{column.name_pascal}")]
        public async Task<IActionResult> GetBy{column.name_pascal}(int {column.name_pascal})
        {{
            var response = await _{column.table_name_pascal}UseCase.GetBy{column.name_pascal}({column.name_pascal});
            return Ok(response);
        }}
        """
            result += res
    return result


def template_usecase(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = f"""
        public Task<List<{column.table_name_pascal}>> GetBy{column.name_pascal}(int {column.name_pascal})
        {{
            return _unitOfWork.{column.table_name_pascal}Repository.GetBy{column.name_pascal}({column.name_pascal});
        }}
        """
            result += res
    return result


def template_converter(table):
    result = ""
    for column in table["columns"]:
        res = column.name + ' = model.' + column.name + ',\n\t\t\t\t'
        result += res
    return result


def template_model(table):
    result = ""
    for column in table["columns"]:
        if (column.type == 'character varying' or column.type == 'character' or column.type == 'text' or column.type == 'jsonb'  or column.type == 'json'):
            res = "public string " + column.name + " { get; set; }\n\t\t"
        elif (column.type == 'integer' or column.type == 'double precision' or column.type == 'numeric'):
            if (column.nullable == True):
                res = "public int? " + column.name + " { get; set; }\n\t\t"
            else:
                res = "public int " + column.name + " { get; set; }\n\t\t"
        elif (column.type == 'boolean'):
            if (column.nullable == True):
                res = "public bool? " + column.name + " { get; set; }\n\t\t"
            else:
                res = "public bool " + column.name + " { get; set; }\n\t\t"
        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            if (column.nullable == True):
                res = f"""public DateTime? {column.name} {{ get; set; }}
        public string str{column.name}
        {{
            get
            {{
                return {column.name}.HasValue ? {column.name}.Value.ToString("yyyy-MM-dd HH:mm") : null;
            }}
            set
            {{
                DateTime date;
                if (DateTime.TryParseExact(value, "yyyy-MM-dd HH:mm", CultureInfo.InvariantCulture, DateTimeStyles.None, out date))
                {{
                    {column.name} = date;
                }}
                else
                {{
                    {column.name} = null;
                }}
            }}
        }}
        """
            else:
                res = f"""public DateTime {column.name} {{ get; set; }}
        public string str{column.name}
        {{
            get
            {{
                return {column.name}.ToString("yyyy-MM-dd HH:mm");
            }}
            set
            {{
                {column.name} = DateTime.ParseExact(value, "yyyy-MM-dd HH:mm", CultureInfo.InvariantCulture);
            }}
        }}
        """
        elif (column.type == 'varbinary' or column.type == 'ARRAY'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
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


def template_program_repo(table):
    table_name = table['table']
    result = f"""
            builder.Services.AddScoped<I{table["table_pascal_case_name"]}Repository, {table["table_pascal_case_name"]}Repository>();"""
    return result


def template_program_usecase(table):
    table_name = table['table']
    result = f"""
            builder.Services.AddScoped<I{table["table_pascal_case_name"]}UseCase, {table["table_pascal_case_name"]}UseCases>();"""
    return result


def template_program_iunitofwork(table):
    table_name = table['table']
    result = f"""
        private I{table["table_pascal_case_name"]}Repository? _{table["table_pascal_case_name"]}Repository;"""
    return result


def template_program_iunitofwork_dispose(table):
    table_name = table['table']
    result = f"""
        I{table["table_pascal_case_name"]}Repository {table["table_pascal_case_name"]}Repository {{ get; }}"""
    return result


def template_program_iunitofwork_public(table):
    table_name = table['table']
    result = f"""
        public I{table["table_pascal_case_name"]}Repository {table["table_pascal_case_name"]}Repository
        {{
            get
            {{
                if (_{table["table_pascal_case_name"]}Repository == null)
                {{
                    _{table["table_pascal_case_name"]}Repository = new {table["table_pascal_case_name"]}Repository(_dbConnection);
                    _{table["table_pascal_case_name"]}Repository.SetTransaction(_dbTransaction);
                }}
                return _{table["table_pascal_case_name"]}Repository;
            }}
        }}"""
    return result


def template_routes_import(table):
    table_name = table['table_pascal_case_name']
    result = f"const {table_name}ListView = lazy(() => import('features/{table_name}/{table_name}ListView'));\n" + \
        f"const {table_name}AddEditView = lazy(() => import('features/{table_name}/{table_name}AddEditView'));\n"
    return result


def template_locale(table):
    col = ""
    i = 0
    table_name = table['table_pascal_case_name']
    for column in table["columns"]:
        i += 1
        if (column.name == "created_at" or column.name == "updated_at" or column.name == "created_by" or column.name == "updated_by"):
            continue
        if (column.name == PRIMARY_KEY):
            continue
        if (column.is_foreign_key == True):
            col += f'"{column.name_camel}": "{column.name_camel}",\n\t\t'
        else:
            col += f'"{column.name_camel}": "{column.name_camel}",\n\t\t'

    col = remove_last_comma(col)

    res = f""""{table_name}AddEditView": {{
    "entityTitle": "{table_name}",
    {col}
  }},
  "{table_name}ListView": {{
    "{table_name}": "{table_name}",
    "entityTitle": "{table_name}",
    {col}
  }},
  """
    return res


def template_routes_class(table):
    table_name = table['table_pascal_case_name']
    result = f"""{{ path: '{table_name}', element: (<Suspense fallback={{<LoadingFallback />}}><{table_name}ListView /></Suspense>) }},
              {{ path: '{table_name}/addedit', element: (<Suspense fallback={{<LoadingFallback />}}><{table_name}AddEditView /></Suspense>) }},
              """
    return result


def template_base_fields(table):
    result = ''
    table_name = table['table']

    for column in table["columns"]:
        if (column.name == PRIMARY_KEY or table["main_column"] == column.name):
            continue
        if (column.name == "created_at" or column.name == "updated_at" or column.name == "created_by" or column.name == "updated_by"):
            continue
        if (column.is_foreign_key == True):
            plural_table_name = funcs.convert_case(to_plural(column.foreign_table))
            res = f"""
                  <Grid item md={{12}} xs={{12}}>
                    <LookUp
                      value={{store.{column.name_camel}}}
                      onChange={{(event) => store.handleChange(event)}}
                      name="{column.name_camel}"
                      data={{store.{plural_table_name[0]}}}
                      id='id_f_{column.table_name_pascal}_{column.name_camel}'
                      label={{translate('label:{column.table_name_pascal}AddEditView.{column.name_camel}')}}
                      helperText={{store.errors.{column.name_camel}}}
                      error={{!!store.errors.{column.name_camel}}}
                    />
                  </Grid>"""

        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""
                  <Grid item md={{12}} xs={{12}}>
                    <DateTimeField
                      value={{store.{column.name_camel}}}
                      onChange={{(event) => store.handleChange(event)}}
                      name="{column.name_camel}"
                      id='id_f_{column.table_name_pascal}_{column.name_camel}'
                      label={{translate('label:{column.table_name_pascal}AddEditView.{column.name_camel}')}}
                      helperText={{store.errors.{column.name_camel}}}
                      error={{!!store.errors.{column.name_camel}}}
                    />
                  </Grid>"""

        elif (column.type == 'boolean'):
            res = f"""
                  <Grid item md={{12}} xs={{12}}>
                    <CustomCheckbox
                      value={{store.{column.name_camel}}}
                      onChange={{(event) => store.handleChange(event)}}
                      name="{column.name_camel}"
                      label={{translate('label:{column.table_name_pascal}AddEditView.{column.name_camel}')}}
                      id='id_f_{column.table_name_pascal}_{column.name_camel}'
                    />
                  </Grid>"""

        elif (column.type == 'character varying' or column.type == 'character' or column.type == 'integer' or column.type == 'double precision' or column.type == 'numeric' or column.type == 'text' or column.type == 'jsonb'  or column.type == 'json'):
            res = f"""
                  <Grid item md={{12}} xs={{12}}>
                    <CustomTextField
                      value={{store.{column.name_camel}}}
                      onChange={{(event) => store.handleChange(event)}}
                      name="{column.name_camel}"
                      data-testid="id_f_{column.table_name_pascal}_{column.name_camel}"
                      id='id_f_{column.table_name_pascal}_{column.name_camel}'
                      label={{translate('label:{column.table_name_pascal}AddEditView.{column.name_camel}')}}
                      helperText={{store.errors.{column.name_camel}}}
                      error={{!!store.errors.{column.name_camel}}}
                    />
                  </Grid>"""

        elif (column.type == 'varbinary' or column.type == 'ARRAY'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    return result


def template_mtm_import(table):
    result = ''
    for mtm_table, mtm_column in table["mtms"]:
        pascal_table = funcs.convert_case(mtm_table)[1]
        result += f"""import {pascal_table}ListView from 'features/{pascal_table}/{pascal_table}ListView';
              """
    return result


def template_mtm_title(table):
    result = ''
    index = 0
    for mtm_table, mtm_column in table["mtms"]:
        pascal_table = funcs.convert_case(mtm_table)[1]
        result += f"""<Tab data-testid={{"{pascal_table}TabTitle"}} label={{translate("label:{pascal_table}ListView.entityTitle")}} {{...a11yProps({index})}} />
              """
        index += 1
    return result


def template_mtm_content(table):
    result = ''
    index = 0
    for mtm_table, mtm_column in table["mtms"]:
        pascal_table = funcs.convert_case(mtm_table)[1]
        result += f"""
      <CustomTabPanel value={{value}} index={{{index}}}>
        <{pascal_table}ListView mainId={{store.id}} />
      </CustomTabPanel>
            """
        index += 1
    return result


def template_save_save(table):
    result = ''
    table_name = table['table']
    for column in table["columns"]:
        if (table["main_column"] == column.name):
            res = f"""{table["main_column"]}: props.{table["main_column"]} - 0,
    """
        elif (column.type == 'integer' or column.type == 'double precision' or column.type == 'numeric'):
            if (column.nullable == True):
                res = f"""{column.name}: store.{column.name} - 0 == 0 ? null : store.{column.name} - 0,
    """
            else:
                res = f"""{column.name}: store.{column.name} - 0,
    """
        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""str{column.name}: store.{column.name},
    """
        elif (column.type == 'boolean'):
            res = f"""{column.name}: !!store.{column.name},
    """
        elif (column.type == 'character varying' or column.type == 'character' or column.type == 'text' or column.type == 'jsonb'  or column.type == 'json'):
            res = f"""{column.name}: store.{column.name},
    """
        elif (column.type == 'varbinary' or column.type == 'ARRAY'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    return result


def template_store_init(table):
    result = ''
    for column in table["columns"]:
        if (column.name == "created_at" or column.name == "updated_at" or column.name == "created_by" or column.name == "updated_by"):
            continue
        if (column.type == 'integer' or column.type == 'double precision' or column.type == 'numeric'):
            res = f"""@observable {column.name_camel}: number = 0\n\t"""
        elif (column.type == 'character varying' or column.type == 'character' or column.type == 'text' or column.type == 'jsonb'  or column.type == 'json'):
            res = f"""@observable {column.name_camel}: string = ""\n\t"""
        elif (column.type == 'boolean'):
            res = f"""@observable {column.name_camel}: boolean = false\n\t"""
        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""@observable {column.name_camel}: Dayjs = null\n\t"""
        elif (column.type == 'varbinary' or column.type == 'ARRAY'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    # for column in table["columns"]:
    #     result += f"""error{column.name} = ""\n\t"""
    return result


def template_store_init_dictionaries(table):
    result = ''
    for for_table in table['foreign_tables']:
        plural_table = funcs.convert_case(to_plural(for_table[0]))
        result += f'@observable {plural_table[0]} = []\n\t'
    return result


def template_store_clear(table):
    result = ''
    for column in table["columns"]:
        if (column.name == "created_at" or column.name == "updated_at" or column.name == "created_by" or column.name == "updated_by"):
            continue
        if (column.type == 'integer' or column.type == 'double precision' or column.type == 'numeric'):
            res = f"""this.{column.name_camel} = 0\n\t\t"""
        elif (column.type == 'character varying' or column.type == 'character' or column.type == 'text' or column.type == 'jsonb'  or column.type == 'json'):
            res = f"""this.{column.name_camel} = ""\n\t\t"""
        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""this.{column.name_camel} = null\n\t\t"""
        elif (column.type == 'boolean'):
            res = f"""this.{column.name_camel} = false\n\t\t"""
        elif (column.type == 'varbinary' or column.type == 'ARRAY'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    # for column in table["columns"]:
    #     result += f"""this.error{column.name} = ""\n\t\t"""
    return result


def template_store_validate(table):
    result = ''
    table_name = table['table']
    for column in table["columns"]:
        if (column.name == "created_at" or column.name == "updated_at" or column.name == "created_by" or column.name == "updated_by"):
            continue
        result += f"""
      {column.name_camel}: this.{column.name_camel}{" - 0" if column.type == 'integer' else ""},"""
    return result


def template_store_load_dictionaries(table):
    result = ''
    for for_table in table['foreign_tables']:
        plural_table = funcs.convert_case(to_plural(for_table[0]))
        result += f"""
  load{plural_table[1]} = async () => {{
    try {{
      MainStore.changeLoader(true);
      const response = await get{plural_table[1]}();
      if ((response.status === 201 || response.status === 200) && response?.data !== null) {{
        this.{plural_table[0]} = response.data
      }} else {{
        throw new Error();
      }}
    }} catch (err) {{
      MainStore.setSnackbar(i18n.t("message:somethingWentWrong"), "error");
    }} finally {{
      MainStore.changeLoader(false);
    }}
  }};
    """
    return result


def template_store_set_data(table):
    result = ''
    for column in table["columns"]:
        if (column.name == "created_at" or column.name == "updated_at" or column.name == "created_by" or column.name == "updated_by"):
            continue
        if (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            result += f"""
          this.{column.name_camel} = dayjs(data.{column.name_camel});"""
        else:
            result += f"""
          this.{column.name_camel} = data.{column.name_camel};"""
    return result


def template_store_doload_dict(table):
    result = ''
    for for_table in table['foreign_tables']:
        # plural_table = to_plural(for_table[0])
        plural_table_name = funcs.convert_case(to_plural(for_table[0]))
        result += f'await this.load{plural_table_name[1]}();\n\t\t'
    return result


def template_valid_fields(table):
    result = ''
    for column in table["columns"]:
        if (column.name == "created_at" or column.name == "updated_at" or column.name == "created_by" or column.name == "updated_by"):
            continue
        valids = ""
        if (column.name == PRIMARY_KEY):
            continue
        if (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""
  {column.name_camel}: yup
    .date()
    .nullable()
    .required("Required field")
    .typeError("Please provide a valid date"),"""

        elif (column.type == "integer" or column.type == "double" or column.type == "double precision"):
            res = f"""
  {column.name_camel}: yup.number().notOneOf([0], "Required field").required("Required field"),"""
        elif (column.type == "boolean"):
            res = f"""
  {column.name_camel}: yup.boolean().nullable().default(false),"""
        else:
            res = f"""
  {column.name_camel}: yup.string(),"""

        # if(column.nullable == False):
        #     if(column.is_foreign_key):
        #         if(table["main_column"] != column.name):
        #             valids += f"""CheckEmptyLookup(event.target.value, {column.name}Errors)\n\t"""
        #     else:
        #         valids += f"""CheckEmptyTextField(event.target.value, {column.name}Errors)\n\t"""

        result += res
    return result


def template_valid_check_cansave(table):
    result = ''
    for column in table["columns"]:
        if (column.name == PRIMARY_KEY):
            continue
        result += f"""&& {column.name} === ''\n\t"""
    return result


def template_index_columns(table):
    result = ''
    table_name = table['table']
    for column in table["columns"]:
        if (column.name == 'id' or table["main_column"] == column.name):
            continue
        if (column.name == "created_at" or column.name == "updated_at" or column.name == "created_by" or column.name == "updated_by"):
            continue
        label = column.name
        if column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone':
            result += f"""
    {{
      field: '{column.name_camel}',
      headerName: translate("label:{column.table_name_pascal}ListView.{column.name_camel}"),
      flex: 1,
      renderCell: (param) => (<div data-testid="table_{column.table_name_pascal}_column_{column.name_camel}"> {{param.row.{column.name_camel} ? dayjs(param.row.{column.name_camel})?.format("DD.MM.YYYY HH:mm") : ""}} </div>),
      renderHeader: (param) => (<div data-testid="table_{column.table_name_pascal}_header_{column.name_camel}">{{param.colDef.headerName}}</div>)
    }},"""
        else:
            result += f"""
    {{
      field: '{column.name_camel}',
      headerName: translate("label:{column.table_name_pascal}ListView.{column.name_camel}"),
      flex: 1,
      renderCell: (param) => (<div data-testid="table_{column.table_name_pascal}_column_{column.name_camel}"> {{param.row.{column.name_camel}}} </div>),
      renderHeader: (param) => (<div data-testid="table_{column.table_name_pascal}_header_{column.name_camel}">{{param.colDef.headerName}}</div>)
    }},"""

    return result


def template_index_is_mtm_popup(table):
    if (table['is_mtm']):
        return 'popup'
    else:
        return 'form'


def template_index_is_mtm_column_name(table):
    if (table['is_mtm']):
        return f"""
              {table["main_column"]}={{this.props.{table["main_column"]}}}"""
    else:
        return ""


def template_mtm_has_mtm(table):
    if (len(table['mtms']) != 0):
        return f"""{{/* start MTM */}}
            {{store.id > 0 && <Grid item xs={{12}} spacing={{0}}><MtmTabs /></Grid>}}
            {{/* end MTM */}}"""
    else:
        return ""


def template_mtm_has_mtm_grid(table):
    if (len(table['mtms']) != 0):
        return f"""store.id == 0 ? 6 : 12"""
    else:
        return "6"


def template_index_load_function(table):
    table_name = table['table']
    if (table['is_mtm']):
        return f"""
  useEffect(() => {{
    if (store.idMain !== props.idMain) {{
      store.idMain = props.idMain
    }}
    store.load{to_plural(table_name)}()
    return () => store.clearStore()
  }}, [props.idMain])"""
    else:
        return f"""
  useEffect(() => {{
    store.load{to_plural(table_name)}()
    return () => {{
      store.clearStore()
    }}
  }}, [])"""


def template_index_list_props(table):
    if (table['is_mtm']):
        return f"""
  idMain: number;"""
    else:
        return ""


def template_store_index_load_function(table):
    table_name = table['table']
    if (table['is_mtm']):
        return f"""const response = await get{to_plural(table_name)}By{table["main_column"]}(this.idMain);"""
    else:
        return f"""const response = await get{to_plural(table_name)}();"""


def template_store_load_function(table):
    table_name = table['table']
    if (table['is_mtm']):
        return f'store.load{to_plural(table_name)}(this.props.idMain)'
    else:
        return f'store.load{to_plural(table_name)}()'


def template_fast_input_load_dicts(table):
    table_name = table['table']
    result = ""
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            result += f"""storeAddEdit.load{to_plural(column.foreign_table)}()
            """
    return result


def template_fast_input_change_main_id(table):
    table_name = table['table']
    if (table['is_mtm']):
        return f"""storeAddEdit.{table["main_column"]} = this.props.idMain - 0"""
    else:
        return ""


def template_fast_input_columns(table):
    table_name = table['table']
    result = ""
    for column in table["columns"]:
        if (column.name == 'id'):
            continue
        if (column.is_foreign_key == True):
            result += f"""{{
                    field: '{column.name}NavName',
                    width: null, //or number from 1 to 12
                    headerName: translate("label:{table_name}ListView.{column.name}"),
                }},
                """
        else:
            result += f"""{{
                    field: '{column.name}',
                    width: null, //or number from 1 to 12
                    headerName: translate("label:{table_name}ListView.{column.name}"),
                }},
                """
    return result


def template_constant_fields(table):
    result = ''
    for column in table["columns"]:
        if(column.name == "updated_at" or column.name == "updated_by" or column.name == "created_at" or column.name == "created_by"): continue
        if (column.type == 'integer' or column.type == 'double precision' or column.type == 'numeric'):
            result += f"""
  {column.name_camel}: number;"""
        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            result += f"""
  {column.name_camel}: Dayjs;"""
        elif (column.type == 'boolean'):
            result += f"""
  {column.name_camel}: boolean;"""
        else:
            result += f"""
  {column.name_camel}: string;"""
    return result


def template_export_mtm_api(table):
    if (table["is_mtm"]):
        main_column = funcs.convert_case(table["main_column"])[1]
        main_column_camel = funcs.convert_case(table["main_column"])[0]
        return f"""
export const get{table_name_plural(table)}By{main_column} = ({main_column_camel}: number): Promise<any> => {{
  return http.get(`/api/v1/{table['table_pascal_case_name']}/GetBy{main_column}?{main_column}=${{{main_column_camel}}}`);
}};"""
    else:
        return ""


def template_fastinput_fields(table):
    result = ''
    table_name = table['table']

    for column in table["columns"]:
        if (column.name == PRIMARY_KEY or table["main_column"] == column.name):
            continue
        if (column.is_foreign_key == True):
            plural_table_name = to_plural(column.foreign_table)
            res = f"""
                                <Grid item md={{6}} xs={{6}}>
                                    <BaseLookup
                                        helperText={{storeAddEdit.error{column.name}}}
                                        error={{storeAddEdit.error{column.name} != ''}}
                                        id='id_f_{table_name}_{column.name}'
                                        label={{translate('label:{table_name}AddEditView.{column.name}NavName')}}
                                        value={{storeAddEdit.{column.name}}}
                                        onChange={{(event) => storeAddEdit.handleChange(event)}}
                                        data={{storeAddEdit.{plural_table_name}}}
                                        name="{column.name}">
                                    </BaseLookup>
                                </Grid>"""

        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""
                                <Grid item md={{6}} xs={{6}}>
                                    <ProtectedDateTimeField
                                        helperText={{storeAddEdit.error{column.name}}}
                                        error={{storeAddEdit.error{column.name} != ''}}
                                        id='id_f_{table_name}_{column.name}'
                                        label={{translate('label:{table_name}AddEditView.{column.name}')}}
                                        value={{storeAddEdit.{column.name}}}
                                        type="date"
                                        onChange={{(event) => storeAddEdit.handleChange(event)}}
                                        name="{column.name}"
                                    />
                                </Grid>"""

        elif (column.type == 'boolean'):
            res = f"""
                                <Grid item md={{12}} xs={{12}}>
                                    <FormControlLabel
                                        label={{<span id="id_f_{table_name}_{column.name}-label">
                                            {{translate('label:{table_name}AddEditView.{column.name}')}}
                                        </span>}}
                                        control={{
                                            <ProtectedCheckbox
                                                name="{column.name}"
                                                id="id_f_{table_name}_{column.name}"
                                                onChange={{(event) => store.handleChange(event)}} size="small"
                                                value={{store.{column.name}}}
                                            />
                                        }}
                                    />
                                </Grid>"""

        elif (column.type == 'character varying' or column.type == 'character' or column.type == 'text' or column.type == 'jsonb'  or column.type == 'json' or column.type == 'integer' or column.type == 'double precision' or column.type == 'numeric'):
            res = f"""
                                <Grid item md={{6}} xs={{6}}>
                                    <ProtectedTextField
                                        helperText={{storeAddEdit.error{column.name}}}
                                        error={{storeAddEdit.error{column.name} != ''}}
                                        id='id_f_{table_name}_{column.name}'
                                        label={{translate('label:{table_name}AddEditView.{column.name}')}}
                                        value={{storeAddEdit.{column.name}}}
                                        onChange={{(event) => storeAddEdit.handleChange(event)}}
                                        name="{column.name}" 
                                    />
                                </Grid>"""

        elif (column.type == 'varbinary' or column.type == 'ARRAY'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    return result


def table_get_list_import(table):
    result = ''
    plural_name = table_name_plural_str(table['table_pascal_case_name'])
    column_names = funcs.convert_case(table["main_column"])
    if (table["is_mtm"]):
        result = f'import {{ get{plural_name}By{column_names[1]} }} from "api/{table["table_pascal_case_name"]}";'
    else:
        result = f'import {{ get{plural_name} }} from "api/{table["table_pascal_case_name"]}";'
    return result

def template_index_set_main(table):
    result = ''
    if (table["is_mtm"]):
        result = f"""useEffect(() => {{
    store.setMainId(props.mainId)
  }}, [props.mainId]);
  """
    return result

def template_index_props_idmain(table):
    result = ''
    if (table["is_mtm"]):
        result = f"""mainId: number;
"""
    return result

def template_index_store_set_idmain(table):
    result = ''
    if (table["is_mtm"]):
        result = f"""setMainId = async (id: number) => {{
    if (id !== this.mainId) {{
      this.mainId = id;
      await this.load{table["table_pascal_case_name"]}s()
    }}
  }}
"""
    return result

def load_list_func_name(table):
    result = ''
    plural_name = table_name_plural_str(table['table_pascal_case_name'])
    column_names = funcs.convert_case(table["main_column"])
    if (table["is_mtm"]):
        result = f'() => get{plural_name}By{column_names[1]}(this.mainId)'
    else:
        result = "get" + table_name_plural(table)
        # result = f'import {{ get{plural_name} }} from "api/{table["table_pascal_case_name"]}";'

    return result

def template_index_is_popup(table):
    result = ''
    if (table["is_mtm"]):
        result = "popup"
    else:
        result = "form"
    return result

def load_list_func_is_mtm(table):
    result = ''
    if (table["is_mtm"]):
        result = """if (this.mainId === 0) return;
    """
    return result


def template_store_import_dictionaries(table):
    result = ''
    for for_table in table['foreign_tables']:
        plural_table = funcs.convert_case(to_plural(for_table[0]))[1]
        result += f"""
import {{ get{plural_table} }} from "api/{funcs.convert_case(for_table[0])[1]}";
    """
    return result


TEMPLATE_FUNCS = {
    "template_dto": template_dto,
    "template_fields": template_fields,
    "dto_fields": dto_fields,
    "dto_map_get": dto_map_get,
    "dto_map_create_update": dto_map_create_update,
    "repo_get_all_fields": repo_get_all_fields,
    "template_request_converter_without_id": template_request_converter_without_id,
    "template_repo_map_fields": template_repo_map_fields,
    "template_repo_create_fields": template_repo_create_fields,
    "template_repo_create_fields_values": template_repo_create_fields_values,
    "template_repo_update_fields": template_repo_update_fields,
    "template_program_usecase": template_program_usecase,
    "template_program_repo": template_program_repo,
    "template_program_iunitofwork": template_program_iunitofwork,
    "template_program_iunitofwork_public": template_program_iunitofwork_public,
    "template_program_iunitofwork_dispose": template_program_iunitofwork_dispose,

    "template_usecase": template_usecase,
    "table_name_plural": table_name_plural,
    "table_name": table_name,
    "table_name_camel": table_name_camel,
    "table_name_pascal": table_name_pascal,
    "get_main_column": get_main_column,
    "table_get_list_import": table_get_list_import,
    "template_index_store_set_idmain": template_index_store_set_idmain,
    "template_index_props_idmain": template_index_props_idmain,
    "template_index_set_main": template_index_set_main,
    "load_list_func_name": load_list_func_name,
    "template_index_is_popup": template_index_is_popup,
    "load_list_func_is_mtm": load_list_func_is_mtm,
    "template_store_import_dictionaries": template_store_import_dictionaries,
    "template_export_mtm_api": template_export_mtm_api,
    "template_constant_fields": template_constant_fields,
    "template_index_list_props": template_index_list_props,
    "template_service": template_service,
    "template_irepository": template_irepository,
    "template_iservice": template_iservice,
    "template_repository": template_repository,
    "repo_model_converter": repo_model_converter,
    "template_toDto": template_toDto,
    "template_toEntity": template_toEntity,
    "template_repository_include": template_repository_include,
    "template_controller": template_controller,
    "template_converter": template_converter,
    "template_model": template_model,
    "template_diconverter": template_diconverter,
    "template_direpo": template_direpo,
    "template_diservice": template_diservice,
    "template_base_fields": template_base_fields,
    "template_mtm_title": template_mtm_title,
    "template_mtm_content": template_mtm_content,
    "template_save_save": template_save_save,
    "template_store_init": template_store_init,
    "template_store_init_dictionaries": template_store_init_dictionaries,
    "template_store_clear": template_store_clear,
    "template_store_validate": template_store_validate,
    "template_store_load_dictionaries": template_store_load_dictionaries,
    "template_store_set_data": template_store_set_data,
    "template_store_doload_dict": template_store_doload_dict,
    "template_valid_fields": template_valid_fields,
    "template_valid_check_cansave": template_valid_check_cansave,
    "template_index_columns": template_index_columns,
    "template_index_is_mtm_popup": template_index_is_mtm_popup,
    "template_index_is_mtm_column_name": template_index_is_mtm_column_name,
    "template_index_load_function": template_index_load_function,
    "template_store_index_load_function": template_store_index_load_function,
    "template_routes_import": template_routes_import,
    "template_routes_class": template_routes_class,
    "template_mtm_import": template_mtm_import,
    "template_locale": template_locale,
    "template_mtm_has_mtm": template_mtm_has_mtm,
    "template_mtm_has_mtm_grid": template_mtm_has_mtm_grid,
    "template_fast_input_load_dicts": template_fast_input_load_dicts,
    "template_fast_input_columns": template_fast_input_columns,
    "template_store_load_function": template_store_load_function,
    "template_fastinput_fields": template_fastinput_fields,
    "template_fast_input_change_main_id": template_fast_input_change_main_id
}
