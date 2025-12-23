from sqlalchemy import create_engine
import pymysql
import pandas as pd

sqlEngine = create_engine('mysql+pymysql://Minemas_R:b1EppZu9bX6vhvMf@endurorecambios.com/Alim')

dbConnection = sqlEngine.connect()

frame = pd.read_sql("select * from test.uservitals", dbConnection);

pd.set_option('display.expand_frame_repr', False)

print(frame)

dbConnection.close()

125_22vs21
200_22vs21
250_22vs21
300_22vs21
350_22vs21
390_22vs21
430_22vs21
480_22vs21
xtrainer_250_22vs21
xtrainer_300_22vs21