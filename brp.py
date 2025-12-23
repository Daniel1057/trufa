from selenium import webdriver
from urllib.request import urlretrieve
import pandas as pd
import os
import time

dormir = 5

def descarga_img(enlace,v_tipo,v_anyo,v_familia,v_vehiculo,v_categoria):

    dir = os.path.abspath('./brp/img/')
    fichero = str(v_tipo)+'_'+str(v_anyo)+'_'+str(v_familia)+'_'+str(v_vehiculo)+'_'+str(v_categoria)+".png"
    work_path=os.path.join(dir,fichero)
    urlretrieve(enlace,work_path)
    return(fichero)

def descarga_categoria(driver,v_tipo,v_anyo,v_familia,v_vehiculo,v_categoria):
    time.sleep(2*dormir)
    #descarga imagen categoria
    img_categoria_Medium = driver.find_element_by_xpath('//*[@id="ariparts_image"]').get_attribute('src')
    descarga_img(img_categoria_Medium, v_tipo, v_anyo, v_familia, v_vehiculo, 'Medium_' + v_categoria)
    img_categoria_ExtraSmall = img_categoria_Medium.replace('Medium', 'ExtraSmall')
    descarga_img(img_categoria_ExtraSmall, v_tipo, v_anyo, v_familia, v_vehiculo, 'ExtraSmall_' + v_categoria)
    img_categoria_Small = img_categoria_Medium.replace('Medium', 'Small')
    descarga_img(img_categoria_Small, v_tipo, v_anyo, v_familia, v_vehiculo, 'Small_' + v_categoria)
    img_categoria_Large = img_categoria_Medium.replace('Medium', 'Large')
    descarga_img(img_categoria_Large, v_tipo, v_anyo, v_familia, v_vehiculo, 'Large_' + v_categoria)
    img_categoria_ExtraLarge = img_categoria_Medium.replace('Medium', 'ExtraLarge')
    descarga_img(img_categoria_ExtraLarge, v_tipo, v_anyo, v_familia, v_vehiculo, 'ExtraLarge_' + v_categoria)
    img_categoria_Max = img_categoria_Medium.replace('Medium', 'Max')
    descarga_img(img_categoria_Max, v_tipo, v_anyo, v_familia, v_vehiculo, 'Max_' + v_categoria)

    matriz = driver.find_element_by_xpath('//*[@id="ariPartList"]').text
    l_matriz = matriz.split('Ref:')
    df = pd.DataFrame(columns=['posicion','referencia','descripcion','observacion'])
    for registro in range(len(l_matriz)):
        l_registro = l_matriz[registro].splitlines()
        if(len(l_registro)>0):
            v_posicion = l_registro[1]
            v_referencia = l_registro[2]
            v_descripcion = l_registro[3]
            v_observaciones = l_registro[4]
            d_registro = {'posicion':[v_posicion],'referencia':[v_referencia],'descripcion':[v_descripcion],'observacion':[v_observaciones]}
            df = pd.concat([df,pd.DataFrame(data=d_registro)],ignore_index=True)
    df['tipo']=v_tipo
    df['anyo']=v_anyo
    df['familia']=v_familia
    df['vehiculo']=v_vehiculo
    df['categoria'] = v_categoria
    fichero = './brp/doc/'+str(v_tipo)+'_'+str(v_anyo)+'_'+str(v_familia)+'_'+str(v_vehiculo)+'_'+str(v_categoria)+'.xlsx'
    df.to_excel(fichero)
    print (fichero)



def descarga_moto(driver,v_tipo,v_anyo,v_familia,v_vehiculo):
    l_categorias = (driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[12]/div[2]/div[3]/div[2]').text).splitlines()
    for categoria in range(len(l_categorias)):
        if (categoria > 0):
            driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[11]/ul/li[5]').click()
        v_categoria = l_categorias[categoria]
        driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[12]/div[2]/div[3]/div[2]/div[' + str(categoria + 1) + ']').click()
        descarga_categoria(driver,v_tipo,v_anyo,v_familia,v_vehiculo,v_categoria)



def descarga(url):
    driver = webdriver.Firefox()
    driver.get(url)
    driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[12]/div[2]/div[1]/div[1]').click()
    time.sleep(dormir)
    l_tipos = (driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[12]/div[2]/div[3]').text).splitlines()

    for tipo in range(len(l_tipos)):
        if (tipo>0):
            driver.find_element_by_xpath('//*[@id="ari-new-search-btn"]').click()
        time.sleep(dormir)
        v_tipo = l_tipos[tipo]
        driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[12]/div[2]/div[3]/div/div['+str(tipo+1)+']').click()
        time.sleep(dormir)
        l_anyos = (driver.find_element_by_xpath('//*[@id="ari-hlvl-3xiMPWfqHAPIXFPSCOBLAA2"]').text).splitlines()
        for anyos in range(len(l_anyos)):
            v_anyo = l_anyos[anyos]
            if (anyos>0):
                driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[11]/ul/li[2]').click()
            time.sleep(dormir)
            driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[12]/div[2]/div[3]/div[2]/div/ul/li['+str(anyos+1)+']').click()
            time.sleep(dormir)
            l_familia = (driver.find_element_by_xpath('//*[@id="ari-hlvl-i8YTGsJhlujsZele9D_gKA2"]').text).splitlines()
            for familia in range(len(l_familia)):
                v_familia=l_familia[familia]
                if(familia>0):
                    driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[11]/ul/li[3]').click()
                time.sleep(dormir)
                driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[12]/div[2]/div[3]/div[2]/div[2]/ul/li['+str(familia+1)+']').click()
                time.sleep(dormir)
                l_vehiculo = (driver.find_element_by_xpath('//*[@id="ari-hlvl-o_Rzbbr7Y19X9CgyfGv5ng2"]').text).splitlines()
                for vehiculo in range(len(l_vehiculo)):
                    v_vehiculo = l_vehiculo[vehiculo]
                    if (vehiculo>0):
                        driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[11]/ul/li[4]').click()
                    time.sleep(2*dormir)
                    driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[12]/div[2]/div[3]/div[2]/div[3]/ul/li['+str(vehiculo+1)+']').click()
                    time.sleep(dormir)
                    descarga_moto(driver,v_tipo,v_anyo,v_familia,v_vehiculo)
    print (url)

if __name__=="__main__":
    descarga('https://epc.brp.com/')