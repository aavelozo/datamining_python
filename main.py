import mysql.connector

config = {
    'user' : 'root',
    'password' : 'masterkey',
    'host' : 'localhost',
    'database' : 'datamining',
    'ssl_disabled' : True
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor()

query = ("SELECT * from cotahist where id<100")

cursor.execute(query)

result = cursor.fetchall()

print(result)

cnx.close()