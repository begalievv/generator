import inflect
from settings import PRIMARY_KEY

p = inflect.engine()


def table_name(table):
    return table["table"]

def get_main_column(table):
    return table["main_column"]

def table_name_plural(table):
    return p.plural(table["table"])

def to_plural(text):
    return p.plural(text)

def template_dto(table):
    result = ""

    for column in table["columns"]:
        if (column.type == 'character varying' or column.type == 'character'):
            res = "public string " + column.name + " { get; set; }\n\t\t"

        elif (column.type == 'integer' or column.type == 'double precision'):
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
            res = '.Include(x => x.' + column.name + 'Navigation)\n\t\t\t'
            result += res
    return result


def template_irepository(table):
    result = ""
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = "List<" + table_name + "Dto> GetBy" + \
                column.name + "(int " + column.name + ");\n\t\t"
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
    table_name = table['table']
    for column in table["columns"]:
        if (column.is_foreign_key == True):
            res = f"""
        [HttpGet]
        [Route("GetBy{column.name}")]
        public List<{table_name}Dto> GetBy{column.name}(int {column.name})
        {{
            var items = _{table_name}Service.GetBy{column.name}({column.name});
            return items;
        }}
        """
            # res = '[HttpGet]\npublic List<' + table_name + \
            #     'Dto> GetBy' + column.name + \
            #     '(int ' + column.name + ')\n{\nvar items = _' + \
            #       table_name + 'Service.GetBy' + column.name + \
            #     '(' + column.name + ');\nreturn items;\n}\n'
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
        if (column.type == 'character varying' or column.type == 'character'):
            res = "public string " + column.name + " { get; set; }\n\t\t"
        elif (column.type == 'integer' or column.type == 'double precision'):
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
    result = f"import {table_name}AddEditView from 'features/{table_name}/{table_name}AddEditView';\n" + \
    f"import {table_name}ListView from 'features/{table_name}/{table_name}ListView';\n"
    return result

def template_locale(table):
    col = ""
    i = 0
    table_name = table['table']
    for column in table["columns"]:
        i += 1
        if(column.name == PRIMARY_KEY): continue
        if(column.is_foreign_key == True):
            col += f'"{column.name}": "{column.name}",\n\t\t'
        else: 
            col += f'"{column.name}": "{column.name}",\n\t\t'
        if(len(table["columns"]) == i):
            col = col[:-4]


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
    table_name = table['table']
    result = f"""{{ path: '{table_name}', element: <{table_name}ListView /> }},
      {{ path: '{table_name}/addedit', element: <{table_name}AddEditView /> }},
      """
    return result

def template_base_fields(table):
    result = ''
    table_name = table['table']

    for column in table["columns"]:
        if (column.name == PRIMARY_KEY or table["main_column"] == column.name): continue
        if (column.is_foreign_key == True):
            plural_table_name = to_plural(column.foreign_table)
            res = f"""
                  <Grid item md={{12}} xs={{12}}>
                    <LookUp
                      value={{store.{column.name}}}
                      onChange={{(event) => store.handleChange(event)}}
                      name="{column.name}"
                      data={{store.{plural_table_name}}}
                      id='id_f_{table_name}_{column.name}'
                      label={{translate('label:{table_name}AddEditView.{column.name}')}}
                      helperText={{store.errors.{column.name}}}
                      error={{!!store.errors.{column.name}}}
                    />
                  </Grid>"""

        elif (column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""
                  <Grid item md={{12}} xs={{12}}>
                    <DateTimeField
                      value={{store.{column.name}}}
                      onChange={{(event) => store.handleChange(event)}}
                      name="{column.name}"
                      id='id_f_{table_name}_{column.name}'
                      label={{translate('label:{table_name}AddEditView.{column.name}')}}
                      helperText={{store.errors.{column.name}}}
                      error={{!!store.errors.{column.name}}}
                    />
                  </Grid>"""

        elif(column.type == 'boolean'):
            res = f"""
                  <Grid item md={{12}} xs={{12}}>
                    <CustomCheckbox
                      value={{store.{column.name}}}
                      onChange={{(event) => store.handleChange(event)}}
                      name="{column.name}"
                      label={{translate('label:{table_name}AddEditView.{column.name}')}}
                      id='id_f_{table_name}_{column.name}'
                    />
                  </Grid>"""

        elif (column.type == 'character varying' or column.type == 'character' or column.type == 'integer' or column.type == 'double precision'):
            res = f"""
                  <Grid item md={{12}} xs={{12}}>
                    <CustomTextField
                      value={{store.{column.name}}}
                      onChange={{(event) => store.handleChange(event)}}
                      name="{column.name}"
                      data-testid="id_f_{table_name}_{column.name}"
                      id='id_f_{table_name}_{column.name}'
                      label={{translate('label:{table_name}AddEditView.{column.name}')}}
                      helperText={{store.errors.{column.name}}}
                      error={{!!store.errors.{column.name}}}
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
        result += f"""import {mtm_table}ListView from 'features/{mtm_table}/{mtm_table}ListView';
              """
    return result

def template_mtm_title(table):
    result = ''
    index = 0
    for mtm_table, mtm_column in table["mtms"]:
        result += f"""<Tab data-testid={{"{mtm_table}_tab_title"}} label={{translate("label:{mtm_table}ListView.entityTitle")}} {{...a11yProps({index})}} />
              """
        index += 1
    return result

def template_mtm_content(table):
    result = ''
    index = 0
    for mtm_table, mtm_column in table["mtms"]:
        result += f"""
      <CustomTabPanel value={{value}} index={{{index}}}>
        <{mtm_table}ListView idMain={{store.id}} />
      </CustomTabPanel>
            """
        index += 1
    return result

def template_save_save(table):
    result = ''
    table_name = table['table']
    for column in table["columns"]:
        if(table["main_column"] == column.name):
            res = f"""{table["main_column"]}: props.{table["main_column"]} - 0,
    """
        elif(column.type == 'integer' or column.type == 'double precision'):
            if(column.nullable == True):
                res = f"""{column.name}: store.{column.name} - 0 == 0 ? null : store.{column.name} - 0,
    """
            else:
                res = f"""{column.name}: store.{column.name} - 0,
    """
        elif(column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""str{column.name}: store.{column.name},
    """
        elif(column.type == 'boolean'):
            res = f"""{column.name}: !!store.{column.name},
    """
        elif(column.type == 'character varying' or column.type == 'character'):
            res = f"""{column.name}: store.{column.name},
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
        if(column.type == 'integer' or column.type == 'double precision'):
            res = f"""{column.name} = 0\n\t"""
        elif(column.type == 'character varying' or column.type == 'character'):
            res = f"""{column.name} = ""\n\t"""
        elif(column.type == 'boolean'):
            res = f"""{column.name} = false\n\t"""
        elif(column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""{column.name} = null\n\t"""
        elif (column.type == 'varbinary'):
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
        result += f'{to_plural(for_table[0])} = []\n\t'
    return result

def template_store_clear(table):
    result = ''
    for column in table["columns"]:
        if(column.name == PRIMARY_KEY): continue
        if(column.type == 'integer' or column.type == 'double precision'):
            res = f"""this.{column.name} = 0\n\t\t"""
        elif(column.type == 'character varying' or column.type == 'character' or column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""this.{column.name} = ""\n\t\t"""
        elif(column.type == 'boolean'):
            res = f"""this.{column.name} = false\n\t\t"""
        elif (column.type == 'varbinary'):
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
        result += f"""
      {column.name}: this.{column.name}{" - 0" if column.type == 'integer' else ""},"""
    return result

def template_store_load_dictionaries(table):
    result = ''
    for for_table in table['foreign_tables']:
        plural_table = to_plural(for_table[0])
        result += f"""
  load{plural_table} = async () => {{
    try {{
      MainStore.changeLoader(true);
      const response = await get{plural_table}();
      if ((response.status === 201 || response.status === 200) && response?.data !== null) {{
        this.{plural_table} = response.data
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
        if(column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            result += f"""
          this.{column.name} = dayjs(response.data.{column.name});"""
        else:
            result += f"""
          this.{column.name} = response.data.{column.name};"""
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
        valids = ""
        if(column.name == PRIMARY_KEY): continue
        if(column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            res = f"""
  {column.name}: yup
    .date()
    .nullable()
    .required("Required field")
    .typeError("Please provide a valid date"),"""
            
        elif(column.type == "integer"):
            res = f"""
  {column.name}: yup.number().notOneOf([0], "Required field").required("Required field"),"""
        elif(column.type == "boolean"):
            res = f"""
  {column.name}: yup.boolean().default(false),"""
        else:
            res = f"""
  {column.name}: yup.string(),"""

        
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
        if(column.name == PRIMARY_KEY): continue
        result += f"""&& {column.name} === ''\n\t"""
    return result

def template_index_columns(table):
    result = ''
    table_name = table['table']
    for column in table["columns"]:
        if(column.name == 'id' or table["main_column"] == column.name): continue
        label = column.name
        translate = column.name
        result += f"""
    {{
      field: '{label}',
      headerName: translate("label:{table_name}ListView.{label}"),
      flex: 1,
      renderCell: (param) => (<div data-testid="table_{table_name}_column_{label}"> {{param.row.{label}}} </div>),
      renderHeader: (param) => (<div data-testid="table_{table_name}_header_{label}">{{param.colDef.headerName}}</div>)
    }},"""
            
    return result

def template_index_is_mtm_popup(table):
    if(table['is_mtm']):
        return 'popup'
    else:
        return 'form'

def template_index_is_mtm_column_name(table):
    if(table['is_mtm']):
        return f"""
              {table["main_column"]}={{this.props.{table["main_column"]}}}"""
    else:
        return ""

def template_mtm_has_mtm(table):
    if(len(table['mtms']) != 0):
        return f"""{{/* start MTM */}}
            {{store.id > 0 && <Grid item xs={{12}} spacing={{0}}><MtmTabs /></Grid>}}
            {{/* end MTM */}}"""
    else:
        return ""

def template_mtm_has_mtm_grid(table):
    if(len(table['mtms']) != 0):
        return f"""store.id == 0 ? 6 : 12"""
    else:
        return "6"

def template_index_load_function(table):
    table_name = table['table']
    if(table['is_mtm']):
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
    if(table['is_mtm']):
        return f"""
  idMain: number;"""
    else:
        return ""

def template_store_index_load_function(table):
    table_name = table['table']
    if(table['is_mtm']):
        return f"""const response = await get{to_plural(table_name)}By{table["main_column"]}(this.idMain);"""
    else:
        return f"""const response = await get{to_plural(table_name)}();"""


def template_store_load_function(table):
    table_name = table['table']
    if(table['is_mtm']):
        return f'store.load{to_plural(table_name)}(this.props.idMain)'
    else:
        return f'store.load{to_plural(table_name)}()'
    

def template_fast_input_load_dicts(table):
    table_name = table['table']
    result = ""
    for column in table["columns"]:
        if(column.is_foreign_key == True):
            result += f"""storeAddEdit.load{to_plural(column.foreign_table)}()
            """
    return result

def template_fast_input_change_main_id(table):
    table_name = table['table']
    if(table['is_mtm']):
        return f"""storeAddEdit.{table["main_column"]} = this.props.idMain - 0"""
    else:
        return ""
    

def template_fast_input_columns(table):
    table_name = table['table']
    result = ""
    for column in table["columns"]:
        if(column.name=='id'): continue
        if(column.is_foreign_key == True):
            result += f"""{{
                    field: '{column.name}NavName',
                    width: null, //or number from 1 to 12
                    headerName: translate("label:SmProjectTagListView.{column.name}"),
                }},
                """
        else:
            result += f"""{{
                    field: '{column.name}',
                    width: null, //or number from 1 to 12
                    headerName: translate("label:SmProjectTagListView.{column.name}"),
                }},
                """
    return result

def template_constant_fields(table):
    result = ''
    for column in table["columns"]:
        if(column.type == 'integer'):
            result += f"""
  {column.name}: number;"""
        elif(column.type == 'timestamp without time zone' or column.type == 'timestamp with time zone'):
            result += f"""
  {column.name}: Dayjs;"""
        elif(column.type == 'boolean'):
            result += f"""
  {column.name}: boolean;"""
        else:
            result += f"""
  {column.name}: string;"""
    return result


def template_export_mtm_api(table):
    if(table["is_mtm"]):
        return f"""
export const get{table_name_plural(table)}By{table["main_column"]} = ({table["main_column"]}: number): Promise<any> => {{
  return http.get(`/{table['table']}/GetBy{table["main_column"]}?{table["main_column"]}=${{{table["main_column"]}}}`);
}};"""
    else:
        return ""


def template_fastinput_fields(table):
    result = ''
    table_name = table['table']

    for column in table["columns"]:
        if (column.name == PRIMARY_KEY or table["main_column"] == column.name): continue
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

        elif(column.type == 'boolean'):
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

        elif (column.type == 'character varying' or column.type == 'character' or column.type == 'integer' or column.type == 'double precision'):
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

        elif (column.type == 'varbinary'):
            continue
        else:
            raise Exception('Не могу найти тип - "' + column.type + '"')
        result += res
    return result


def table_get_list_import(table):
    result = ''
    if(table["is_mtm"]):
        result = f'import {{ get{table_name_plural(table)}By{table["main_column"]} }} from "api/{table["table"]}";'
    else:
        result = f'import {{ get{table_name_plural(table)} }} from "api/{table["table"]}";'

    return result


def template_store_import_dictionaries(table):
    result = ''
    for for_table in table['foreign_tables']:
        plural_table = to_plural(for_table[0])
        result += f"""
import {{ get{plural_table} }} from "api/{for_table[0]}";
    """
    return result

TEMPLATE_FUNCS = {
    "template_dto": template_dto,
    "table_name_plural": table_name_plural,
    "table_name": table_name,
    "get_main_column": get_main_column,
    "table_get_list_import": table_get_list_import,
    "template_store_import_dictionaries": template_store_import_dictionaries,
    "template_export_mtm_api": template_export_mtm_api,
    "template_constant_fields": template_constant_fields,
    "template_index_list_props": template_index_list_props,
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
