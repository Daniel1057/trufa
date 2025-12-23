from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys
import main
import Alim_bbdd_sah
import prestaweb



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
            Descuento = 20
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
    update_web = False
    export_excel = True
    inventario = True
    if(fichero_inventario==None):
        inventario = False
    else:
        inventario = True

    brp_web = Alim_bbdd_sah.table_to_df('SELECT * FROM v_brp_product')
    brp_web['cod'] = brp_web['reference'].str.replace('.', '',regex=True)
    tarifa = pd.read_excel(fichero1)
    tarifa['Material_No'] = tarifa['Material_No'].str.strip()
    tarifa2 = pd.read_excel(fichero2)
    tarifa2['Material_No'] = tarifa2['Material_No'].str.strip()
    tarifa = pd.concat([tarifa,tarifa2], ignore_index=True)
    total = tarifa.size
    tarifa = tarifa.drop_duplicates()
    tarifa['Material_No'] = tarifa['Material_No'].astype("string")
    tarifa['Material_No'] = tarifa['Material_No'].str.replace(' ','',regex=True)
    tarifa['Material_No'] = tarifa['Material_No'].str.replace('.', '',regex=True)
    neto = tarifa.size
    duplicados = total - neto
    devuelve = [total,duplicados,neto]
    if (inventario):
        inventario = pd.DataFrame()
        hojas = pd.ExcelFile(fichero_inventario).sheet_names
        for hoja in hojas:
            temporal = pd.read_excel(fichero_inventario, hoja)
            inventario = inventario.append(temporal.values.tolist(), ignore_index=True)
        inventario = inventario.rename(
        columns={0: "Cod_factusol", 1: "Desc_factusol", 2: "Ref_Prov_Factusol", 3: "Porv_factusol", 4: "Costo_Factusol",
                 5: "PVP_Factusol", 6: "Stock_Factusol", 7: "Obs_Factusol"})

        error_ref_sin_descripcion = inventario[inventario["Desc_factusol"] == 'SIN DESCRIPCIÓN']
        #Materiales dados de alta en factusol pero que no tienen descripción
        if(export_excel):
            error_ref_sin_descripcion.to_excel('salida_excel/error_sin_descripcion_factu.xlsx')

        inventario = inventario[inventario["Desc_factusol"] != 'SIN DESCRIPCIÓN']

    else:
        inventario = pd.DataFrame(
            columns=["Cod_factusol", "Desc_factusol", "Ref_Prov_Factusol", "Porv_factusol", "Costo_Factusol",
                     "PVP_Factusol", "Stock_Factusol", "Obs_Factusol"])

    # Calculo del margen y del descuentos
    tarifa['Margen'] = round((tarifa['Retail_Price'] - tarifa['Dealer_Price']) / tarifa['Retail_Price'], 2)
    tarifa = familia_descuento(tarifa)
    tarifa_taller = tarifa
    tarifa_taller = tarifa_taller[['Material_No','Part_Desc','Act_Code','Retail_Price','Descuento','Subtitude_Part','Price_Cat_Desc']]
    tarifa_taller = tarifa_taller.rename(columns={'Material_No': 'Referencia','Part_Desc':'Descripción','Act_Code':'Estado','Retail_Price':'PVP+IVA','Subtitude_Part':'Sustitución','Price_Cat_Desc':'Categoría Artículo'})
    #tarifa_taller= tarifa_taller[tarifa_taller['Retail_Price']!='0']

    #Generamos fichero para las tarifas de talleres
    tarifa_taller .to_excel('salida_excel/brp_excel_precios_taller.xlsx')

    #Genera la tarifa de Factusol
    print(inventario)
    if(len(inventario)>0):
        df_tarifa_factusol = pd.merge(left=tarifa, right=inventario, how='inner', left_on='Material_No', right_on='Cod_factusol')
        df_tarifa_factusol = df_tarifa_factusol[['Cod_factusol','Stock_Factusol','Retail_Price','Dealer_Price','Act_Code','Subtitude_Part','Price_Cat_Desc','Margen','Descuento','Id_Familia_Descuento']]

        #Cambios de referencia
        df_tarifa_factusol_sustituciones = df_tarifa_factusol[df_tarifa_factusol['Subtitude_Part'].notna()]
        if (export_excel):
            df_tarifa_factusol_sustituciones.to_excel('salida_excel/brp_factusol_sustituciones.xlsx')

        df_tarifa_factusol=df_tarifa_factusol[df_tarifa_factusol['Subtitude_Part'].isna()]

        #Errores precio de coste = vta
        df_error_sin_margen = df_tarifa_factusol[df_tarifa_factusol['Retail_Price'] == df_tarifa_factusol['Dealer_Price']]
        if (export_excel):
            df_error_sin_margen.to_excel('salida_excel/brp_factusol_sin_margen.xlsx')
        df_tarifa_factusol = df_tarifa_factusol[df_tarifa_factusol['Retail_Price'] != df_tarifa_factusol['Dealer_Price']]

        #Detectar referencias obsoletas
        df_tarifa_factu_descatalogados = df_tarifa_factusol[df_tarifa_factusol['Act_Code'] == 'OBS']
        df_tarifa_factusol=df_tarifa_factusol[df_tarifa_factusol['Act_Code'] != 'OBS']

        #Referencias obsoletas que existe stock
        df_tarifa_factu_descatalogados_stock = df_tarifa_factu_descatalogados[df_tarifa_factu_descatalogados['Stock_Factusol'] > 0]
        if (export_excel):
            df_tarifa_factu_descatalogados_stock.to_excel('salida_excel/brp_tarifa_factu_descatalogados_stock.xlsx')

        #Referencias obsoletas que no tenemos stock
        df_tarifa_factu_descatalogados = df_tarifa_factu_descatalogados[df_tarifa_factu_descatalogados['Stock_Factusol'].isna()]
        if (export_excel):
            df_tarifa_factu_descatalogados.to_excel('salida_excel/brp_tarifa_factu_descatalogados.xlsx')

        df_tarifa_factu_ropa = df_tarifa_factusol[df_tarifa_factusol['Price_Cat_Desc'] == 'W - Clothing']
        df_tarifa_factu_ropa_stock = df_tarifa_factu_ropa[df_tarifa_factu_ropa['Stock_Factusol'] > 0]
        df_tarifa_factu_ropa_sin_stock = df_tarifa_factu_ropa[df_tarifa_factu_ropa['Stock_Factusol'].isna()]
        if (export_excel):
            df_tarifa_factusol.to_excel('salida_excel/brp_tarifa_factusol.xlsx')

#Revisar la parte web
    # Unión de las tarifa contra la web y el stock
    df_tarifa_stock_w = pd.merge(left=tarifa, right=inventario, how='left', left_on='Material_No',right_on='Cod_factusol')
    df_tarifa_stock_w = pd.merge(left=df_tarifa_stock_w, right=brp_web, how='left', left_on='Material_No', right_on='reference')
    if(len(df_tarifa_stock_w)>0):
        df_tarifa_stock_w = df_tarifa_stock_w [
            ['Material_No', 'Retail_Price', 'Dealer_Price', 'Subtitude_Part', 'Qty_For_UOM', 'Act_Code','Price_Cat_Desc','id_product', 'price',
            'reference', 'cod', 'Cod_factusol', 'Stock_Factusol', 'Id_Familia_Descuento', 'Descuento']]

    '''Cambio de precios de la web
        1. Extraer sustituciones.
        2. Comprobar que Retail - Dealer > 0
        3. ¿Qué hacemos con OBS?
    '''

    #Referencias que no existen en la web
    df_si_tarifa_no_web = df_tarifa_stock_w[df_tarifa_stock_w['id_product'].isna()]
    if (export_excel):
        df_si_tarifa_no_web.to_excel('salida_excel/brp_si_tar_no_web.xlsx')

    #Referencias existentes en la web pero no en la tarifa
    df_si_web_no_tarifa= df_tarifa_stock_w[df_tarifa_stock_w['Material_No'].isna()]
    if (export_excel):
        df_si_web_no_tarifa.to_excel('salida_excel/brp_si_web_no_tarifa.xlsx')

    #Existe en la web y en la tarifa
    df_tarifa_stock_w=df_tarifa_stock_w[df_tarifa_stock_w['id_product'].notna()]

    #Existe en la web y son sustituciones - Buscamos las nuevas referencias
    df_tarifa_sust_w = df_tarifa_stock_w[df_tarifa_stock_w['Subtitude_Part'].notna()]
    df_tarifa_sust_w = pd.merge(left=df_tarifa_sust_w, right=tarifa, how='left', left_on='Subtitude_Part', right_on='Material_No')
    if (export_excel):
        df_tarifa_sust_w.to_excel('salida_excel/brp_sust_w.xlsx')
    df_tarifa_sust_w = df_tarifa_sust_w[['id_product', 'Material_No_y', 'Part_Desc', 'Retail_Price_y']]
    df_tarifa_sust_w = df_tarifa_sust_w[['id_product', 'Material_No_y', 'Part_Desc_x', 'Retail_Price_y']]

    df_tarifa_sust_w['id_product'] = df_tarifa_sust_w['id_product'].astype(int)

    #Existe en la web y no hay sustituciones
    df_tarifa_stock_w = df_tarifa_stock_w[df_tarifa_stock_w['Subtitude_Part'].isna()]

    #Seleccionamos las referencias que han cambiado de precio
    df_tarifa_stock_w['dif'] = df_tarifa_stock_w['Retail_Price'] - df_tarifa_stock_w['Dealer_Price']
    df_tarifa_stock_w['Change_price'] = df_tarifa_stock_w['Retail_Price'] - df_tarifa_stock_w['price']

    #Existen referencias obsoletas en la web
    df_tarifa_obs_w = df_tarifa_stock_w[df_tarifa_stock_w['Act_Code']=='OBS']

    #Obsoletas con stock
    df_tarifa_obs_stock_w = df_tarifa_obs_w[df_tarifa_obs_w['Stock_Factusol'].notna()]

    #Obsoletas sin stock
    df_tarifa_obs_w = df_tarifa_obs_w[df_tarifa_obs_w['Stock_Factusol'].isna()]

    #Referencias de la web que realmente cambia el precio
    df_tarifa_stock_w=df_tarifa_stock_w[df_tarifa_stock_w['dif'] != 0]
    df_change_price_w = df_tarifa_stock_w[df_tarifa_stock_w['Change_price'] != 0]
    if (export_excel):
        df_change_price_w.to_excel('salida_excel/brp_cambio_precio_web.xlsx')
    df_bbdd_preu = df_change_price_w
    df_bbdd_preu = df_bbdd_preu[['id_product', 'Retail_Price', ]]
    df_bbdd_preu['id_product']=df_bbdd_preu['id_product'].astype(int)
    if(update_web):
        Alim_bbdd_sah.sql_minemas_e('Truncate table cambio_obsoletos')
        Alim_bbdd_sah.sql_minemas_e('Truncate table Cambio_preu_brp')
        if (len(df_tarifa_sust_w)>0):
            Alim_bbdd_sah.carga_tarifa_bbdd_e(df_tarifa_sust_w, 'cambio_obsoletos')
            Alim_bbdd_sah.sql_minemas_e('update cambio_obsoletos a, ps_product b set b.reference = a.Material_No_y where a.id_product = b.id_product')
            Alim_bbdd_sah.sql_minemas_e('update cambio_obsoletos a, ps_product b set b.price = a.Retail_Price_y where a.id_product = b.id_product')
            Alim_bbdd_sah.sql_minemas_e('update cambio_obsoletos a, ps_product_shop b set b.price = a.Retail_Price_y where a.id_product = b.id_product')
            Alim_bbdd_sah.sql_minemas_e("update cambio_obsoletos a, ps_product_lang b set b.description=replace(b.description,'. Se vende',concat('-',a.Material_No_y,'. Se vende')) where a.id_product = b.id_product")
        if(len(df_bbdd_preu)>0):
            Alim_bbdd_sah.carga_tarifa_bbdd_e(df_bbdd_preu,'Cambio_preu_brp')
            Alim_bbdd_sah.sql_minemas_e('update nuevaendurorecambios.ps_product a , nuevaendurorecambios.Cambio_preu_brp b set a.price = b.Retail_Price where a.id_product = b.id_product;')
            Alim_bbdd_sah.sql_minemas_e('update nuevaendurorecambios.ps_product_shop a , nuevaendurorecambios.Cambio_preu_brp b set a.price = b.Retail_Price where a.id_product = b.id_product;')
        Alim_bbdd_sah.sql_minemas_e('update ps_product set price = 0.4 where price between 0.01 and 0.38;')
        Alim_bbdd_sah.sql_minemas_e('update ps_product_shop set price = 0.4 where price between 0.01 and 0.38;')
        Alim_bbdd_sah.sql_minemas_e('update ps_product_shop set available_for_order = 0 where price = 0')
        Alim_bbdd_sah.sql_minemas_e('update ps_product set available_for_order = 0 where price = 0')
    if(False):
        df_change_price_w = df_change_price_w[['id_product','Retail_Price']]
        df_change_price_w = df_change_price_w.rename(columns={'Retail_Price':'Preu'})
        df_change_price_w['id_product'] = df_change_price_w['id_product'].astype(int)
        prestaweb.change_price_x_id_product(df_change_price_w)
    return devuelve
if __name__ == '__main__':
    inicio_tarifa_brp('SSVDlrEuropeEUROAllXLS.xls','AtvDlrEuropeEUROAllXLS.xls','Listado de artículos.XLSX')
