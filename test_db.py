import psycopg2


# try:
connection = psycopg2.connect(user="postgres",
                                password="dimaMolodec123",
                                host="194.87.102.173",
                                port="5433",
                                database="Ambulance")
cursor = connection.cursor()
postgreSQL_select_Query = 'select * from "Employee"'

cursor.execute(postgreSQL_select_Query)
print("Selecting rows from mobile table using cursor.fetchall")
mobile_records = cursor.fetchall()

print("Print each row and it's columns values")
for row in mobile_records:
    print(row )

# except (Exception, psycopg2.Error) as error:
#     print("Error while fetching data from PostgreSQL", error)

# finally:
#     # closing database connection.
#     if connection:
#         cursor.close()
#         connection.close()
#         print("PostgreSQL connection is closed")
