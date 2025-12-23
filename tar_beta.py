from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys
import Alim_bbdd_sah
import prestaweb
from ftplib import FTP

update_web = True

def fpt_beta(direccion,user,passwd):
    with FTP(direccion, user, passwd) as ftp:
        print(ftp.dir())
        filename = "products.csv"
        with open(filename, "wb") as file:
            ftp.retrbinary(f"RETR {filename}", file.write)
    ftp.close()
    fichero_csv(filename)

def fichero_csv(filename):
    fichero = filename+'_limpio'
    with open(fichero, 'w') as f:
        with open(filename, "r") as fichero:
            for linea in fichero:
                if(linea[0:1].isalnum()):
                    f.write(linea)
    f.close()
    fichero.close()
    df_csv(fichero)

def df_csv(fichero):
    df_csv = pd.read_csv(fichero,on_bad_lines='warn',sep=';')
    df_csv = df_csv[['IdProducto', 'Combinaciones', 'Cantidad', 'Precio distribuidor ']]
    df_csv  = df_csv.rename(columns= {'IdProducto':'Descripcion', 'Combinaciones':'Article', 'Cantidad':'Preu', 'Precio distribuidor ':'Descuento'})
    df_csv['cod']=df_csv['Article'].str.replace('.','', regex=True)
    df_csv['Num'] = df_csv['Preu'].str.replace('.','', regex=True)
    df_csv['Num'] = df_csv['Num'].str.isdigit()
    df_csv = df_csv[df_csv['Num']==True]
    #7949
    df_csv['Preu'] = df_csv['Preu'].astype(float)
    generar_dataframes(None,'Inventario.XLSX',df_csv)
    print (df_csv)

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
    Alim_bbdd_sah.carga_tarifa_bbdd(df, 'descuentos_beta')
    return df

def change_ref(df_sust):
    df_sustituir = pd.DataFrame(columns=['Referencia', 'Ref_Ultima', 'Name'])
    df_sust['sust'] = df_sust['Descripcion'].str.find('#')
    df = df_sust[df_sust['sust'] == 0].copy()
    if (len(df['sust']>0)):
        df['Descripcion']=df['Descripcion'].str.replace('#', '')
        df=df[df['Descripcion'] != '']
    for i in df.index:
        v_material = df['Article'][i]
        v_sustitute = df['Descripcion'][i]
        v_name = str(v_material)+' - '+str(v_sustitute)
        while (len(df[df['Article']==v_sustitute])>0):
            sust = df[df['Article']==v_sustitute]
            for x in sust.index:
                v_sustitute = df['Descripcion'][x]
                v_name = v_name+' - '+str(v_sustitute)
        lista = {'Referencia':[v_material],'Ref_Ultima':[v_sustitute],'Name':[v_name]}
        df_lista = pd.DataFrame(data=lista, columns=['Referencia', 'Ref_Ultima', 'Name'])
        df_sustituir=pd.concat([df_sustituir,df_lista],ignore_index=True)
    return (df_sustituir)

def update_sustituciones(df_sustitucion, df_web):
    df_update = pd.merge(left=df_sustitucion, right=df_web, how='inner', left_on='Referencia', right_on='reference')
    if(len(df_update)>0):
        if(update_web):
            Alim_bbdd_sah.carga_tarifa_bbdd_e(df_update,'Alim_change_reference')
            v_sql = """SELECT a.id_product,replace(b.name,a.Referencia, Ref_Ultima) as name,replace(b.description,a.Referencia, a.name) FROM nuevaendurorecambios.Alim_change_reference a, ps_product_lang b where a.id_product = b.id_product;"""
            Alim_bbdd_sah.table_to_df_e(v_sql).to_excel('Beta_cambio_referencias.xlsx')
            v_update_refeerence = """update nuevaendurorecambios.Alim_change_reference a, ps_product b SET b.reference = a.Ref_Ultima  where a.id_product = b.id_product"""
            v_update_name = """update nuevaendurorecambios.Alim_change_reference a, ps_product_lang b SET b.name = replace(b.name,a.Referencia, Ref_Ultima)  where a.id_product = b.id_product"""
            v_update_description = """update nuevaendurorecambios.Alim_change_reference a, ps_product_lang b set b.description =  replace(b.description,a.Referencia, a.name)  where a.id_product = b.id_product"""
            Alim_bbdd_sah.sql_minemas_e(v_update_refeerence)
            Alim_bbdd_sah.sql_minemas_e(v_update_name)
            Alim_bbdd_sah.sql_minemas_e(v_update_description)


def generar_dataframes(fichero_tarifa,fichero_inventario,df_csv):
    update_web = False
    if (fichero_inventario==None):
        Cargar_inventario = False
    else:
        Cargar_inventario = True

    #Carga df de la web
    beta_web = Alim_bbdd_sah.table_to_df('SELECT * FROM v_beta_product')
    beta_web['cod'] = beta_web['reference'].str.replace('.', '',regex=True)

    if (fichero_inventario):
        #Carga el inventario de factusol
        inventario = pd.DataFrame()
        hojas = pd.ExcelFile(fichero_inventario).sheet_names
        for hoja in hojas:
            temporal = pd.read_excel(fichero_inventario,hoja)
            inventario = inventario.append(temporal.values.tolist(),ignore_index = True)
        inventario = inventario.rename(
            columns={0: "Cod_factusol", 1: "Desc_factusol", 2: "Ref_Prov_Factusol", 3: "Porv_factusol", 4: "Costo_Factusol",
                     5: "PVP_Factusol", 6: "Stock_Factusol", 7: "Obs_Factusol"})

        #Nueva columna cod eliminando los puntos
        inventario['cod'] = inventario['Cod_factusol'].str.replace('.', '', regex=True)
    else:
        inventario = pd.DataFrame(columns=["cod","Cod_factusol","Desc_factusol","Ref_Prov_Factusol","Porv_factusol","Costo_Factusol","PVP_Factusol","Stock_Factusol","Obs_Factusol"])

    #Carga la tarifa de Beta
    if (fichero_tarifa!=None):
        tarifa = pd.read_excel(fichero_tarifa)

    else:
        tarifa = df_csv.copy(deep=True)

    # Elimina los puntos del código para poder comparar tanto con prestashop como con factusol
    tarifa['cod'] = tarifa['Article'].str.replace('.', '', regex=True)
    tarifa['Margen'] = round(tarifa['Descuento'] / 100, 2)
    tarifa['Coste'] = tarifa['Preu'] - (tarifa['Preu'] * tarifa['Margen'])
    tarifa = familia_descuento(tarifa)

    #Generamos ficheros taller
    tarifa_taller = tarifa.copy()
    tarifa_taller = tarifa_taller.rename(columns={'Article': 'Referencia','Descripcion':'Descripción','Preu':'PVP+IVA','FAMI':'Categoría Artículo'})

    #tarifa_taller= tarifa_taller[tarifa_taller['Retail_Price']!='0']
    tarifa_taller[['Referencia', 'Descripción', 'PVP+IVA', 'Descuento_coste', 'Categoría Artículo']].to_excel('salida_excel/beta_excel_precios_descuento_coste.xlsx')
    tarifa_taller[['Referencia', 'Descripción',  'PVP+IVA', 'Descuento_clte_premium','Categoría Artículo']].to_excel('salida_excel/beta_excel_precios_Descuento_clte_premium.xlsx')
    tarifa_taller[['Referencia', 'Descripción',  'PVP+IVA', 'Descuento_profesional','Categoría Artículo']].to_excel('salida_excel/beta_excel_precios_Descuento_profesional.xlsx')
    tarifa_taller[['Referencia', 'Descripción',  'PVP+IVA', 'Descuento_profesional_especial','Categoría Artículo']].to_excel('salida_excel/beta_excel_precios_Descuento_profesional_especial.xlsx')


    #Referencias sustituciones
    df_sust = change_ref(tarifa)
    if (update_web):
        update_sustituciones(df_sust, beta_web)
        beta_web = Alim_bbdd_sah.table_to_df('SELECT * FROM v_beta_product')
        beta_web['cod'] = beta_web['reference'].str.replace('.', '', regex=True)

    #Copia del df de tarifa
    tarifa_aux = tarifa.copy(deep=True)


    #Une tarifa con la web y el inventario
    tarifa = pd.merge(left=tarifa, right=beta_web, how='left', left_on='cod', right_on='cod')
    tarifa= pd.merge(left=tarifa, right=inventario, how='left', left_on='cod', right_on='cod')

    #Referencias existentes en la tarifa pero no en la web
    beta_si_tarifa_no_web = tarifa[tarifa['id_product'].isna()]

    #Referencias no existentes en la web y que hay stock en factusol
    beta_si_tarifa_no_web_stock = beta_si_tarifa_no_web[beta_si_tarifa_no_web['Stock_Factusol'].notna()]
    beta_si_tarifa_no_web_stock.to_excel('salida_excel/beta_si_tarifa_no_web_stock.xlsx')
    beta_si_tarifa_no_web = beta_si_tarifa_no_web[beta_si_tarifa_no_web['Stock_Factusol'].isna()]
    beta_si_tarifa_no_web.to_excel('salida_excel/beta_si_tarifa_no_web.xlsx')

    # Referencias a sustituir que tienen stock en factusol
    if (len(df_sust)>0):
        df_sust['cod'] = df_sust['Referencia'].str.replace('.', '', regex=True)
        tarifa_sustitucion = pd.merge(left=df_sust, right=inventario, how='inner', left_on='cod', right_on='cod')
        tarifa_sustitucion[tarifa_sustitucion['Stock_Factusol'].notna()].to_excel('salida_excel/beta_ref_sust_stock.xlsx')
        # Referencias a sustituir que no tienen stock
        tarifa_sustitucion[tarifa_sustitucion['Stock_Factusol'].isna()].to_excel('salida_excel/beta_ref_sust.xlsx')

    tarifa_factusol = pd.merge(left=tarifa_aux, right=inventario, how='left', left_on='cod', right_on='cod')
    #Referencias obsoletas en la tarifa
    if (tarifa_factusol[tarifa_factusol['Descripcion'].str.contains('ARTICULO NO SUMINISTRABLE', na=False, regex=True)].size > 0):
        tarifa_no_vta = tarifa_factusol[tarifa_factusol['Descripcion'].str.contains('ARTICULO NO SUMINISTRABLE', na=False, regex=True)].copy()

        #Referencias obsoletas pero hay stock en factusol
        tarifa_no_vta[tarifa_no_vta['Stock_Factusol'].notna()].to_excel('salida_excel/beta_ref_no_vta_stock.xlsx')

        #Referencias obsoletas sin stock
        tarifa_no_vta[tarifa_no_vta['Stock_Factusol'].isna()].to_excel('salida_excel/beta_ref_no_vta.xlsx')

    #Referencias que no tienen precio de vta en la nueva tarifa
    if(tarifa_factusol[tarifa_factusol.Preu == 0].size>0):
        tarifa_precio0 = tarifa_factusol[tarifa_factusol.Preu == 0].copy()

        #Refrencias sin precio en la tarifa y que hay stock
        tarifa_precio0[tarifa_precio0['Stock_Factusol'].notna()].to_excel('salida_excel/beta_ref_preu0_stock.xlsx')

        #Referencias sin precio y que no hay stock
        tarifa_precio0[tarifa_precio0['Stock_Factusol'].isna()].to_excel('salida_excel/beta_ref_preu0_stock.xlsx')



    #Diferencias de precio tarifa vs web
    tarifa.drop(tarifa[tarifa.Preu == 0].index)
    tarifa['Dif_precio_web'] = tarifa['price'] - tarifa['Preu'].astype(float)

    #Exportación tarifa factusol
    tarifa_factusol.drop(tarifa_factusol[tarifa_factusol.Preu == 0].index)
    df_tarifa_factusol_1 = tarifa_factusol.copy()
    df_tarifa_factusol_1  = df_tarifa_factusol_1 [df_tarifa_factusol_1 ['Cod_factusol'].notna()]
    df_tarifa_factusol_1['Coste'] = df_tarifa_factusol_1['Coste']
    df_tarifa_factusol_1['Familia Descuento'] = df_tarifa_factusol_1['Margen'] * 100
    df_tarifa_factusol_1['Precio Venta sin impuestos'] = df_tarifa_factusol_1['Preu']
    df_tarifa_factusol_1 = df_tarifa_factusol_1[
        ['Cod_factusol', 'Desc_factusol', 'Precio Venta sin impuestos', 'Coste', 'Familia Descuento']]
    df_tarifa_factusol_1.to_excel('salida_excel/beta_cambios_precio_factusol.xlsx', sheet_name='Fichero Factusol', index=False)

    #Dataframe para con cambio de precios en la web
    tarifa_w =tarifa[tarifa['id_product'].notna()].copy()
    tarifa_w =tarifa_w[tarifa_w['Dif_precio_web']!=0]
    tarifa_w.to_excel('salida_excel/beta_cambios_precio_web.xlsx')
    if(update_web):
        if(len(tarifa_w)>0):
            Alim_bbdd_sah.carga_tarifa_bbdd_e(tarifa_w,'Cambio_preu_beta')
            print ('Actualizando ps_product')
            Alim_bbdd_sah.sql_minemas_e('update nuevaendurorecambios.ps_product a , nuevaendurorecambios.Cambio_preu_beta b set a.price = b.Preu where a.id_product = b.id_product;')
            print('Actualizando ps_product_shop')
            Alim_bbdd_sah.sql_minemas_e('update nuevaendurorecambios.ps_product_shop a , nuevaendurorecambios.Cambio_preu_beta b set a.price = b.Preu where a.id_product = b.id_product;')
        Alim_bbdd_sah.sql_minemas_e('update ps_product set price = 0.4 where price between 0.01 and 0.38;')
        Alim_bbdd_sah.sql_minemas_e('update ps_product_shop set price = 0.4 where price between 0.01 and 0.38;')
        #Alim_bbdd_sah.sql_minemas_e('update ps_product_shop set available_for_order = 0 where price = 0')
        #Alim_bbdd_sah.sql_minemas_e('update ps_product set available_for_order = 0 where price = 0')

if __name__ == '__main__':
    #fpt_beta('betatruebaonline.com','BetaProductos','fR2*ixB1()')
    #generar_dataframes('TARIFA 15-09-2021.xlsx','Inventario.XLSX',None)
    df_csv('products.csv_limpio')
