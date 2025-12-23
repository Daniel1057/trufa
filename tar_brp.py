from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys
import main
import Alim_bbdd_sah
import prestaweb



def familia_descuento(df):
    df['Id_Familia_Descuento'] = 5
    df['Descuento_profesional'] = 0
    df['Descuento_clte_premium'] = 0
    df['Descuento_profesional_especial'] = 0
    df['Descuento_coste'] = 0
    for i in df.index:
        Margen = df['Margen'][i]
        print (i)
        print (Margen)
        Id_Familia_Descuento = 5
        Descuento_profesional = 0
        Descuento_clte_premium = 0
        Descuento_profesional_especial = 0
        Descuento_coste = 0
        if (Margen >= 0.09 and Margen < 0.14):
            Id_Familia_Descuento = 10
            Descuento_coste = 0
            Descuento_profesional_especial = 0
            Descuento_clte_premium = 0
            Descuento_profesional = 0
        if (Margen >= 0.14 and Margen < 0.19):
            Id_Familia_Descuento = 15
            Descuento_coste = 10
            Descuento_profesional_especial = 5
            Descuento_clte_premium = 0
            Descuento_profesional = 0
        if (Margen >= 0.19 and Margen < 0.24):
            Id_Familia_Descuento = 20
            Descuento_coste = 15
            Descuento_profesional_especial = 10
            Descuento_clte_premium = 0
            Descuento_profesional = 5
        if (Margen >= 0.24 and Margen < 0.29):
            Id_Familia_Descuento = 25
            Descuento_coste = 20
            Descuento_clte_premium = 5
            Descuento_profesional = 10
            Descuento_profesional_especial = 15
        if (Margen >= 0.29 and Margen < 0.34):
            Id_Familia_Descuento = 30
            Descuento_coste = 25
            Descuento_clte_premium = 5
            Descuento_profesional = 15
            Descuento_profesional_especial = 20
        if (Margen >= 0.34 and Margen < 0.39):
            Id_Familia_Descuento = 35
            Descuento_coste = 30
            Descuento_clte_premium = 10
            Descuento_profesional = 20
            Descuento_profesional_especial = 25
        if (Margen >= 0.39 and Margen < 0.44):
            Id_Familia_Descuento = 40
            Descuento_coste = 35
            Descuento_clte_premium = 10
            Descuento_profesional = 20
            Descuento_profesional_especial = 25
        if (Margen >= 0.44 and Margen < 0.48):
            Id_Familia_Descuento = 45
            Descuento_coste = 40
            Descuento_clte_premium = 15
            Descuento_profesional = 25
            Descuento_profesional_especial = 35
        if (Margen >= 0.48 and Margen < 0.54):
            Id_Familia_Descuento = 50
            Descuento_coste = 45
            Descuento_clte_premium = 20
            Descuento_profesional = 30
            Descuento_profesional_especial = 40
        if (Margen >= 0.54 and Margen < 0.59):
            Id_Familia_Descuento = 55
            Descuento_coste = 50
            Descuento_clte_premium = 20
            Descuento_profesional = 30
            Descuento_profesional_especial = 40
        if (Margen >= 0.59 ):
            Id_Familia_Descuento = 60
            Descuento_coste = 55
            Descuento_clte_premium = 30
            Descuento_profesional = 40
            Descuento_profesional_especial = 40
        df.at[i,'Id_Familia_Descuento'] = Id_Familia_Descuento
        df.at[i,'Descuento_coste'] = Descuento_coste
        df.at[i, 'Descuento_clte_premium'] = Descuento_clte_premium
        df.at[i, 'Descuento_profesional'] = Descuento_profesional
        df.at[i, 'Descuento_profesional_especial'] = Descuento_profesional_especial
    return df

def sustituciones(df):
    df_sustituir = pd.DataFrame(columns=['Referencia','Ref_Ultima','Name'])

    for i in df.index:
        v_material = df['Material_No'][i]
        v_sustitute = df['Subtitude_Part'][i]
        v_name = str(v_material)+' - '+str(v_sustitute)
        while (len(df[df['Material_No']==v_sustitute])>0):
            sust = df[df['Material_No']==v_sustitute]
            for x in sust.index:
                v_sustitute = df['Subtitude_Part'][x]
                v_name = v_name+' - '+str(v_sustitute)
        lista = {'Referencia':[v_material],'Ref_Ultima':[v_sustitute],'Name':[v_name]}
        df_lista = pd.DataFrame(data=lista, columns=['Referencia', 'Ref_Ultima', 'Name'])
        df_sustituir=pd.concat([df_sustituir,df_lista],ignore_index=True)
    return (df_sustituir)

def update_sustituciones(df_sustitucion, df_web):
    df_update = pd.merge(left=df_sustitucion, right=df_web, how='inner', left_on='Referencia', right_on='reference')
    if(len(df_update)>0):
        df_update.drop(['id_manufacturer','show_price', 'state','price', 'cod'],axis= 1,inplace=True)
        Alim_bbdd_sah.carga_tarifa_bbdd_e(df_update,'Alim_change_reference')
        v_sql = """SELECT a.id_product,replace(b.name,a.Referencia, Ref_Ultima) as name,replace(b.description,a.Referencia, a.name) FROM nuevaendurorecambios.Alim_change_reference a, ps_product_lang b where a.id_product = b.id_product;"""
        Alim_bbdd_sah.table_to_df_e(v_sql).to_excel('BRP_cambio_referencias.xlsx')
        v_update_refeerence = """update nuevaendurorecambios.Alim_change_reference a, ps_product b SET b.reference = a.Ref_Ultima  where a.id_product = b.id_product"""
        v_update_name = """update nuevaendurorecambios.Alim_change_reference a, ps_product_lang b SET b.name = replace(b.name,a.Referencia, Ref_Ultima)  where a.id_product = b.id_product"""
        v_update_description = """update nuevaendurorecambios.Alim_change_reference a, ps_product_lang b set b.description =  replace(b.description,a.Referencia, a.name)  where a.id_product = b.id_product"""
        Alim_bbdd_sah.sql_minemas_e(v_update_refeerence)
        Alim_bbdd_sah.sql_minemas_e(v_update_name)
        Alim_bbdd_sah.sql_minemas_e(v_update_description)


def inicio_tarifa_brp(fichero1,fichero2,fichero_inventario):
    update_web = True
    export_excel = True
    if(fichero_inventario==None):
        inventario = False
    else:
        inventario = True
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
    tarifa_sustitucion = tarifa[tarifa['Subtitude_Part'].notna()].copy()
    tarifa_sustitucion.drop(
        ['Part_Desc', 'Last_Yr_Util', 'MOQ', 'Act_Code', 'Retail_Price', 'Dealer_Price', 'Dist_Price', 'Blank',
         'Qty_Assembly', 'UOM_Base_Price', 'UOM_Sale_Price', 'Qty_For_UOM', 'Price_Cat_Desc'], axis=1, inplace=True)
    df_sust =sustituciones(tarifa_sustitucion)
    brp_web = Alim_bbdd_sah.table_to_df('SELECT * FROM v_brp_product')
    brp_web['cod'] = brp_web['reference'].str.replace('.', '',regex=True)
    if (update_web):
        update_sustituciones(df_sust, brp_web)

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

    #Genera Excels con los descuentos
    tarifa_taller = tarifa
    tarifa_taller = tarifa_taller.rename(columns={'Material_No': 'Referencia','Part_Desc':'Descripción','Act_Code':'Estado','Retail_Price':'PVP+IVA','Subtitude_Part':'Sustitución','Price_Cat_Desc':'Categoría Artículo'})
    #tarifa_taller= tarifa_taller[tarifa_taller['Retail_Price']!='0']
    tarifa_taller[['Referencia', 'Descripción', 'Estado', 'PVP+IVA', 'Descuento_coste','Sustitución', 'Categoría Artículo']].to_excel('salida_excel/brp_excel_precios_descuento_coste.xlsx')
    tarifa_taller[['Referencia', 'Descripción', 'Estado', 'PVP+IVA', 'Descuento_clte_premium', 'Sustitución',
                   'Categoría Artículo']].to_excel('salida_excel/brp_excel_precios_Descuento_clte_premium.xlsx')
    tarifa_taller[['Referencia', 'Descripción', 'Estado', 'PVP+IVA', 'Descuento_profesional', 'Sustitución',
                   'Categoría Artículo']].to_excel('salida_excel/brp_excel_precios_Descuento_profesional.xlsx')
    tarifa_taller[['Referencia', 'Descripción', 'Estado', 'PVP+IVA', 'Descuento_profesional_especial', 'Sustitución',
                   'Categoría Artículo']].to_excel('salida_excel/brp_excel_precios_Descuento_profesional_especial.xlsx')


    #Genera la tarifa de Factusol
    print(inventario)
    if(len(inventario)>0):
        #Tarifa cambio de precios
        df_tarifa_factusol = pd.merge(left=tarifa, right=inventario, how='inner', left_on='Material_No', right_on='Cod_factusol').copy()
        df_tarifa_factusol_1 = df_tarifa_factusol.copy()
        df_tarifa_factusol_1['Coste'] = df_tarifa_factusol_1['Dealer_Price']
        df_tarifa_factusol_1 ['Familia Descuento'] = df_tarifa_factusol_1['Margen']*100
        df_tarifa_factusol_1['Precio Venta sin impuestos'] = df_tarifa_factusol_1['Retail_Price']
        df_tarifa_factusol_1 = df_tarifa_factusol_1[['Cod_factusol', 'Desc_factusol', 'Precio Venta sin impuestos', 'Coste', 'Familia Descuento']]
        df_tarifa_factusol_1.to_excel('salida_excel/brp_factusol.xlsx',sheet_name='Fichero Factusol',index=False)

        #Productos Obsoletos
        df_tarifa_obs = df_tarifa_factusol[df_tarifa_factusol['Act_Code'] == 'OBS'].copy()
        df_tarifa_obs[df_tarifa_obs['Stock_Factusol'].isna()].to_excel('salida_excel/brp_osboleto_sin_stock_factusol.xlsx')
        df_tarifa_obs[df_tarifa_obs['Stock_Factusol'].notna()].to_excel('salida_excel/brp_osboleto_con_stock_factusol.xlsx')
        df_tarifa_factusol[['Cod_factusol','Stock_Factusol','Retail_Price','Dealer_Price','Act_Code','Subtitude_Part','Price_Cat_Desc','Margen','Id_Familia_Descuento']].to_excel('salida_excel/brp_obsoletos_factusol.xlsx')
        #Cambio de referencias
        pd.merge(left=df_sust, right=inventario, how='inner', left_on='Referencia', right_on='Cod_factusol').to_excel('salida_excel/brp_cambio_referencia_factusol.xlsx')


#Revisar la parte web
    # Unión de las tarifa contra la web y el stock
    df_tarifa_stock_w = pd.merge(left=tarifa, right=brp_web, how='left', left_on='Material_No', right_on='reference')

    #Referencias existentes en la web pero no en la tarifa
    df_tarifa_stock_w[df_tarifa_stock_w['Material_No'].isna()].to_excel('salida_excel/brp_si_web_no_tarifa.xlsx')

    # Referencias existentes en la tarifa pero no en la web
    df_tarifa_stock_w[df_tarifa_stock_w['id_product'].isna()].to_excel('salida_excel/brp_si_tarifa_no_web.xlsx')


    #Existe en la web y en la tarifa
    df_tarifa_stock_w.dropna(subset=['id_product'],inplace=True)

    #Seleccionamos las referencias que han cambiado de precio
    df_tarifa_stock_w['dif'] = df_tarifa_stock_w['Retail_Price'] - df_tarifa_stock_w['Dealer_Price']
    df_tarifa_stock_w['Change_price'] = df_tarifa_stock_w['Retail_Price'] - df_tarifa_stock_w['price']

    #Referencias de la web que realmente cambia el precio
    df_tarifa_stock_w=df_tarifa_stock_w[df_tarifa_stock_w['dif'] != 0]
    df_change_price_w = df_tarifa_stock_w[df_tarifa_stock_w['Change_price'] != 0]
    df_change_price_w.to_excel('salida_excel/brp_cambio_precio_web.xlsx')
    df_bbdd_preu = df_change_price_w
    df_bbdd_preu = df_bbdd_preu[['id_product', 'Retail_Price', ]]
    df_bbdd_preu['id_product']=df_bbdd_preu['id_product'].astype(int)
    if(update_web):

        Alim_bbdd_sah.sql_minemas_e('Truncate table Cambio_preu_brp')
        if(len(df_bbdd_preu)>0):
            Alim_bbdd_sah.carga_tarifa_bbdd_e(df_bbdd_preu,'Cambio_preu_brp')
            Alim_bbdd_sah.sql_minemas_e('update nuevaendurorecambios.ps_product a , nuevaendurorecambios.Cambio_preu_brp b set a.price = b.Retail_Price where a.id_product = b.id_product;')
            Alim_bbdd_sah.sql_minemas_e('update nuevaendurorecambios.ps_product_shop a , nuevaendurorecambios.Cambio_preu_brp b set a.price = b.Retail_Price where a.id_product = b.id_product;')
        Alim_bbdd_sah.sql_minemas_e('update ps_product set price = 0.4 where price between 0.01 and 0.38;')
        Alim_bbdd_sah.sql_minemas_e('update ps_product_shop set price = 0.4 where price between 0.01 and 0.38;')
        #Alim_bbdd_sah.sql_minemas_e('update ps_product_shop set available_for_order = 0 where price = 0')
        #Alim_bbdd_sah.sql_minemas_e('update ps_product set available_for_order = 0 where price = 0')
    return devuelve
if __name__ == '__main__':
    inicio_tarifa_brp('SSVDlrEuropeEUROAllXLS.xls','AtvDlrEuropeEUROAllXLS.xls',None)
