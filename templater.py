import inflect
from settings import PRIMARY_KEY

p = inflect.engine()


def table_name(table):
    return table["table"]


def table_name_plural(table):
    return p.plural(table["table"])

def to_plural(text):
    return p.plural(text)

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
        elif (column.type == 'varbinary'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
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
        elif (column.type == 'varbinary'):
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

def template_routes_import(table):
    table_name = table['table']
    result = f"import {table_name}AddEditView from 'src/views/{table_name}/{table_name}AddEditView';\n" + \
    f"import {table_name}ListView from 'src/views/{table_name}/{table_name}ListView';\n"
    return result

def template_routes_class(table):
    table_name = table['table']
    result = f"""{{ path: '{table_name}', element: <{table_name}ListView /> }},
      {{ path: '{table_name}/addedit', element: <{table_name}AddEditView /> }},
      """
    return result

def template_base_fields(table):
    result = ''
    table_name = table['table']
    plural_table_name = to_plural(table_name)

    for column in table["columns"]:
        if (column.name == PRIMARY_KEY): continue
        if (column.is_foreign_key == True and table["main_column"] != column.name):
            res = f"""
                      <Grid item md={{12}} xs={{12}}>
                        <BaseLookup
                          helperText={{store.error{column.name}}}
                          error={{store.error{column.name} != ''}}
                          id='id_f_{table_name}_{column.name}'
                          label={{translate('label:{table_name}AddEditView.{column.name}NavName')}}
                          value={{store.{column.name}}}
                          onChange={{(event) => store.handleChange(event)}}
                          data={{store.{plural_table_name}}}
                          name="{column.name}">
                        </BaseLookup>
                      </Grid>"""

        elif (column.type == 'datetime'):
            res = f"""
                      <Grid item md={{12}} xs={{12}}>
                        <ProtectedDateTimeField
                          helperText={{store.error{column.name}}}
                          error={{store.error{column.name} != ''}}
                          id='id_f_{table_name}_{column.name}'
                          label={{translate('label:{table_name}AddEditView.{column.name}NavName')}}
                          value={{store.{column.name}}}
                          type="date"
                          onChange={{(event) => store.handleChange(event)}}
                          name="{column.name}"/>
                      </Grid>"""

        elif(column.type == 'bit'):
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
                              onChange={{this.handleChange}} size="small"
                              checked={{this.state.{column.name}}}
                            />
                          }}
                        />
                      </Grid>"""

        elif (column.type == 'nvarchar' or column.type == 'varchar' or column.type == 'int'):
            res = f"""
                      <Grid item md={{12}} xs={{12}}>
                        <ProtectedTextField
                          helperText={{store.error{column.name}}}
                          error={{store.error{column.name} != ''}}
                          id='id_f_{table_name}_{column.name}'
                          label={{translate('label:{table_name}AddEditView.{column.name}NavName')}}
                          value={{store.{column.name}}}
                          onChange={{(event) => store.handleChange(event)}}
                          name="{column.name}" 
                        />
                      </Grid>"""

        elif (column.type == 'varbinary'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    return result

def template_mtm_import(table):
    result = ''
    for mtm_table, mtm_column in table["mtms"]:
        result += f"""import {mtm_table}ListView from 'src/views/{mtm_table}/{mtm_table}ListView';
              """
    return result

def template_mtm_title(table):
    result = ''
    index = 0
    for mtm_table, mtm_column in table["mtms"]:
        result += f"""<Tab name={{"{mtm_table}"}} label={{translate("label:{mtm_table}ListView.{mtm_table}")}} {{...a11yProps({index})}} />
              """
        index += 1
    return result

def template_mtm_content(table):
    result = ''
    index = 0
    for mtm_table, mtm_column in table["mtms"]:
        result += f"""<TabPanel value={{this.state.value}} index={{{index}}} dir={{theme.direction}}>
              <Card>
                <CardContent>
                  <{mtm_table}ListView
                    {mtm_column}={{store.id}}
                  />
                </CardContent>
              </Card>
            </TabPanel>
            """
        index += 1
    return result

def template_save_save(table):
    result = ''
    table_name = table['table']
    for column in table["columns"]:
        if(column.type == 'int'):
            res = f"""{column.name}: store.{column.name} - 0,
    """
        elif(column.type == 'datetime'):
            res = f"""str{column.name}: store.{column.name},
    """
        elif(column.type == 'bit'):
            res = f"""{column.name}: !!store.{column.name},
    """
        elif(column.type == 'nvarchar' or column.type == 'varchar'):
            res = f"""{column.name}: !!store.{column.name},
    """
        elif (column.type == 'varbinary'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    return result

def template_store_init(table):
    result = ''
    for column in table["columns"]:
        if(column.name == PRIMARY_KEY): continue
        if(column.type == 'int'):
            res = f"""{column.name} = 0\n\t"""
        elif(column.type == 'nvarchar' or column.type == 'varchar' or column.type or column.type == 'datetime'):
            res = f"""{column.name} = ""\n\t"""
        elif(column.type == 'bit'):
            res = f"""{column.name} = false\n\t"""
        elif (column.type == 'varbinary'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    for column in table["columns"]:
        result += f"""error{column.name} = ""\n\t"""
    return result

def template_store_init_dictionaries(table):
    result = ''
    for for_table in table['foreign_tables']:
        result += f'{to_plural(for_table[0])} = []\n\t'
    return result

def template_store_clear(table):
    result = ''
    for column in table["columns"]:
        if(column.name == PRIMARY_KEY): continue
        if(column.type == 'int'):
            res = f"""this.{column.name} = 0\n\t\t"""
        elif(column.type == 'nvarchar' or column.type == 'varchar' or column.type or column.type == 'datetime'):
            res = f"""this.{column.name} = ""\n\t\t"""
        elif(column.type == 'bit'):
            res = f"""this.{column.name} = false\n\t\t"""
        elif (column.type == 'varbinary'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    for column in table["columns"]:
        result += f"""this.error{column.name} = ""\n\t\t"""
    return result

def template_store_validate(table):
    result = ''
    table_name = table['table']
    for column in table["columns"]:
        result += f"""var event = {{ target: {{ name: '{column.name}', value: this.{column.name}, }} }};
        canSave = validate(event, validated) && canSave;
        """
    return result

def template_store_load_dictionaries(table):
    result = ''
    for for_table in table['foreign_tables']:
        plural_table = to_plural(for_table[0])
        result += f"""
    load{plural_table}() {{
        var url = '/{for_table[0]}/GetAll';
        return userApiClient(url)
            .then(json => this.{plural_table} = json);
    }}
    """
    return result

def template_store_set_data(table):
    result = ''
    for column in table["columns"]:
        result += f"""this.{column.name} = json.{column.name}\n\t\t"""
    return result
    
def template_store_doload_dict(table):
    result = ''
    for for_table in table['foreign_tables']:
        plural_table = to_plural(for_table[0])
        result += f'await this.load{plural_table}();\n\t\t'
    return result
    
def template_valid_fields(table):
    result = ''
    for column in table["columns"]:
        result += f"""
  var {column.name} = '';
  if (event.target.name === '{column.name}') {{
    var {column.name}Errors = [];
    {column.name} = {column.name}Errors.join(', ');
    validated('error{column.name}', {column.name});
  }}
  """
    return result

def template_valid_check_cansave(table):
    result = ''
    for column in table["columns"]:
        result += f"""&& {column.name} === ''\n\t"""
    return result

def template_index_columns(table):
    result = ''
    table_name = table['table']
    for column in table["columns"]:
        if(column.name == 'id' or table["main_column"] == column.name): continue
        label = column.name
        if(column.is_foreign_key == True):
            label = column.name + 'NavName'
        elif(column.type == 'datetime'):
            label = 'str' + column.name
        result += f"""{{
          name: "{column.name}",
          id: "id_g_{table_name}_{column.name}",
          label: translate("label:{table_name}ListView.{column.name}"),
          options: {{
            filter: true,
            customHeadLabelRender: (columnMeta) => (<div name={{"name_g_{table_name}_{column.name}_title"}}>{{columnMeta.label}}</div>),
            customBodyRenderLite: (dataIndex) => {{
              if (dataIndex >= store.data.length) return null;
              return <div name={{"name_g_{table_name}_{column.name}"}}>{{store.data[dataIndex].{label}}}</div>
            }}
          }}
        }},
        """
    return result

def template_index_is_mtm_popup(table):
    if(table['is_mtm']):
        return 'popup'
    else:
        return 'form'

def template_index_load_function(table):
    table_name = table['table']
    if(table['is_mtm']):
        return f'store.load{to_plural(table_name)}(this.props.{table["main_column"]})'
    else:
        return f'store.load{to_plural(table_name)}()'

def template_store_index_load_function(table):
    table_name = table['table']
    if(table['is_mtm']):
        return f"""load{to_plural(table_name)}({table["main_column"]}) {{
        var url = '/{table_name}/GetBy{table["main_column"]}?{table["main_column"]}=' + {table["main_column"]}"""
    else:
        return f"""load{to_plural(table_name)}() {{
        var url = '/{table_name}/GetAll'"""

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
    "template_index_load_function": template_index_load_function,
    "template_store_index_load_function": template_store_index_load_function,
    "template_routes_import": template_routes_import,
    "template_routes_class": template_routes_class,
    "template_mtm_import": template_mtm_import,
}
