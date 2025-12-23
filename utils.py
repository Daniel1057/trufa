import pandas as pd
import chardet

fichero_x_categoria = False

def dic_change():
    lst_error = ['CIGUE�AL','PI�ON','SILL�N','5�','3�','6�','2�','1�','4�','M�XIMO','INYECCI�N','DI�METRO','T�RICA','PU�OS','GUARNICI�N','PROTECCI�N','FIJACI�N']
    lst_ok =    ['CIGUEÑAL','PIÑON','SILLÓN','5ª','3ª','6ª','2ª','1ª','4ª','MÁXIMO','INYECCIÓN','DIÁMETRO','TÓRICA','PUÑOS','GUARNICIÓN','PROTECCIÓN','FIJACIÓN']
    df = pd.DataFrame(list(zip(lst_error, lst_ok)),columns=['Valor', 'Cambiar'])
    return df

def interesante():
    with open("./csv_web/ENDURO RR 125 2T_.csv", 'rb') as rawdata:
        result = chardet.detect(rawdata.read(10000))
    # check what the character encoding might be
    print(result)

def preparar_df():
    df_csv = pd.read_excel('general_2023.xlsx')
    df_change = dic_change()
    for i in df_change.index:
        print(i)
        df_csv['Descripción']=df_csv['Descripción'].str.replace(df_change['Valor'][i],df_change['Cambiar'][i])
    df_csv.drop(['Unnamed: 0'], axis=1, inplace=True)
    motos = df_csv['moto'].unique()
    for moto in motos:
        df_moto = df_csv[df_csv['moto']==moto].copy()
        if (fichero_x_categoria):
            categorias = df_moto['categoria'].unique()
            for categoria in categorias:
                df_categoria = df_moto[df_moto['categoria'] == categoria].copy()
                genera_csv(df_categoria,'BETA','Trufa_',moto,categoria)
        else:
            genera_csv(df_moto, 'BETA', 'Trufa_', moto, '')
def genera_csv (df_csv,marca,prefijo,moto,categoria):
    df_csv['Precio'] = df_csv['Precio'].str.replace('€', '')
    df_csv['componente'] = df_csv['categoria'].str[:127]
    df_csv['tax'] = 17
    df_csv['shop_default'] = 1
    df_csv['mostrar_pvp'] = 1
    df_csv['marca'] = marca
    df_csv['on_sale'] = 1
    df_csv['active'] = 1
    df_csv['stock']=9999
    df_csv['Descripcion']=df_csv['Descripción'].astype(str)
    df_csv['modelo'] = df_csv['moto'].astype(str)
    df_csv['Código'] = df_csv['Código'].astype(str)
    df_csv['Cantidad'] = df_csv['Cantidad'].astype(str)
    df_csv['Posición']=df_csv['Posición'].astype(str)
    df_csv['Nombre'] = "Nº "+df_csv['Posición']+" - "+df_csv['Descripcion'] + " - " + df_csv['Código']
    df_csv['Nombre'] = df_csv['Nombre'].str.replace('#', '')
    df_csv['Nombre'] = df_csv['Nombre'].str.replace('&', '')
    df_csv['Nombre'] = df_csv['Nombre'].str.replace("'", "")
    for i in df_csv.index:
        df_csv['modelo'][i]=str(df_csv['anyo'][i])+'_'+df_csv['modelo'][i]
        if(str(df_csv['Descripcion'][i]).find('�')>-1):
            print(df_csv['Descripcion'][i])
        if(df_csv['Precio'][i]==0):
            df_csv['on_sale'][i] = 0
        df_csv['componente'][i]=str(prefijo)+df_csv['modelo'][i]+'_'+df_csv['componente'][i]
        df_csv['Descripcion'][i] = "Nº "+str(df_csv['Posición'][i])+" - "+str(df_csv['Descripcion'][i])+" - "+str(df_csv['modelo'][i])+" - "+str(df_csv['Código'][i])+". Se vende por unidades, según despiece son necesarias "+str(df_csv['Cantidad'][i])+" u"
    df_csv['componente'] = df_csv['componente'].str[:127]
    df_csv['componente']=df_csv['componente'].str.replace(' ','_')
    df_csv.drop(['Posición',  'Cantidad', 'Descripción', 'anyo', 'moto', 'categoria'], axis=1,inplace=True)
    df_csv.to_csv('./csv_web/'+str(moto)+'_'+categoria+'.csv',index = False, sep = ';')

if __name__=="__main__":
    preparar_df()
    #interesante()

