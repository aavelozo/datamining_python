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
        CODNEG,
        DTPREGAO,        
        VLEXTRINSECO
    FROM
        COTAHIST
    WHERE
        CODNEG in (
            'PETRG311',
            'PETRG319'
        )
    ORDER BY
        DTPREGAO"""

cursor.execute(query)

result = cursor.fetchall()

data={
    "PETRG311":{
        "x":[],
        "y":[]
    },
    "PETRG319":{
        "x":[],
        "y":[]
    }
}
#print(data)
for row in result:
    #print(row[0],data[row[0]])
    data[row[0]]["x"].append(row[1])
    data[row[0]]["y"].append(row[2])
#print(data)
#print(dates)
plt.plot(data["PETRG311"]["x"],data["PETRG311"]["y"],data["PETRG319"]["x"],data["PETRG319"]["y"])
plt.show()

cnx.close()