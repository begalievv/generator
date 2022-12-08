import pyodbc

from settings import CONNECTING_STRING, PRIMARY_KEY


def get_tables():
    main_tables = ["Employee", "Student", "Course", "Lesson", "Group"]
    mtm_tables = {
        "Subject": "CourseName", 
        "LessonStatusHistory": "Lesson", 
        "EmployeeInCourse": "Course", 
        "EmployeeRole": "Employee",
        "StudentInGroup": "Group",
        "StudentInLesson": "Lesson",
        "PassedCourse": "Student",
        "StudentContact": "Student",
        "CourseStatusHistory": "Course"
    }
    cnxn = pyodbc.connect(CONNECTING_STRING)
    cursor = cnxn.cursor()

    text_columns = """ SELECT TABLE_NAME, COLUMN_NAME, IS_NULLABLE, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS ORDER by "TABLE_NAME" """
    cursor.execute(text_columns)

    rows = []
    table_names = []
    all_data = []

    for row in cursor.fetchall():
        if(row[0] == 'sysdiagrams'): continue
        rows.append(row)
        is_null = True if row[2] == "YES" else False
        column = Column(row[1], is_null, row[3], False)
        # column = {"name": row[1], "nullable": is_null, "type": row[3], "is_foreign_key": False} # todo wtf foreign key

        if (row[0] not in table_names):
            table_names.append(row[0])
            r = {"table": row[0], "columns": [column]}
            all_data.append(r)
        else:
            all_data[table_names.index(row[0])]["columns"].append(column)


    # text_constraints = """SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE """
    # cursor.execute(text_constraints)

    # cons_row = []
    # foreign_tables = []
    # foreign_columns = []

    # for row in cursor.fetchall():
    #     if(row[0].upper().startswith("FK_")):
    #         cons_row.append(row)
    #         foreign_tables.append(row[1])
    #         foreign_columns.append(row[2])
            
    # for i in range(len(foreign_tables)):
    #     for j in range(len(all_data)):
    #         if(all_data[j]["table"] == foreign_tables[i]):
    #             cols = all_data[j]["columns"]
    #             for h in range(len(cols)):
    #                 if(foreign_columns[i] == cols[h].name):
    #                     all_data[j]["columns"][h].is_foreign_key = True
    #                     break
    #             break


    foreign_tables_text =  """
    SELECT 
    OBJECT_NAME(f.parent_object_id) table_name,
    COL_NAME(fc.parent_object_id,fc.parent_column_id) col_name,
    t.name foreign_table
    FROM 
    sys.foreign_keys AS f
    INNER JOIN 
    sys.foreign_key_columns AS fc 
        ON f.OBJECT_ID = fc.constraint_object_id
    INNER JOIN 
    sys.tables t 
        ON t.OBJECT_ID = fc.referenced_object_id
    Order by table_name
    """
    cursor.execute(foreign_tables_text)
    foreign_tables = []
    for row in cursor.fetchall():
        foreign_tables.append(row)

    for table in all_data:
        f_table = []
        c_table = []
        for for_table in foreign_tables:
            if(for_table[0] == table["table"]):
                f_table.append([for_table[2], for_table[1]])
                for column in table["columns"]:
                    if(column.name == for_table[1]):
                        column.is_foreign_key = True
                        column.foreign_table = for_table[2]
            if(for_table[2] == table["table"]):
                c_table.append([for_table[0], for_table[1]])
        table['foreign_tables'] = f_table
        table['constraint_tables'] = c_table

        table["is_mtm"] = False
        table["main"] = ""
        table["main_column"] = ""
        table["is_main"] = False
        table["mtms"] = []
        
        for key, value in mtm_tables.items():
            if(key == table["table"]):
                table["is_mtm"] = True
                table["main"] = value
                for i in range(len(f_table)):
                    if(f_table[i][0] == value):
                        table["main_column"] = f_table[i][1]
            if(value == table["table"]):
                table["is_main"] = True
                for c_table ,c_column in table['constraint_tables']:
                    if(c_table == key):
                        table["mtms"].append([key, c_column])
                        break

    return all_data
    # for table in all_data:
    #     print(table['table'], ' ----- ', table["mtms"])
        # print(table['table'], ' ----- ', table["is_main"], ', ', table["mtms"])
        # for column in table['columns']:
        #     print(column.name, ' ---- ', column.is_foreign_key, ' ---- ', column.foreign_table)



class Column:
    def __init__(self, name, nullable, type, is_foreign_key):
        self.name = name
        self.nullable = nullable
        self.type = type
        self.is_foreign_key = is_foreign_key
        self.foreign_table = ''

    def get_data(self):
        return self.name + ", " + self.type
