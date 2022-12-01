import pyodbc

from settings import CONNECTING_STRING, PRIMARY_KEY



def get_tables():
    cnxn = pyodbc.connect(CONNECTING_STRING)
    cursor = cnxn.cursor()

    table_columns = """SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG='CourseTest' ORDER by "TABLE_NAME" """

    text_columns = """ SELECT TABLE_NAME, COLUMN_NAME, IS_NULLABLE, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS ORDER by "TABLE_NAME" """

    cursor.execute(text_columns)
    
    rows = []
    table_names = []
    all_data = []

    for row in cursor.fetchall():
        rows.append(row)
        is_null = True if row[2] == "YES" else False
        column = Column(row[1], is_null, row[3], False)
        # column = {"name": row[1], "nullable": is_null, "type": row[3], "is_foreign_key": False} # todo wtf foreign key

        if(row[0] not in table_names):
            table_names.append(row[0])
            r = {"table": row[0], "columns": [column]}
            all_data.append(r)
        else:
            all_data[table_names.index(row[0])]["columns"].append(column)

    return all_data


class Column:
    def __init__(self, name, nullable, type, is_foreign_key):
        self.name = name
        self.nullable = nullable
        self.type = type
        self.is_foreign_key = is_foreign_key

    def get_data(self):
        return self.name  + ", " + self.type