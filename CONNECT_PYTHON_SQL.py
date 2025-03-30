import pymysql
from sqlalchemy import create_engine
import mysql.connector
import pandas as pd
import numpy as np
import getpass

user = ''
passw = ''
host = ''
port = ''

database = 'definir schema a ser importado'
tabela = 'definir tabela a ser importada'

# ================= SQLALCHEMY ===================
# IMPORT
mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database, echo=False)
DF = pd.read_sql('SELECT * FROM `' + tabela + '`', con=mydb)
mydb.dispose()

#  EXPORT 
mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database, echo=False)
DF.to_sql(name=tabela, con=mydb, if_exists='replace', index=False)
mydb.dispose()


# =============== MYSQL.CONNECTOR ==================
conn = mysql.connector.connect(host=host, user=user, password=passw, database=database)

#  IMPORT 
DF = pd.read_sql(f'SELECT * FROM {tabela}', conn)

#  EXPORT 
cursor = conn.cursor()
for _, row in DF.iterrows():
    cursor.execute(f"INSERT INTO {tabela} VALUES ({', '.join(['%s'] * len(row))})", tuple(row))
conn.commit()

cursor.close()
conn.close()