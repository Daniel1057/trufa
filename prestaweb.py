from PIL import Image
import requests
#from __future__ import print_function

import pandas as pd
from prestapyt import PrestaShopWebServiceDict
from xml.etree import ElementTree
from os import listdir
import os
import sys
import urllib.request
import Alim_bbdd_sah
import re

def alim():
    prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    #datos_product = prestashop.get('products', resource_id=227602)
    #print (datos_product)
    stock = prestashop.get('stock_availables', resource_id=prestashop.search('stock_availables', options={'filter[id_product]': '228273'})[0])
    stock['stock_available']['quantity'] = '9999'
    prestashop.edit('stock_availables', stock)

def specifi_price():
    prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    xml_percentaje = {'id': '77257', 'id_shop_group': '0', 'id_shop': '1', 'id_cart': '0', 'id_product': '227244', 'id_product_attribute': '0', 'id_currency': '0', 'id_country': '0', 'id_group': '5', 'id_customer': '0', 'id_specific_price_rule': '0', 'price': '-1.000000', 'from_quantity': '1', 'reduction': '0.100000', 'reduction_tax': '1', 'reduction_type': 'percentage', 'from': '0000-00-00 00:00:00', 'to': '0000-00-00 00:00:00'}
    xml_example = prestashop.search('specific_prices', options={'filter[id_product]': str(227244)})
def change_price_x_value():
    prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    df = Alim_bbdd_sah.table_to_df('SELECT * FROM v_brp_product')
    for i in range(len(df)):
        print (str(df['id_product'][i]))
        if (int(df['id_product'][i])>191681):
            print ('dentro')
            xml_prod = prestashop.get('products', df['id_product'][i])
            xml_prod['product']['manufacturer_name'] = []
            xml_prod['product']['quantity'] = []
            old_price = xml_prod['product']['price']
            old_price = float(old_price)
            print(float(old_price))
            old_price=str(round(old_price * 1.07,2))
            print(old_price)
            xml_prod['product']['price'] = old_price
            prestashop.edit('products', xml_prod)

def change_price_x_id_product(df_change_price):
    #prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    df_change_price['id_product'] = df_change_price['id_product'].astype(int)
    df_change_price.reset_index(drop=True, inplace=True)
    for i in range(len(df_change_price)):

        new_price = str(df_change_price['Preu'][i])
        new_price = new_price.replace(',','.')
        sql = 'update ps_product set price='+new_price+' where id_product='+str(df_change_price['id_product'][i])
        sql_1 =  'update ps_product_shop set price='+new_price+' where id_product='+str(df_change_price['id_product'][i])
        print('***************************************************************')
        print('---->'+sql)
        print('---->' +sql_1)
        print('***************************************************************')
        Alim_bbdd_sah.sql_minemas_e(sql)
        Alim_bbdd_sah.sql_minemas_e(sql_1)

def ps_web_catego_producto(df,manufacturer):
    valor_link = 0
    prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    #xml_cate = prestashop.get('categories', options={'schema': 'blank'})704869
    if (manufacturer == '13'):
        categorias = df['modelo'].unique()
        nueva_categoria = True
        categoria_root = '150770'

    if (manufacturer == '103'):
        categorias = df['modelo'].unique()
        nueva_categoria = True
        categoria_root = '149617'
    for categoria in categorias:
        alim_categoria = "ALIM_"+categoria
        link = categoria.replace(" ","_")
        link = link.replace(",","_")
        link = link.replace("ñ", "ny")
        link = link.replace(' ', '_')
        link = link.replace(',', '_')
        link = link.replace('-', '_')
        link = link.replace('--', '_')
        link = link.replace('---', '_')
        link = link.replace('ñ', 'ny')
        link = link.replace('á', 'a')
        link = link.replace('é', 'e')
        link = link.replace('í', 'i')
        link = link.replace('ó', 'o')
        link = link.replace('ú', 'u')
        link = link.replace('Á', 'A')
        link = link.replace('É', 'E')
        link = link.replace('Í', 'I')
        link = link.replace('Ó', 'O')
        link = link.replace('Ú', 'U')
        link = re.sub(r"[^a-zA-Z0-9]","",link)
        valor = prestashop.get('categories', options={'filter[name]': alim_categoria})
        if(valor['categories']!=''):
            cat_padre = valor['categories']['category']['attrs']['id']
        else:
            new_catego = {
                'category': {'id': '', 'id_parent': str(categoria_root), 'active': '0', 'id_shop_default': '1', 'is_root_category': '','position': '', 'date_add': '', 'date_upd': '', 'name': {'language': [{'attrs': {'id': '1'}, 'value': str(alim_categoria)},{'attrs': {'id': '2'}, 'value': str(alim_categoria)}]}, 'link_rewrite': {'language': [{'attrs': {'id': '1'}, 'value': str(link)},{'attrs': {'id': '2'}, 'value': str(link)}]}, 'description': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},'meta_title': {
                                 'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'meta_description': {
                                 'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'meta_keywords': {
                                 'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                             'associations': {'categories': {'category': {'id': ''}}, 'products': {'product': {'id': ''}}}}}
            print(new_catego)
            cat = prestashop.add('categories', new_catego)
            cat_padre = prestashop.search('categories', options={'filter[name]': str(alim_categoria)})


        df_categorias_hijas = df[df['modelo'] == categoria]
        categorias_hijas = df_categorias_hijas['componente'].unique()
        for hija in categorias_hijas:
            #Crear categoria hija refrenciadas al padre
            alim_categoria = "ALIM_" + hija
            link = hija.replace(" ", "_")
            link = link.replace(' ', '_')
            link = link.replace(',', '_')
            link = link.replace('-', '_')
            link = link.replace('--', '_')
            link = link.replace('---', '_')
            link = link.replace('ñ', 'ny')
            link = link.replace('á', 'a')
            link = link.replace('é', 'e')
            link = link.replace('í', 'i')
            link = link.replace('ó', 'o')
            link = link.replace('ú', 'u')
            link = link.replace('Á', 'A')
            link = link.replace('É', 'E')
            link = link.replace('Í', 'I')
            link = link.replace('Ó', 'O')
            link = link.replace('Ú', 'U')
            link = re.sub(r"[^a-zA-Z0-9]", "", link)
            valor = prestashop.get('categories', options={'filter[name]': alim_categoria})
            if (valor['categories'] != ''):
                cat_hija = valor['categories']['category']['attrs']['id']
            else:
                new_catego = {
                    'category': {'id': '', 'id_parent': cat_padre, 'active': '0', 'id_shop_default': '1',
                                 'is_root_category': '', 'position': '', 'date_add': '', 'date_upd': '', 'name': {
                            'language': [{'attrs': {'id': '1'}, 'value': str(alim_categoria)},
                                         {'attrs': {'id': '2'}, 'value': str(alim_categoria)}]}, 'link_rewrite': {
                            'language': [{'attrs': {'id': '1'}, 'value': str(link)},
                                         {'attrs': {'id': '2'}, 'value': str(link)}]}, 'description': {
                            'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                                 'meta_title': {
                                     'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                  {'attrs': {'id': '2'}, 'value': ''}]},
                                 'meta_description': {
                                     'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                  {'attrs': {'id': '2'}, 'value': ''}]},
                                 'meta_keywords': {
                                     'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                  {'attrs': {'id': '2'}, 'value': ''}]},
                                 'associations': {'categories': {'category': {'id': ''}},
                                                  'products': {'product': {'id': ''}}}}}
                cat = prestashop.add('categories', new_catego)
                cat_hija = prestashop.search('categories', options={'filter[name]': str(alim_categoria)})
            df_producto_hijas = df[df['componente'] == hija]
            for i in df_producto_hijas.index:
                try:
                    valor_link = valor_link+1
                    if (manufacturer == '13'):
                        referencia =str(df_producto_hijas['Part Number'][i])
                        referencia = referencia.replace ('.','')
                        posicion = str(df_producto_hijas['Ref.'][i])
                        cantidad = str(df_producto_hijas['Parts'][i])
                        descripcion = str(df_producto_hijas['Descripcion_x'][i])
                        descripcion = descripcion.replace('=',' ')
                        moto = str(df_producto_hijas['modelo'][i])
                        nombre ="Nº "+ str(posicion)+" - "+str(descripcion)+" - "+str(referencia)
                        descripcion = "Nº "+str(posicion)+" - "+str(descripcion)+ "- "+str(moto)+" - "+str(referencia)+". Se vende por unidades, según despiece son necesarias "+str(cantidad)+" u"
                        precio = str(df_producto_hijas['Preu_x'][i])
                        print (referencia+" ")
                        if (precio == 'nan'):
                            precio ='999999'

                    if (manufacturer =='103'):
                        referencia =str(df_producto_hijas['Part #'][i])
                        referencia = referencia.replace('.0','')
                        posicion = str(df_producto_hijas['#'][i])
                        cantidad = str(df_producto_hijas['Qty'][i])
                        descripcion = str(df_producto_hijas['Description'][i])
                        moto = str(df_producto_hijas['modelo'][i])
                        nombre = "Nº "+str(posicion)+" - "+str(descripcion)+" - "+str(referencia)
                        nombre = nombre[6:-6]
                        descripcion = "Nº "+str(posicion)+" - "+str(descripcion)+" - "+str(moto)+" - "+str(referencia)+". Se vende por unidades, según despiece son necesarias "+str(cantidad)+" u"
                        link = nombre+"_"+str(valor_link)
                        link = link.replace(' ','_')
                        link = link.replace(',', '_')
                        link = link.replace('-', '_')
                        link = link.replace('--', '_')
                        link = link.replace('---', '_')
                        link = link.replace('ñ', 'ny')
                        link = link.replace('á', 'a')
                        link = link.replace('é', 'e')
                        link = link.replace('í', 'i')
                        link = link.replace('ó', 'o')
                        link = link.replace('ú', 'u')
                        link = link.replace('Á', 'A')
                        link = link.replace('É', 'E')
                        link = link.replace('Í', 'I')
                        link = link.replace('Ó', 'O')
                        link = link.replace('Ú', 'U')
                        link = re.sub(r"[^a-zA-Z0-9]", "", link)
                        link = link[:127]
                        precio = str(df_producto_hijas['Retail_Price'][i])
                        print (referencia+" ")
                        if (precio == 'nan'):
                            precio ='999999'
                    print(moto)
                    print (alim_categoria)

                    data_product = {'product': {'id': '', 'id_manufacturer': str(manufacturer), 'id_supplier': '',
                                                'id_category_default': cat_hija, 'new': '', 'cache_default_attribute': '',
                                                'id_default_image': '', 'id_default_combination': '',
                                                'id_tax_rules_group': '17', 'position_in_category': '', 'type': '',
                                                'id_shop_default': '1', 'reference': str(referencia),
                                                'supplier_reference': '', 'location': '', 'width': '', 'height': '',
                                                'depth': '', 'weight': '', 'quantity_discount': '', 'ean13': '', 'isbn': '',
                                                'upc': '', 'cache_is_pack': '', 'cache_has_attachments': '',
                                                'is_virtual': '', 'state': '1', 'additional_delivery_times': '',
                                                'delivery_in_stock': {
                                                    'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                 {'attrs': {'id': '2'}, 'value': ''}]},
                                                'delivery_out_stock': {'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                                    {'attrs': {'id': '2'}, 'value': ''}]},
                                                'on_sale': '0', 'online_only': '', 'ecotax': '', 'minimal_quantity': '',
                                                'low_stock_threshold': '', 'low_stock_alert': '', 'price': str(precio),
                                                'wholesale_price': '', 'unity': '', 'unit_price_ratio': '',
                                                'additional_shipping_cost': '', 'customizable': '', 'text_fields': '',
                                                'uploadable_files': '', 'active': '0', 'redirect_type': '301-category',
                                                'id_type_redirected': '', 'available_for_order': '1', 'available_date': '',
                                                'show_condition': '', 'condition': '', 'show_price': '', 'indexed': '',
                                                'visibility': '', 'advanced_stock_management': '', 'date_add': '',
                                                'date_upd': '', 'pack_stock_type': '', 'meta_description': {
                            'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                                                'meta_keywords': {'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                               {'attrs': {'id': '2'}, 'value': ''}]},
                                                'meta_title': {'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                            {'attrs': {'id': '2'}, 'value': ''}]},
                                                'link_rewrite': {'language': [{'attrs': {'id': '1'}, 'value': str(link)},
                                                                              {'attrs': {'id': '2'}, 'value': str(link)}]},
                                                'name': {'language': [{'attrs': {'id': '1'}, 'value': str(nombre)},
                                                                      {'attrs': {'id': '2'}, 'value': str(nombre)}]},
                                                'description': {'language': [{'attrs': {'id': '1'}, 'value': str(descripcion)},
                                                                             {'attrs': {'id': '2'}, 'value': str(descripcion)}]},
                                                'description_short': {'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                                   {'attrs': {'id': '2'}, 'value': ''}]},
                                                'available_now': {'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                               {'attrs': {'id': '2'}, 'value': ''}]},
                                                'available_later': {'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                                 {'attrs': {'id': '2'}, 'value': ''}]},
                                                'associations': {'categories': {'category': {'id': ''}},
                                                                 'images': {'image': {'id': ''}},
                                                                 'combinations': {'combination': {'id': ''}},
                                                                 'product_option_values': {
                                                                     'product_option_value': {'id': ''}},
                                                                 'product_features': {
                                                                     'product_feature': {'id': '', 'id_feature_value': ''}},
                                                                 'tags': {'tag': {'id': ''}}, 'stock_availables': {
                                                        'stock_available': {'id': '', 'id_product_attribute': ''}},
                                                                 'accessories': {'product': {'id': ''}}, 'product_bundle': {
                                                        'product': {'id': '', 'id_product_attribute': '',
                                                                    'quantity': ''}}}}}
                    #print(data_product)
                    valor = prestashop.add('products', data_product)
                    stock = prestashop.get('stock_availables',resource_id = prestashop.search('stock_availables',options={'filter[id_product]': valor['prestashop']['product']['id']})[0])
                    stock['stock_available']['quantity'] = '9999'
                    prestashop.edit('stock_availables', stock)
                    print(valor)
                except:
                    print ("ERROR:")
                    print (data_product)

def search_category_by_name (name):
    prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    return prestashop.search('categories', options={'filter[name]': str(name)})
def search_product_by_id_category (category):
    prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    return prestashop.search('products', options={'filter[id_category_default]': str(category)})
def copy_image():
    try:
        prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
        datos_product = prestashop.get('products', resource_id=189656)
        product = prestashop.get('products', resource_id=227244)
        id_img = datos_product['product']['id_default_image']['value']
        product['product']['id_default_image']['value'] = datos_product['product']['id_default_image']['value']
        print(product)

    except:
        ("Error inesperado:" + str(sys.exc_info()[0]))

def get_image(tipo,id_origen,id,prefijo_web):
    prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    product = prestashop.get('products',resource_id=id_origen)
    link = product['product']['link_rewrite']['language'][0]['value']

    if(len(product['product']['associations']['images']['image'])<2):
        id_img = product['product']['associations']['images']['image']['id']
        url = str(prefijo_web) + '/' + str(id_img) + '/' + str(link) + '.jpg'
        im = requests.get(str(url))
        img = open("copia.jpg", "wb")
        img.write(im.content)
        img.close()
        add_image('copia.jpg', tipo, str(id))
    else:
        for num in product['product']['associations']['images']['image']:
            url = str(prefijo_web)+'/'+str(num['id'])+'/'+str(link)+'.jpg'
            im = requests.get(str(url))
            img = open("copia.jpg", "wb")
            img.write(im.content)
            img.close()
            add_image('copia.jpg',tipo,str(id))

def add_image(imagen,tipo,id):
    try:
        if(id.find('[')>0):
            id = id.replace('[','')
            id = id.replace(']', '')
        file_name = str(imagen)
        fd = open(file_name, "rb")
        content = fd.read()
        fd.close()
        prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
        (ruta_img) = '/images/'+str(tipo)+'/'+str(id)
        print (ruta_img)
        prestashop.add(ruta_img, files=[('image', file_name, content)])
        return 'Ok'
    except:
        return ("Error inesperado:" + str(sys.exc_info()[0]))
def recorrer_directorio (ruta):
    arch = listdir(str(ruta))
    ruta_completa = os.getcwd()
    ruta_completa = ruta_completa.replace('/prestaweb.py','')
    ruta_completa = ruta_completa+ruta.replace('.','')
    print(ruta_completa)
    for archivo in arch:
        if (archivo.find('png')>0):
            archivo1 = archivo.replace('Cuadro_','')
            archivo1 = archivo1.replace('Motor_', '')
            print(ruta_completa+archivo)
            print (str(search_category_by_name('ALIM_'+archivo1.replace('.png',''))))
            id_catego = search_category_by_name('ALIM_'+archivo1.replace('.png',''))
            if(len(id_catego)>0):
                print(add_image(ruta_completa+archivo, 'categories',str(id_catego[0])))

def recorrer_directorio_B (ruta):
    arch = listdir(str(ruta))
    ruta_completa = os.getcwd()
    ruta_completa = ruta_completa.replace('/prestaweb.py','')
    ruta_completa = ruta_completa+ruta.replace('.','')
    print(ruta_completa)
    for archivo in arch:
        if (archivo.find('jpg')>0):
            MOTO = archivo[archivo.find('ENDURO'):-4]
            DESPIECE = archivo[4:archivo.find('ENDURO') - 1]
            if(len(archivo)-len(MOTO)>8):
                categoria='ALIM_'+MOTO+"_"+DESPIECE
            else:
                categoria = 'ALIM_' + MOTO
            print(ruta_completa+archivo)
            print (str(search_category_by_name(categoria)))
            id_catego = search_category_by_name(categoria)
            if(len(id_catego)>0):
                print(add_image(ruta_completa+archivo, 'categories',str(id_catego[0])))

def recorrer_directorio_product_B (ruta):
    arch = listdir(str(ruta))
    ruta_completa = os.getcwd()
    ruta_completa = ruta_completa.replace('/prestaweb.py','')
    ruta_completa = ruta_completa+ruta.replace('.','')
    print(ruta_completa)
    for archivo in arch:
        if (archivo.find('jpg')>0):
            MOTO = archivo[archivo.find('ENDURO'):-4]
            DESPIECE = archivo[4:archivo.find('ENDURO') - 1]
            if(len(archivo)-len(MOTO)>8):
                categoria='ALIM_'+MOTO+"_"+DESPIECE
            else:
                categoria = 'ALIM_' + MOTO
            print(ruta_completa+archivo)
            print (str(search_category_by_name(categoria)))
            id_catego = search_category_by_name(categoria)
            products = search_product_by_id_category(id_catego[0])
            for product in products:
                print(product)
                print(add_image(ruta_completa+archivo, 'products',str(product)))
def carga_brp_20220123():
    df_tar = pd.read_excel('AtvDlrEuropeEUROAllXLS(2).xls')
    Alim_bbdd_sah.carga_tarifa_bbdd(df_tar, 'tar_carga_brp_19_18')
    ruta = './carga_20220123/'
    arch = listdir(str(ruta))
    ruta_completa = os.getcwd()
    ruta_completa = ruta_completa.replace('/prestaweb.py','')
    ruta_completa = ruta_completa+ruta.replace('.','')
    print(ruta_completa)
    primera_it = True
    for archivo in arch:
        print (archivo)
        if (archivo.find('xls')>1):
            anyo = archivo[:4]
            if(primera_it):
                primera_it = False
                df_completo = pd.read_excel(ruta_completa+archivo)
                df_completo['anyo'] = str(anyo)
            else:
                df_parcial = pd.read_excel(ruta_completa+archivo)
                df_parcial['anyo'] = str(anyo)
                df_completo = pd.concat([df_completo,df_parcial])
    df_completo = df_completo[['#', 'Part #', 'Description', 'Qty', 'Add to Pick List', 'modelo', 'componente', 'anyo']]
    Alim_bbdd_sah.carga_tarifa_bbdd(df_completo, 'Carga_brp_19_18')
    df_cargar=Alim_bbdd_sah.table_to_df("SELECT * FROM Minemas_R.tar_carga_brp_19_18 a, Minemas_R.Carga_brp_19_18 b where a.Material_No = b.`Part #` and anyo='2018'")
    ps_web_catego_producto(df_cargar, '103')

def recorrer_directorio_BRP (ruta):
    arch = listdir(str(ruta))
    ruta_completa = os.getcwd()
    ruta_completa = ruta_completa.replace('/prestaweb.py','')
    ruta_completa = ruta_completa+ruta.replace('.','')
    print(ruta_completa)
    for archivo in arch:
        print (archivo)
        if (archivo.find('18')>0):
            print(ruta_completa+archivo)
            catego = archivo[:-4]
            id_catego = search_category_by_name(catego)
            if(len(id_catego)>0):
                print(add_image(ruta_completa+archivo, 'categories',str(id_catego[0])))
def clonar_img():
    df_clonar = Alim_bbdd_sah.table_to_df_e("SELECT * FROM alim_image")
    for i in range(len(df_clonar)):
        referencia = df_clonar['referencia'][i]
        id_origen = df_clonar['id_product_origen'][i]
        id_destino = df_clonar['id_product_destino'][i]
        print('Clonado referencia: '+str(referencia)+' del producto '+str(id_origen)+' al '+str(id_destino))
        get_image('products', id_origen, id_destino, 'https://endurorecambios.com')

def borrar_csv():
    #sql = "select id_product from nuevaendurorecambios.ps_category_product where id_product in (select id_product from nuevaendurorecambios.t_borrar_brp2018);"
    #sql = "select id_category from nuevaendurorecambios.t_borrar_brp2018 group by id_category"
    sql = "SELECT distinct(id_category) FROM nuevaendurorecambios.t_borrar_brp2018"
    df_cargar = Alim_bbdd_sah.table_to_df(sql)
    df_cargar['sql'] = 'rm '
    for i in df_cargar.index:
        df_cargar['sql'][i] = df_cargar['sql'][i]+str(df_cargar['id_category'][i])+'* ;'
    df_cargar.to_csv('rm_category.csv', sep=';')



def genera_csv ():
    sql = 'SELECT * FROM Minemas_R.tar_carga_brp_19_18 a, Minemas_R.Carga_brp_19_18 b where a.Material_No = b.`Part #` '
    df_cargar = Alim_bbdd_sah.table_to_df(sql)
    df_csv = df_cargar[['Retail_Price', '#', 'Part #', 'Description', 'Qty', 'modelo', 'componente', 'anyo']]
    df_csv.columns = df_csv.columns.str.replace('\n', '')
    df_csv['componente'] = df_csv['componente'].str[:127]
    df_csv['tax'] = 17
    df_csv['shop_default'] = 1
    df_csv['mostrar_pvp'] = 1
    df_csv['marca'] = 'CAN-AM'
    df_csv['on_sale'] = 0
    df_csv['active'] = 1
    df_csv['stock']=9999
    df_csv['#']=df_csv['#'].astype(str)
    df_csv['Description']=df_csv['Description'].astype(str)
    df_csv['modelo'] = df_csv['modelo'].astype(str)
    df_csv['Part #'] = df_csv['Part #'].astype(str)
    df_csv['Qty'] = df_csv['Qty'].astype(str)
    df_csv['Nombre'] = df_csv['Description'] + " - " + df_csv['Part #']
    df_csv['Nombre'] = df_csv['Nombre'].str.replace('#', '')
    df_csv['Nombre'] = df_csv['Nombre'].str.replace('&', '')
    df_csv['Nombre'] = df_csv['Nombre'].str.replace("'", "")
    df_csv['Description_1'] ='hola'
    for i in df_csv.index:
        df_csv['modelo'][i]='ALIM_'+df_csv['anyo'][i]+'_'+df_csv['modelo'][i]
        df_csv['componente'][i]=df_csv['modelo'][i]+'_'+df_csv['componente'][i]
        df_csv['Description'][i] = "Nº "+str(df_csv['#'][i])+" - "+str(df_csv['Description'][i])+" - "+str(df_csv['modelo'][i])+" - "+str(df_csv['Part #'][i])+". Se vende por unidades, según despiece son necesarias "+str(df_csv['Qty'][i])+" u"
    df_csv['componente'] = df_csv['componente'].str[:127]
    df_csv.to_csv('completo_18_19.csv', sep=';')

def imagen_categoria_Beta():
    ruta='./beta_23/img/'
    prefijo = 'Trufa_'
    arch = listdir(str(ruta))
    for archivo in arch:
        if (archivo.find('2023_ENDURO RR 350 4T')>-1):
                categoria=archivo.replace(' ','_')
                categoria=prefijo+categoria[:-4]
                print(ruta+archivo)
                print (str(search_category_by_name(categoria)))
                id_catego = search_category_by_name(categoria)
                if(len(id_catego)>0):
                    print(add_image(ruta+archivo, 'categories',str(id_catego[0])))

"""
update ps_category_lang set name = replace(replace(name,'Trufa_2023_ENDURO_RR_350_4T_',''),'_',' ')  where id_shop = 1 and id_category between 211480 and 211510
"""
"""
update ps_category
set level_depth = 7, id_parent = 211511
where id_category between 211480 and 211510
"""
"""
update ps_stock_available set quantity = 9999, physical_quantity=9999 WHERE id_product between 1102811 and 1109398
"""
"""
insert into ps_category_group (id_category,id_group)
select id_category,'6'
from ps_category a
where id_category between 211261 and 211511 
and not exists (select 'x' from ps_category_group b where a.id_category = b.id_category and b.id_group = 6 )
"""

def imagen_incial():
    ruta ='./'
    arch = listdir(str(ruta))
    ruta_completa = os.getcwd()
    ruta_completa = ruta_completa.replace('/prestaweb.py','')
    ruta_completa = ruta_completa+ruta.replace('.','')
    print(ruta_completa)
    for archivo in arch:
        if (archivo.find('endurorecambios.png')>-1):
            print(ruta_completa+archivo)
            #products = search_product_by_id_category(id_catego[0])
            for catego in range(211480,211510):
                print (catego)
                if (catego==211261):
                    print ('hola')
                else:
                    products = search_product_by_id_category(catego)

            for product in products:
                print(product)
                print(add_image(ruta_completa+archivo, 'products',str(product)))


def excel_to_sql (sql,name_fichero):
    df_sql = Alim_bbdd_sah.table_to_df_e(sql)
    df_sql.to_excel(name_fichero,';')
if __name__ == '__main__':
    #alim()
    #change_price_x_value()
    #copy_image()
    #recorrer_directorio('./beta/img/')
    #add_image('/home/mauro/PycharmProjects/jarvis/beta/img/ENDURO_RR_125_2T_MY22_Cuadro_0.png','categories','149379')
    #ps_web_catego_producto(pd.read_excel('beta_trueba_df_completo_2022.xls'),'13')
    #recorrer_directorio_product_B('./IMGB2022/')
    #change_price_x_id_product(pd.read_excel('change_price_beta.xlsx'))
    #carga_brp_20220123()
    #recorrer_directorio_BRP('./brp/img/')
    #clonar_img()
    #borrar_csv()


    #imagen_categoria_Beta()
    imagen_incial()