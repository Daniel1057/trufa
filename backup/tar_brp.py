from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys
import main

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

def create_temp_table(sql,destino):
    sqlEngine = create_engine('mysql+pymysql://Minemas_R:b1EppZu9bX6vhvMf@endurorecambios.com/Minemas_R')
    dbConnection = sqlEngine.connect()
    frame = pd.read_sql(sql, dbConnection)
    frame.to_sql(name=destino, con=dbConnection, if_exists='replace', index=False)
    print ("Tabla creada "+str(destino))
    dbConnection.close()

def carga_tarifa_bbdd(dataframe,tabla):
    sqlEngine = create_engine('mysql+pymysql://Minemas_R:b1EppZu9bX6vhvMf@endurorecambios.com/Minemas_R')
    dbConnection = sqlEngine.connect()
    dataframe.to_sql(name=tabla, con=dbConnection, if_exists='replace', index=False)
    print ("actualizado")
    dbConnection.close()


def cambio_ref_b():
    dbConecction = pymysql.connect(host = 'endurorecambios.com',user='Minemas_R',passwd = 'b1EppZu9bX6vhvMf',db='Minemas_R')
    cur = dbConecction.cursor()
    sql_change_ref_ps_product = "update t_referen_subs a, nuevaendurorecambios.ps_product b Set b.reference = a.Subtitude_Part where a.id_product = b.id_product"
    sql_change_name = 'UPDATE Minemas_R.t_referen_subs a ,nuevaendurorecambios.ps_product_lang b SET b.name = CONCAT(b.name," - ",a.Subtitude_Part) where a.id_product = b.id_product'
    sql_change_description = "update Minemas_R.t_referen_subs a ,nuevaendurorecambios.ps_product_lang b   set b.description=REPLACE(b.description,a.reference,a.Subtitude_Part) where a.id_product = b.id_product"
    sql_change_ref_ps_product_att = "update  nuevaendurorecambios.ps_product b, nuevaendurorecambios.ps_product_attribute c set c.reference = b.reference  where b.reference <> c.reference and b.id_product = c.id_product and b.id_manufacturer = 103"
    try:
        cur.execute(sql_change_ref_ps_product)
        print("Update referencia")
        dbConecction.commit()
        cur.execute(sql_change_name)
        print("Update name")
        dbConecction.commit()
        cur.execute(sql_change_description)
        print("update description")
        cur.execute(sql_change_ref_ps_product_att)
        print("Igualando referencias entre ps_product y ps_product_attribute")

        dbConecction.commit()

    except Exception as e:
        print (e)
        dbConecction.rollback()
    dbConecction.close()

def actualiza_price(shop):
    dbConecction = pymysql.connect(host = 'endurorecambios.com',user='Minemas_R',passwd = 'b1EppZu9bX6vhvMf',db='Minemas_R')
    cur = dbConecction.cursor()
    sql_ps_product = "update nuevaendurorecambios.ps_product a, Minemas_R.t_change_price b set a.price = b.Retail_Price  where a.`id_shop_default` = "+str(shop)+" and a.id_product = b.id_product"
    #Cambiar esta línea por actulizar directamente desde la ps_product price
    sql_ps_product_shop ="update nuevaendurorecambios.ps_product_shop r, Minemas_R.t_change_price b set r.price = b.Retail_Price where r.id_shop = "+str(shop)+" and r.id_product = b.id_product"
    sql_ps_product_shop_reference="update nuevaendurorecambios.ps_product_attribute r, Minemas_R.t_change_price b  set r.reference = b.Subtitude_Part where r.id_product = b.id_product "
    sql_ps_product_shop_price = "update nuevaendurorecambios.ps_product_attribute r, Minemas_R.t_change_price s set r.`price` = s.Retail_Price  where r.id_product = s.id_product"
    #sql_ps_product_attribute_shop="update nuevaendurorecambios.ps_product_attribute_shop r, Minemas_R.t_change_price s set r.price = s.Retail_Price where r.id_shop = "+str(shop)+" and r.id_product = s.id_product"
    try:
        dbConecction.commit()
        cur.execute(sql_ps_product)
        print ("Update sql products")
        dbConecction.commit()
        cur.execute(sql_ps_product_shop)
        print("Update sql products shop")
        dbConecction.commit()
        cur.execute(sql_ps_product_shop_reference)
        print("Update sql products shop reference")
        dbConecction.commit()
        cur.execute(sql_ps_product_shop_price)
        print("Update sql products shop price")
        dbConecction.commit()
        #cur.execute(sql_ps_product_attribute_shop)
        #print("Update sql products shop attribute shop")
        #dbConecction.commit()
    except Exception as e:
        print (e)
        dbConecction.rollback()

    dbConecction.close()
def familia_descuento(df):
    df['Id_Familia_Descuento'] = 5
    df['Descuento'] = 0
    for i in df.index:
        Margen = df['Margen'][i]
        print (i)
        print (Margen)
        Id_Familia_Descuento = 5
        Descuento = 0
        if (Margen >= 0.19 and Margen < 0.24):
            Id_Familia_Descuento = 20
            Descuento = 5
        if (Margen >= 0.24 and Margen < 0.29):
            Id_Familia_Descuento = 25
            Descuento = 10
        if (Margen >= 0.29 and Margen < 0.34):
            Id_Familia_Descuento = 30
            Descuento = 15
        if (Margen >= 0.34 and Margen < 0.39):
            Id_Familia_Descuento = 35
            Descuento = 20
        if (Margen >= 0.39 and Margen < 0.44):
            Id_Familia_Descuento = 40
            Descuento = 25
        if (Margen >= 0.44 and Margen < 0.48):
            Id_Familia_Descuento = 45
            Descuento = 25
        if (Margen >= 0.48 and Margen < 0.54):
            Id_Familia_Descuento = 50
            Descuento = 30
        if (Margen >= 0.54 and Margen < 0.59):
            Id_Familia_Descuento = 55
            Descuento = 30
        if (Margen >= 0.59 ):
            Id_Familia_Descuento = 60
            Descuento = 40
        df.at[i,'Id_Familia_Descuento'] = Id_Familia_Descuento
        df.at[i,'Descuento'] = Descuento
    return df
def inicio_tarifa_brp(fichero1,fichero2,fichero_inventario):

    brp_web = table_to_df('SELECT * FROM v_brp_product')
    brp_web['cod'] = brp_web['reference'].str.replace('.', '',regex=True)
    tarifa = pd.read_excel(fichero1)
    tarifa2 = pd.read_excel(fichero2)
    tarifa = pd.concat([tarifa,tarifa2], ignore_index=True)
    total = tarifa.size
    tarifa = tarifa.drop_duplicates()
    neto = tarifa.size
    duplicados = total - neto
    devuelve = [total,duplicados,neto]
    inventario = pd.DataFrame()
    hojas = pd.ExcelFile(fichero_inventario).sheet_names
    for hoja in hojas:
        temporal = pd.read_excel(fichero_inventario, hoja)
        inventario = inventario.append(temporal.values.tolist(), ignore_index=True)
    inventario = inventario.rename(
        columns={0: "Cod_factusol", 1: "Desc_factusol", 2: "Ref_Prov_Factusol", 3: "Porv_factusol", 4: "Costo_Factusol",
                 5: "PVP_Factusol", 6: "Stock_Factusol", 7: "Obs_Factusol"})

    error_ref_sin_descripcion = inventario[inventario["Desc_factusol"] == 'SIN DESCRIPCIÓN']
    error_ref_sin_descripcion.to_excel('salida_excel/error_sin_descripcion_factu.xlsx')
    inventario = inventario[inventario["Desc_factusol"] != 'SIN DESCRIPCIÓN']

    #carga_tarifa_bbdd(inventario,'T_Inventario_factusol')

    # Calculo del margen y del descuentos
    tarifa['Margen'] = round((tarifa['Retail_Price'] - tarifa['Dealer_Price']) / tarifa['Retail_Price'], 2)
    tarifa = familia_descuento(tarifa)


    #Genera la tarifa de Factusol
    df_tarifa_factusol = pd.merge(left=tarifa, right=inventario, how='inner', left_on='Material_No', right_on='Cod_factusol')
    df_tarifa_factusol = df_tarifa_factusol[['Cod_factusol','Stock_Factusol','Retail_Price','Dealer_Price','Act_Code','Subtitude_Part','Price_Cat_Desc','Margen','Descuento','Id_Familia_Descuento']]
    #Cambios de referencia
    df_tarifa_factusol_sustituciones = df_tarifa_factusol[df_tarifa_factusol['Subtitude_Part'].notna()]
    df_tarifa_factusol_sustituciones.to_excel('salida_excel/brp_factusol_sustituciones.xlsx')
    df_tarifa_factusol=df_tarifa_factusol[df_tarifa_factusol['Subtitude_Part'].isna()]

    #Errores precio de coste = vta
    df_error_sin_margen = df_tarifa_factusol[df_tarifa_factusol['Retail_Price'] == df_tarifa_factusol['Dealer_Price']]
    df_error_sin_margen.to_excel('salida_excel/brp_factusol_sin_margen.xlsx')
    df_tarifa_factusol = df_tarifa_factusol[df_tarifa_factusol['Retail_Price'] != df_tarifa_factusol['Dealer_Price']]


    df_tarifa_factusol['Dif_vta_coste'] = df_tarifa_factusol['Retail_Price'] - df_tarifa_factusol['Dealer_Price']
    df_tarifa_factusol['Media_cambio'] = df_tarifa_factusol['Dif_vta_coste'].mean()
    df_tarifa_factusol['Desviacion con la media'] = df_tarifa_factusol['Dif_vta_coste'] / df_tarifa_factusol['Media_cambio']

    df_tarifa_factu_descatalogados = df_tarifa_factusol[df_tarifa_factusol['Act_Code'] == 'OBS']
    df_tarifa_factusol=df_tarifa_factusol[df_tarifa_factusol['Act_Code'] != 'OBS']
    df_tarifa_factu_descatalogados_stock = df_tarifa_factu_descatalogados[df_tarifa_factu_descatalogados['Stock_Factusol'] > 0]
    df_tarifa_factu_descatalogados_stock.to_excel('salida_excel/df_tarifa_factu_descatalogados_stock.xlsx')
    df_tarifa_factu_descatalogados_pdte_servir=df_tarifa_factu_descatalogados[df_tarifa_factu_descatalogados['Stock_Factusol']<1]
    df_tarifa_factu_descatalogados_pdte_servir.to_excel('salida_excel/df_tarifa_factu_descatalogados_pdte_servir.xlsx')
    df_tarifa_factu_descatalogados = df_tarifa_factu_descatalogados[df_tarifa_factu_descatalogados['Stock_Factusol'].isna()]
    df_tarifa_factu_descatalogados.to_excel('salida_excel/df_tarifa_factu_descatalogados.xlsx')

    df_tarifa_factu_ropa = df_tarifa_factusol[df_tarifa_factusol['Price_Cat_Desc'] == 'W - Clothing']
    df_tarifa_factu_ropa_stock = df_tarifa_factu_ropa[df_tarifa_factu_ropa['Stock_Factusol'] > 0]
    df_tarifa_factu_ropa_sin_stock = df_tarifa_factu_ropa[df_tarifa_factu_ropa['Stock_Factusol'].isna()]
    df_tarifa_factu_ropa_stock.to_excel('salida_excel/df_tarifa_factu_ropa_stock.xlsx')
    df_tarifa_factu_ropa_sin_stock.to_excel('salida_excel/df_tarifa_factu_ropa_sin_stock.xlsx')

    df_tarifa_factusol_alerta_cambio = df_tarifa_factusol[df_tarifa_factusol['Desviacion con la media'] > 1]
    df_tarifa_factusol = df_tarifa_factusol[df_tarifa_factusol['Desviacion con la media'] <= 1]
    df_tarifa_factusol_alerta_cambio.to_excel('salida_excel/brp_tarifa_factusol_revisar_incremento.xlsx')
    df_tarifa_factusol.to_excel('salida_excel/brp_tarifa_factusol.xlsx')

#Revisar la parte web
    # Unión de las tarifa contra la web y el stock
    df_tarifa_stock_w = pd.merge(left=tarifa, right=inventario, how='left', left_on='Material_No',right_on='Cod_factusol')
    df_tarifa_stock_w = pd.merge(left=df_tarifa_stock_w, right=brp_web, how='left', left_on='Material_No', right_on='cod')

    df_tarifa_stock_w = df_tarifa_stock_w [
        ['Material_No', 'Retail_Price', 'Dealer_Price', 'Subtitude_Part', 'Qty_For_UOM', 'Act_Code','Price_Cat_Desc','id_product', 'price',
         'reference', 'cod', 'Cod_factusol', 'Stock_Factusol', 'Id_Familia_Descuento', 'Descuento']]
    #tarifa_general.to_excel('salida_excel/brp_tarifa_general.xlsx')

    '''Cambio de precios de la web
        1. Extraer sustituciones.
        2. Comprobar que Retail - Dealer > 0
        3. ¿Qué hacemos con OBS?
    '''
    #Referencias obsoletas
    df_si_tarifa_no_web = df_tarifa_stock_w[df_tarifa_stock_w['id_product'].isna()]
    df_si_tarifa_no_web.to_excel('salida_excel/brp_si_tar_no_web.xlsx')
    df_si_web_no_tarifa= df_tarifa_stock_w[df_tarifa_stock_w['Material_No'].isna()]
    df_si_web_no_tarifa.to_excel('salida_excel/brp_si_web_no_tarifa.xlsx')

    df_tarifa_stock_w=df_tarifa_stock_w[df_tarifa_stock_w['id_product'].notna()]
    df_tarifa_sust_w = df_tarifa_stock_w[df_tarifa_stock_w['Subtitude_Part'].notna()]
    df_tarifa_sust_w = pd.merge(left=df_tarifa_sust_w, right=tarifa, how='left', left_on='Subtitude_Part', right_on='Material_No')
    df_tarifa_sust_w.to_excel('salida_excel/brp_sust_w.xlsx')

    df_tarifa_stock_w = df_tarifa_stock_w[df_tarifa_stock_w['Subtitude_Part'].isna()]
    df_tarifa_stock_w['dif'] = df_tarifa_stock_w['Retail_Price'] - df_tarifa_stock_w['Dealer_Price']
    df_tarifa_stock_w['Change_price'] = df_tarifa_stock_w['Retail_Price'] - df_tarifa_stock_w['price']
    df_tarifa_obs_w = df_tarifa_stock_w[df_tarifa_stock_w['Act_Code']=='OBS']
    df_tarifa_obs_stock_w = df_tarifa_obs_w[df_tarifa_obs_w['Stock_Factusol'].notna()]
    df_tarifa_obs_w = df_tarifa_obs_w[df_tarifa_obs_w['Stock_Factusol'].isna()]
    df_tarifa_obs_stock_w.to_excel('salida_excel/brp_web_obs_con_stock.xlsx')
    df_tarifa_obs_w.to_excel('salida_excel/brp_web_obs.xlsx')

    df_tarifa_stock_w=df_tarifa_stock_w[df_tarifa_stock_w['dif'] != 0]
    df_change_price_w = df_tarifa_stock_w[df_tarifa_stock_w['Change_price'] != 0]
    df_change_price_w.to_excel('salida_excel/brp_cambio_precio_web.xlsx')



    return devuelve
if __name__ == '__main__':
    inicio_tarifa_brp('SSVDlrEuropeEUROAllXLS.xls','AtvDlrEuropeEUROAllXLS.xls','Inventario.XLSX')
