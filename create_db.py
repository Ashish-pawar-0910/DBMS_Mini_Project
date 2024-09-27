import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Adesh@65",
    )

my_cursor= mydb.cursor()

# my_cursor.execute("CREATE DATABASE users")  commented not to run repeatedly

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)