from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys

print (sys.argv[1])

sqlEngine       = create_engine('mysql+pymysql://Minemas_R:b1EppZu9bX6vhvMf@endurorecambios.com/Minemas_R')
dbConnection    = sqlEngine.connect()
df = pd.read_excel(sys.argv[1])
print(df)
df.to_sql(name = 'Bruta_BRP', con = dbConnection, if_exists = 'replace', index = False)
df.to_sql(name = 'Andrea', con = dbConnection, if_exists = 'replace', index = False)
df = pd.read_excel(sys.argv[2])
print(df)
df.to_sql(name = 'Bruta_BRP', con = dbConnection, if_exists = 'append', index = False)

