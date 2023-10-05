PRIMARY_KEY = "id"

CONNECTING_STRING = 'DRIVER={SQL Server};Server=(local);Database=GeologyDB;Trusted_Connection=True;MultipleActiveResultSets=true'

# CONN_STR_PGSQL = 'DRIVER={Devart ODBC Driver for PostgreSQL};Server=localhost;Port=5432;Database=Ambulance;User ID=postgres;Password=00890;String Types=Unicode'
# CONN_STR_PGSQL = 'DRIVER={Devart ODBC Driver for PostgreSQL};Server=194.87.102.173;Port=5433;Database=Ambulance;Username=postgres;Password=dimaMolodec123;String Types=Unicode'
CONN_STR_PGSQL = 'DRIVER={Devart ODBC Driver for PostgreSQL};Server=81.200.146.76;Port=5432;Database=database_t2;Username=postgres;Password=dimaMolodec123;String Types=Unicode'




# SUBD = "MSSQL"
# # mssql
# SQL_COLUMNS = """SELECT TABLE_NAME, COLUMN_NAME, IS_NULLABLE, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS ORDER by "TABLE_NAME" """
# SQL_FOREIGN_COLUMNS = """
#     SELECT 
#     OBJECT_NAME(f.parent_object_id) table_name,
#     COL_NAME(fc.parent_object_id,fc.parent_column_id) col_name,
#     t.name foreign_table
#     FROM 
#     sys.foreign_keys AS f
#     INNER JOIN 
#     sys.foreign_key_columns AS fc 
#         ON f.OBJECT_ID = fc.constraint_object_id
#     INNER JOIN 
#     sys.tables t 
#         ON t.OBJECT_ID = fc.referenced_object_id
#     Order by table_name
#     """







SUBD = "PGSQL"
# pgsql
# SQL_COLUMNS = """SELECT table_name, column_name, is_nullable, data_type FROM information_schema.columns WHERE table_schema = 'public' ORDER BY table_name"""
SQL_COLUMNS = """SELECT table_name, column_name, is_nullable, data_type FROM information_schema.columns WHERE table_schema = 'public' ORDER BY "dtd_identifier" """
SQL_FOREIGN_COLUMNS = """
    SELECT
    tc.table_name, kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM
    information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage 
        AS kcu ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage 
        AS ccu ON ccu.constraint_name = tc.constraint_name
WHERE constraint_type = 'FOREIGN KEY';
"""

PGCON = {
    "user":"postgres",
    "password":"dimaMolodec123",
    "host":"194.87.102.173",
    "port":"5433",
    "database":"2t_database_1909"
}


        # cnxn = psycopg2.connect(user="postgres",
        #                         password="dimaMolodec123",
        #                         host="194.87.102.173",
        #                         port="5433",
        #                         database="Ambulance")
        # cnxn = psycopg2.connect(user="postgres",
        #                         password="00890",
        #                         host="localhost",
        #                         port="5432",
        #                         database="amb_prod1807")
        # cnxn = psycopg2.connect(user="postgres",
        #                         password="dimaMolodec123",
        #                         host="194.87.102.173",
        #                         port="5433",
        #                         database="2t_database_1909")