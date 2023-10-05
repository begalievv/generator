# import pyodbc
import psycopg2

from settings import CONNECTING_STRING, PRIMARY_KEY, SUBD, CONN_STR_PGSQL, SQL_COLUMNS, SQL_FOREIGN_COLUMNS, PGCON



def get_tables():
    need_tables = ["ProjectMember", "Project"]
    mtm_tables = {
        "ProjectMember": "Project",
        # "meetingReport": "VideoMeeting",
    }
    if(SUBD == 'MSSQL'):
        cnxn = psycopg2.connect(CONNECTING_STRING)
    else:
        cnxn = psycopg2.connect(**PGCON)

    cursor = cnxn.cursor()

    
    cursor.execute(SQL_COLUMNS)

    rows = []
    table_names = []
    all_data = []

    for row in cursor.fetchall():
        if(row[0] == 'sysdiagrams'): continue
        if(len(need_tables) != 0 and row[0] not in need_tables):
            continue
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

    
    cursor.execute(SQL_FOREIGN_COLUMNS)

    foreign_tables = []
    for row in cursor.fetchall():
        if(len(need_tables) != 0 and row[0] not in need_tables):
            continue
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
