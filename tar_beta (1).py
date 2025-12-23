from sqlalchemy import create_engine
import pymysql
import pandas as pd
import sys
import Alim_bbdd_sah
import prestaweb

def generar_dataframes(fichero_tarifa,fichero_inventario):
    update_web = True
    #Carga df de la web
    beta_web = Alim_bbdd_sah.table_to_df('SELECT * FROM v_beta_product')
    beta_web['cod'] = beta_web['reference'].str.replace('.', '',regex=True)

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

    #Carga la tarifa de Beta
    tarifa = pd.read_excel(fichero_tarifa)

    #Elimina los puntos del código para poder comparar tanto con prestashop como con factusol
    tarifa['cod']=tarifa['Article'].str.replace('.','',regex=True)

    #Copia del df de tarifa
    tarifa_aux = tarifa


    #Une tarifa con la web y el inventario
    tarifa = pd.merge(left=tarifa, right=beta_web, how='left', left_on='cod', right_on='cod')
    tarifa= pd.merge(left=tarifa, right=inventario, how='left', left_on='cod', right_on='cod')

    #Referencias existentes en la tarifa pero no en la web
    beta_si_tarifa_no_web = tarifa[tarifa['id_product'].isna()]
    #Referencias no existentes en la web y que hay stock en factusol
    beta_si_tarifa_no_web_stock = beta_si_tarifa_no_web[beta_si_tarifa_no_web['Stock_Factusol'].notna()]
    beta_si_tarifa_no_web_stock.to_excel('salida_excel/beta_si_tarifa_no_web_stock.xlsx')
#    beta_si_tarifa_no_web = beta_si_tarifa_no_web[beta_si_tarifa_no_web['Stock_Factusol'].isna()]
#    beta_si_tarifa_no_web.to_excel('salida_excel/beta_si_tarifa_no_web.xlsx')


    #Buscamos las sustituciones
    if (tarifa[tarifa['Descripcion'].str.contains('#',na=False, regex=True)].size > 0):
        tarifa_sustitucion = tarifa[tarifa['Descripcion'].str.contains('#', na=False, regex=True)]
        tarifa_sustitucion ['newcod'] = tarifa_sustitucion['Descripcion'].str.replace('.', '', regex=True)
        tarifa_sustitucion['newcod'] = tarifa_sustitucion['newcod'].str.replace('#', '', regex=True)
        tarifa_sustitucion = pd.merge(left=tarifa_sustitucion, right=tarifa_aux, how='left', left_on='newcod', right_on='cod')

        #Referencias a sustituir que tienen stock en factusol
        tarifa_sustitucion_stock = tarifa_sustitucion[tarifa_sustitucion['Stock_Factusol'].notna()]
        tarifa_sustitucion_stock.to_excel('salida_excel/beta_ref_sust_stock.xlsx')

        #Referencias a sustituir que no tienen stock
        tarifa_sustitucion = tarifa_sustitucion[tarifa_sustitucion['Stock_Factusol'].isna()]
        tarifa_sustitucion.to_excel('salida_excel/beta_ref_sust.xlsx')

        #Eliminamos las referencias a sustituir del df
        tarifa= tarifa.drop(tarifa[tarifa['Descripcion'].str.contains('#', na=False, regex=True)].index)

    #Referencias obsoletas en la tarifa
    if (tarifa[tarifa['Descripcion'].str.contains('ARTICULO NO SUMINISTRABLE', na=False, regex=True)].size > 0):
        tarifa_no_vta = tarifa[tarifa['Descripcion'].str.contains('ARTICULO NO SUMINISTRABLE', na=False, regex=True)]

        #Referencias obsoletas pero hay stock en factusol
        tarifa_no_vta_stock = tarifa_no_vta[tarifa_no_vta['Stock_Factusol'].notna()]
        tarifa_no_vta_stock.to_excel('salida_excel/beta_ref_no_vta_stock.xlsx')

        #Referencias obsoletas sin stock
        tarifa_no_vta = tarifa_no_vta[tarifa_no_vta['Stock_Factusol'].isna()]
        tarifa_no_vta.to_excel('salida_excel/beta_ref_no_vta.xlsx')

        #Eliminamos las referencias obsoletas
        tarifa = tarifa.drop(tarifa[tarifa['Descripcion'].str.contains('ARTICULO NO SUMINISTRABLE', na=False, regex=True)].index)

    #Referencias que no tienen precio de vta en la nueva tarifa
    if(tarifa[tarifa.Preu == 0].size>0):
        tarifa_precio0 = tarifa[tarifa.Preu == 0]

        #Refrencias sin precio en la tarifa y que hay stock
        tarifa_precio0_stock = tarifa_precio0[tarifa_precio0['Stock_Factusol'].notna()]
        tarifa_precio0_stock.to_excel('salida_excel/beta_ref_preu0_stock.xlsx')

        #Referencias sin precio y que no hay stock
        tarifa_precio0 = tarifa_precio0[tarifa_precio0['Stock_Factusol'].isna()]
        tarifa_precio0.to_excel('salida_excel/beta_ref_preu0_stock.xlsx')

        #Eliminamos las referencias sin precio
        tarifa.drop(tarifa[tarifa.Preu == 0].index)


    #Diferencias de precio tarifa vs web
    tarifa['Dif_precio_web'] = tarifa['price'] - tarifa['Preu']

    #Diferencias de precio tarifa vs factusol
    tarifa['Dif_precio_factusol'] = tarifa['Costo_Factusol'] - tarifa['Preu']

    #Dataframe para con cambio de precios en la web
    tarifa_w =tarifa[tarifa['id_product'].notna()]
    tarifa_w =tarifa_w[tarifa_w['Dif_precio_web']!=0]
    tarifa_w.to_excel('salida_excel/beta_cambios_precio_web.xlsx')
    if(update_web):
        prestaweb.change_price_x_id_product(tarifa_w)

    #Cambio de precios para factusol
    tarifa_f =tarifa[tarifa['Cod_factusol'].notna()]
    tarifa_f =tarifa_f[tarifa_f['Dif_precio_factusol']!=0]
    tarifa_f.to_excel('salida_excel/beta_cambios_precio_factusol.xlsx')


if __name__ == '__main__':
    generar_dataframes('TARIFA 15-09-2021.xlsx','Inventario.XLSX')
