import mysql.connector
import matplotlib.pyplot as plt

config = {
    'user' : 'root',
    'password' : 'masterkey',
    'host' : 'localhost',
    'database' : 'datamining',
    'ssl_disabled' : True
}

cnx = mysql.connector.connect(**config)

cursor = cnx.cursor()

query = """
    SELECT 
        DTPREGAO,
        VLEXTRINSECO
    FROM
        COTAHIST
    WHERE
        CODNEG = 'PETRH298'
    ORDER BY
        DTPREGAO"""

cursor.execute(query)

result = cursor.fetchall()

data=[]
dates=[]
for row in result:
    data.append(row[1])
    dates.append(row[0])

plt.plot(dates,data)
plt.show()

cnx.close()