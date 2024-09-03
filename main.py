import pandas as pd
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
        H.CODNEG,
        H.DTPREGAO,        
        coalesce(H.VLEXTRINSECO,H.PREULT) AS VLEXTRINSECO,
        H.DATVEN,
        DATEDIFF(H.DTPREGAO,H.DATVEN) AS LIFEDAYS
    FROM
        COTAHIST H
    WHERE
        H.TPMERC IN (70,80)
        /*AND H.CODNEG LIKE 'PETRD%'*/
        AND H.CODNEG = 'PETRL361'
        AND DATEDIFF(H.DTPREGAO,H.DATVEN) >= -180
        /*AND H.STATUSOPCPERC BETWEEN -50 AND 50
        AND NOT EXISTS(
            SELECT 1
            FROM
                COTAHIST H2
            WHERE
                H2.CODNEG = H.CODNEG
                AND H2.STATUSOPC IN ('ATM','ITM')
        )*/
    ORDER BY
        DATEDIFF(H.DTPREGAO,H.DATVEN) DESC"""

cursor.execute(query)
result = cursor.fetchall()
#print(result)
colunas = [desc[0] for desc in cursor.description]
data2 = pd.DataFrame(result, columns=colunas)
data2['DTPREGAO'] = pd.to_datetime(data2['DTPREGAO'])
data2['DATVEN'] = pd.to_datetime(data2['DATVEN'])
#data2['DIAS_PARA_VENCIMENTO'] = (data2['DATVEN'] - data2['DTPREGAO']).dt.days
data2['DIAS_PARA_VENCIMENTO'] = pd.to_numeric(data2['LIFEDAYS'])
correlacao = data2['VLEXTRINSECO'].corr(data2['DIAS_PARA_VENCIMENTO'])
print(f'Correlação entre valor extrínseco e dias para o vencimento: {correlacao}')
plots,subPlots = plt.subplots(2)
subPlots[0].scatter(data2['DIAS_PARA_VENCIMENTO'], data2['VLEXTRINSECO'])
subPlots[0].set_xlabel('Dias para Vencimento')
subPlots[0].set_ylabel('Valor Extrínseco')
subPlots[0].set_title('Correlação entre Valor Extrínseco e Dias para Vencimento')
#subPlots[0].show()

data={}

for row in result:
    if row[0] not in data:
        data[row[0]] = {"x":[],"y":[]}
    data[row[0]]["x"].append(row[4])
    data[row[0]]["y"].append(row[2])

for key in data:
    subPlots[1].plot(data[key]["x"],data[key]["y"])
plt.show()

cnx.close()