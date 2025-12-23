from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys
import Alim_bbdd_sah
update_web = True

def generar_dataframes(marca,fichero_tarifa,fichero_inventario):
    Husqvarna = False
    Sherco = False

    #Revisión fichero inventario
    if (fichero_inventario==None):
        Cargar_inventario = False
    else:
        Cargar_inventario = True


    #Carga df de la web
    if (marca == 'Husqvarna' ):
        query = 'SELECT * FROM v_husq_product'
        Husqvarna = True

    if (marca == 'Sherco' ):
        query = 'SELECT * FROM v_sherco_product'
        Sherco = True
    marca_web = Alim_bbdd_sah.table_to_df(query)
    marca_web['cod'] = marca_web['reference']
    marca_web['cod'] = marca_web['cod'].astype("string")
    marca_web['cod'] = marca_web['cod'].str.replace('.', '',regex=True)


    if (Cargar_inventario):
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
        #Alim_bbdd_sah.carga_tarifa_bbdd(inventario,'t_inventario_factusol')

    else:
        inventario = pd.DataFrame(
            columns=["cod", "Cod_factusol", "Desc_factusol", "Ref_Prov_Factusol", "Porv_factusol", "Costo_Factusol","PVP_Factusol", "Stock_Factusol", "Obs_Factusol"])

    #Carga la tarifa de marca
    tarifa = pd.read_excel(fichero_tarifa)


    if(Sherco):

        tarifa['prefijo']='S'
        tarifa['Código'] = tarifa['prefijo']+tarifa['Código']
        tarifa_aux = tarifa.copy()
        tarifa = pd.merge(left=tarifa, right=marca_web, how='left', left_on='Código', right_on='cod')
        tarifa = tarifa[tarifa['id_product'].notna()]
        tarifa['id_product'] = tarifa['id_product'].astype("int")
        tarifa['Público'] = tarifa['Público'].str.replace(',','.').astype("float")
        tarifa['price'] = tarifa['price'].astype("float")
        tarifa['diferencia'] = tarifa['Público'] - tarifa['price']
        tarifa = tarifa[tarifa['diferencia'] != 0]
        fichero_excel = 'salida_excel/Sherco_cambios_precio_web.xlsx'
        tarifa.to_excel(fichero_excel)
        if(update_web):
            if(len(tarifa)>0):
                Alim_bbdd_sah.carga_tarifa_bbdd_e(tarifa, 'Cambio_preu_sherco')
                Alim_bbdd_sah.sql_minemas_e("update nuevaendurorecambios.ps_product a , nuevaendurorecambios.Cambio_preu_sherco b set a.price = b.`Público` where a.id_product = b.id_product;")
                Alim_bbdd_sah.sql_minemas_e(" update nuevaendurorecambios.ps_product_shop a , nuevaendurorecambios.Cambio_preu_sherco b set a.price = b.`Público` where a.id_product = b.id_product;")
        tarifa = tarifa_aux

        tarifa['Código'] = tarifa['Código'].astype("string")
        inventario['cod'] = inventario['cod'].astype("string")
        #inventario['Cod_factusol'] = inventario['Cod_factusol'].str.replace('S', '')
        tarifa= pd.merge(left=tarifa, right=inventario, how='left', left_on='Código', right_on='cod')

#        fichero_excel = 'salida_excel/Sherco_cambios_precio_web.xlsx'
#        tarifa.to_excel(fichero_excel)
        tarifa = tarifa[tarifa['Cod_factusol'].notna()]
        tarifa['Coste'] = None
        tarifa ['Familia Descuento'] = None
        tarifa['Precio Venta sin impuestos'] = tarifa['Público']
        df_factusol = tarifa[['Cod_factusol', 'Desc_factusol', 'Precio Venta sin impuestos', 'Coste', 'Familia Descuento']].copy()


    if(Husqvarna):
        #Elimina los puntos del código para poder comparar tanto con prestashop como con factusol
        tarifa['cod'] = tarifa['#Article Number']
        tarifa['cod'] = tarifa['cod'].astype("string")
        tarifa['cod']=tarifa['cod'].str.replace('.','',regex=True)
        #Copia del df de tarifa
        tarifa_aux = tarifa.copy()

        #Une web con la tarifa
        tarifa['cod'] = tarifa['cod'].astype("string")
        marca_web['cod'] = marca_web['cod'].astype("string")
        tarifa = pd.merge(left=tarifa, right=marca_web, how='left', left_on='cod', right_on='cod')
        tarifa = tarifa[tarifa['id_product'].notna()]
        tarifa['id_product'] = tarifa['id_product'].astype("int")
        tarifa['Sales Price'] = tarifa['Retail Price (excl. VAT)'].astype("float")
        tarifa['price'] = tarifa['price'].astype("float")
        tarifa['diferencia'] = tarifa['Sales Price']  - tarifa['price']
        tarifa = tarifa[tarifa['diferencia']!=0]
        fichero_excel = 'salida_excel/Husqvarna_cambios_precio_web.xlsx'
        tarifa.to_excel(fichero_excel)
        if(update_web):
            if(len(tarifa)>0):
                Alim_bbdd_sah.carga_tarifa_bbdd_e(tarifa, 'Cambio_preu_hsq')
                Alim_bbdd_sah.sql_minemas_e("update nuevaendurorecambios.ps_product a , nuevaendurorecambios.Cambio_preu_hsq b set a.price = b.`Sales Price` where a.id_product = b.id_product;")
                Alim_bbdd_sah.sql_minemas_e(" update nuevaendurorecambios.ps_product_shop a , nuevaendurorecambios.Cambio_preu_hsq b set a.price = b.`Sales Price` where a.id_product = b.id_product;")
        tarifa = tarifa_aux
        tarifa['cod'] = tarifa['cod'].astype("string")
        inventario['cod'] = inventario['cod'].astype("string")
        tarifa= pd.merge(left=tarifa, right=inventario, how='left', left_on='cod', right_on='cod')
        tarifa = tarifa[tarifa['Cod_factusol'].notna()]
        tarifa['Coste'] = tarifa['Margin'] / 100
        tarifa['Coste'] = tarifa['Retail Price (excl. VAT)'] - (tarifa['Retail Price (excl. VAT)'] * tarifa['Coste'])
        tarifa['Familia Descuento'] = tarifa['Margin']
        tarifa['Precio Venta sin impuestos'] = tarifa['Retail Price (excl. VAT)']
        df_factusol = tarifa[['Cod_factusol', 'Desc_factusol', 'Precio Venta sin impuestos', 'Coste', 'Familia Descuento']].copy()





    if(Sherco):

        fichero_excel = 'salida_excel/Sherco_factusol.xlsx'



    if (Husqvarna):
        fichero_excel = 'salida_excel/Husqvarna_factusol.xlsx'

    df_factusol.to_excel(fichero_excel,sheet_name='Fichero Factusol',index=False)

    if (update_web):
        Alim_bbdd_sah.sql_minemas_e('update ps_product set price = 0.4 where price between 0.01 and 0.38;')
        Alim_bbdd_sah.sql_minemas_e('update ps_product_shop set price = 0.4 where price between 0.01 and 0.38;')

if __name__ == '__main__':
    #generar_dataframes('Sherco','SHERCO NOVIEMBRE 2021.xlsx','Inventario.XLSX')
    generar_dataframes('Husqvarna', 'husqvarna 2023.xlsx', None)
