from selenium import webdriver
from urllib.request import urlretrieve
import pandas as pd
import os
import time

dormir = 2

def df_unico():
    ficheros = os.listdir('./beta/doc/')
    df_general = pd.DataFrame(columns=['Posición', 'Código', 'Cantidad', 'Descripción', 'Precio','anyo','moto', 'categoria'])

    for fichero in ficheros:

        print (fichero)
        if(fichero.find('xls')>0):
            df_fichero = pd.read_excel('./beta/doc/'+fichero)
            df_fichero = df_fichero[['Posición', 'Código', 'Cantidad', 'Descripción','Precio', 'anyo','moto', 'categoria']]
            df_general = pd.concat([df_general,df_fichero],ignore_index=True)
    df_general.to_excel('./beta/general_2023.xlsx')



def descarga_img(enlace,v_moto,v_categoria,anyo):

    dir = os.path.abspath('./beta/img/')
    fichero = str(anyo)+'_'+str(v_moto)+'_'+str(v_categoria)+".jpg"
    work_path=os.path.join(dir,fichero)
    urlretrieve(enlace,work_path)
    return(fichero)

def descarga_categoria(driver,v_moto,v_categoria,anyo):
    categoria = driver.find_element_by_xpath('/html/body/div[4]/div/span').text
    #descarga imagen categoria
    img_categoria = driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/img').get_attribute('src')
    descarga_img(img_categoria, v_moto, v_categoria,str(anyo))
    df = pd.read_html(driver.page_source)
    matriz = df[0]
    matriz = matriz[['Posición', 'Código', 'Cantidad', 'Descripción','Precio']]
    matriz['anyo']=anyo
    matriz['moto']=v_moto
    matriz['categoria'] = v_categoria
    fichero = './beta/doc/'+str(anyo)+'_'+str(v_moto)+'_'+v_categoria+'.xlsx'
    matriz.to_excel(fichero)
    print (df)



def descarga_moto(driver,v_moto,anyo):
    url_moto = driver.current_url
    # Imagen de la moto
    v_img_moto = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/img').get_attribute('src')
    descarga_img(v_img_moto, v_moto, 'General',str(anyo))


    try:
        l_lista_categorias = driver.find_element_by_xpath('/html/body/div[4]/div/div[3]').text
        preenlace = '/html/body/div[4]/div/div[3]/div['
    except:
        l_lista_categorias = driver.find_element_by_xpath('/html/body/div[4]/div/div[2]').text
        preenlace = '/html/body/div[4]/div/div[2]/div['

    l_lista_categorias = l_lista_categorias.splitlines()

    #Descargar imagenes miniaturas

    for categoria in range(len(l_lista_categorias)):
        driver.get(url_moto)
        time.sleep(dormir)
        v_categoria = l_lista_categorias[categoria]
        v_imagen = driver.find_element_by_xpath(preenlace+str(categoria+1)+']/a/div/img').get_attribute('src')
        descarga_img(v_imagen, v_moto, 'mini_'+v_categoria,str(anyo))
        driver.get(driver.find_element_by_xpath(preenlace+str(categoria+1)+']/a').get_attribute('href'))
        time.sleep(dormir)
        descarga_categoria(driver,v_moto,v_categoria,anyo)

    #hacer click


def descarga(url,anyo):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(dormir)

    l_listados_motos = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]').text
    l_listados_motos = l_listados_motos.splitlines()
    for moto in range(len(l_listados_motos)):
        driver.get(url)
        time.sleep(dormir)
        v_moto = l_listados_motos[moto]
        if (v_moto.find('RACING')>-1):
            v_imagen = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div['+str(moto+1)+']/a/div[1]/img').get_attribute('src')
            descarga_img(v_imagen,v_moto,'General_miniatura',str(anyo))
            driver.get(driver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/div['+str(moto+1)+']/a').get_attribute('href'))
            time.sleep(dormir)
            descarga_moto(driver,v_moto,anyo)
    print (url)

def comparar_df():
    d1 = pd.read_excel('./beta_23/general_2023.xlsx')
    d2 = pd.read_excel('./beta_2022/general_2022.xlsx')
    print (d1)
    d1['compara'] = d1['Posición'].astype(str).replace('\n','')+'-'+d1['Código'].astype(str).replace('\n','')+'-'+d1['Cantidad'].astype(str).replace('\n','')+'-'+d1['moto'].astype(str).replace('\n','')+'-'+d1['categoria'].astype(str).replace('\n','')
    d2['compara'] = d2['Posición'].astype(str).replace('\n', '') + '-' + d2['Código'].astype(str).replace('\n','') + '-' +d2['Cantidad'].astype(str).replace('\n', '') + '-' + d2['moto'].astype(str).replace('\n','') + '-' + d2['categoria'].astype(str).replace('\n', '')
    d1_compara = d1.copy()
    d2_compara = d2.copy()
    d1_compara = d1_compara['compara']
    d2_compara = d2_compara['compara']
    d1_compara.compare(d2_compara)
    nuevas_referencias=d1_compara[~d1_compara.isin(d2_compara)].dropna()
    nuevas_referencias=d1.loc[d1.index & nuevas_referencias.index]
if __name__=="__main__":
    if (False):
        descarga('https://betatruebaonline.com/motos/2023/6','2023')
        df_unico()
    if (True):
        comparar_df()


