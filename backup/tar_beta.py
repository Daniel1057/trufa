from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys

def sql_minemas_r(sql):
    dbConecction = pymysql.connect(host = 'endurorecambios.com',user='Minemas_R',passwd = 'b1EppZu9bX6vhvMf',db='Minemas_R')
    cur = dbConecction.cursor()
    cur.execute(sql)
    dbConecction.commit()
    dbConecction.close()

def table_to_df(sql):
    sqlEngine = create_engine('mysql+pymysql://Minemas_R:b1EppZu9bX6vhvMf@endurorecambios.com/Minemas_R')
    dbConnection = sqlEngine.connect()
    frame = pd.read_sql(sql, dbConnection);
    dbConnection.close()
    return frame

def carga_tarifa_bbdd(dataframe,tabla):
    sqlEngine = create_engine('mysql+pymysql://Minemas_R:b1EppZu9bX6vhvMf@endurorecambios.com/Minemas_R')
    dbConnection = sqlEngine.connect()
    dataframe.to_sql(name=tabla, con=dbConnection, if_exists='replace', index=False)
    print ("actualizado")
    dbConnection.close()

def generar_dataframes(fichero_tarifa,fichero_inventario):
    beta_web = table_to_df('SELECT * FROM v_beta_product')
    beta_web['cod'] = beta_web['reference'].str.replace('.', '',regex=True)
    inventario = pd.DataFrame()
    hojas = pd.ExcelFile(fichero_inventario).sheet_names
    for hoja in hojas:
        temporal = pd.read_excel(fichero_inventario,hoja)
        inventario = inventario.append(temporal.values.tolist(),ignore_index = True)
    inventario = inventario.rename(
        columns={0: "Cod_factusol", 1: "Desc_factusol", 2: "Ref_Prov_Factusol", 3: "Porv_factusol", 4: "Costo_Factusol",
                 5: "PVP_Factusol", 6: "Stock_Factusol", 7: "Obs_Factusol"})
    tarifa = pd.read_excel(fichero_tarifa)
    tarifa['cod']=tarifa['Article'].str.replace('.','',regex=True)
    tarifa = pd.merge(left=tarifa, right=beta_web, how='left', left_on='cod', right_on='cod')
    inventario['cod'] = inventario['Cod_factusol'].str.replace('.', '', regex=True)
    carga_tarifa_bbdd(inventario,'t_inventario_factusol')
    tarifa= pd.merge(left=tarifa, right=inventario, how='left', left_on='cod', right_on='cod')
    if (tarifa[tarifa['Descripcion'].str.contains('#',na=False, regex=True)].size > 0):
        tarifa_obsoletos = tarifa[tarifa['Descripcion'].str.contains('#', na=False, regex=True)]
        tarifa_obsoletos.to_excel('tar_beta_obs.xlsx')
        carga_tarifa_bbdd(tarifa_obsoletos, 't_obsoletos_beta')
        tarifa= tarifa.drop(tarifa[tarifa['Descripcion'].str.contains('#', na=False, regex=True)].index)
    if (tarifa[tarifa['Descripcion'].str.contains('ARTICULO NO SUMINISTRABLE', na=False, regex=True)].size > 0):
        tarifa_no_vta = tarifa[tarifa['Descripcion'].str.contains('ARTICULO NO SUMINISTRABLE', na=False, regex=True)]
        tarifa_no_vta.to_excel('tar_no_vta.xlsx')
        carga_tarifa_bbdd(tarifa_no_vta, 't_no_vta_beta')
        tarifa = tarifa.drop(tarifa[tarifa['Descripcion'].str.contains('ARTICULO NO SUMINISTRABLE', na=False, regex=True)].index)
    if(tarifa[tarifa.Preu == 0].size>0):
        tarifa_precio0 = tarifa[tarifa.Preu == 0]
        tarifa_precio0.to_excel('tar_preu_0.xlsx')
        carga_tarifa_bbdd(tarifa_precio0, 't_preu0_beta')
        tarifa.drop(tarifa[tarifa.Preu == 0].index)
    tarifa.to_excel('tar_beta_limpia.xlsx')
    carga_tarifa_bbdd(tarifa, 't_tarifa_beta')
    change_price = table_to_df('SELECT * FROM t_tarifa_beta where Preu` <>price')
    change_price.to_excel('change_price_beta.xlsx')
    print (tarifa)

def tablas_web():
    #Indicies de las tablas
    sql_minemas_r("ALTER TABLE `Minemas_R`.`t_tarifa_beta` ADD INDEX (`Article`(64), `cod`(64))")
    sql_minemas_r("ALTER TABLE `Minemas_R`.`t_no_vta_beta` ADD INDEX (`Article`(64), `cod`(64))")
    sql_minemas_r("ALTER TABLE `Minemas_R`.`t_obsoletos_beta` ADD INDEX (`Article`(64), `cod`(64))")
    sql_minemas_r("ALTER TABLE `Minemas_R`.`t_preu0_beta` ADD INDEX (`Article`(64), `cod`(64))")
    sql_minemas_r("ALTER TABLE `Minemas_R`.`t_inventario_factusol` ADD INDEX (`Cod_factusol`(64), `cod`(64))")
if __name__ == '__main__':
    generar_dataframes('TARIFA 15-09-2021.xlsx','Inventario.XLSX')
    tablas_web()