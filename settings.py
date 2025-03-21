PRIMARY_KEY = "id"

CONNECTING_STRING = 'DRIVER={SQL Server};Server=(local);Database=GeologyDB;Trusted_Connection=True;MultipleActiveResultSets=true'
CONN_STR_PGSQL = ''









SUBD = "PGSQL"
# pgsql
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
    "password":"pass",
    "host":"127.0.0.1",
    "port":"5433",
    "database":"database"
}

PGCONSERVER = {
    "host":"local",
    "user":"postgres",
    "password":"pass",
    "port":"5434",
    "database":"database"
}

