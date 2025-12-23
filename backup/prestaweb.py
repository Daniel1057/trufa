from __future__ import print_function

import pandas as pd
from prestapyt import PrestaShopWebServiceDict
from xml.etree import ElementTree

def change_price(df):
    prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    xml_prod = prestashop.get('products', '156810')
    xml_prod['product']['price']

    print(xml_prod)
def ps_web_catego_producto(df,manufacturer):

    prestashop = PrestaShopWebServiceDict('http://endurorecambios.com/api', '6641LD9XJAL6YL34Z35JLNJPJ6UCRZW1')
    #xml_cate = prestashop.get('categories', options={'schema': 'blank'})
    if (manufacturer == '13'):
        categorias = df['modelo'].unique()
        nueva_categoria = True
    for categoria in categorias:
        alim_categoria = "ALIM_"+categoria
        link = categoria.replace(" ","_")
        new_catego = {
            'category': {'id': '', 'id_parent': '149379', 'active': '0', 'id_shop_default': '1', 'is_root_category': '','position': '', 'date_add': '', 'date_upd': '', 'name': {'language': [{'attrs': {'id': '1'}, 'value': str(alim_categoria)},{'attrs': {'id': '2'}, 'value': str(alim_categoria)}]}, 'link_rewrite': {'language': [{'attrs': {'id': '1'}, 'value': str(link)},{'attrs': {'id': '2'}, 'value': str(link)}]}, 'description': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},'meta_title': {
                             'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                         'meta_description': {
                             'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                         'meta_keywords': {
                             'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                         'associations': {'categories': {'category': {'id': ''}}, 'products': {'product': {'id': ''}}}}}
        cat = prestashop.add('categories', new_catego)
        cat_padre = prestashop.search('categories', options={'filter[name]': str(alim_categoria)})
        df_categorias_hijas = df[df['modelo'] == categoria]
        categorias_hijas = df_categorias_hijas['componente'].unique()
        for hija in categorias_hijas:
            #Crear categoria hija refrenciadas al padre
            alim_categoria = "ALIM_" + hija
            link = hija.replace(" ", "_")
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
                referencia =str(df_producto_hijas['Part Number'][i])
                posicion = str(df_producto_hijas['Ref.'][i])
                cantidad = str(df_producto_hijas['Parts'][i])
                descripcion = str(df_producto_hijas['Descripcion_x'][i])
                moto = str(df_producto_hijas['modelo'][i])
                nombre = referencia + " - " + moto
                descripcion = str(posicion)+" - "+str(descripcion)+" en este despiece hacen falta "+str(cantidad)+" und - "+str(moto)+" - "+str(referencia)
                precio = str(df_producto_hijas['Preu_x'][i])
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
                                            'on_sale': '1', 'online_only': '', 'ecotax': '', 'minimal_quantity': '',
                                            'low_stock_threshold': '', 'low_stock_alert': '', 'price': str(precio),
                                            'wholesale_price': '', 'unity': '', 'unit_price_ratio': '',
                                            'additional_shipping_cost': '', 'customizable': '', 'text_fields': '',
                                            'uploadable_files': '', 'active': '0', 'redirect_type': '',
                                            'id_type_redirected': '', 'available_for_order': '', 'available_date': '',
                                            'show_condition': '', 'condition': '', 'show_price': '', 'indexed': '',
                                            'visibility': '', 'advanced_stock_management': '', 'date_add': '',
                                            'date_upd': '', 'pack_stock_type': '', 'meta_description': {
                        'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]},
                                            'meta_keywords': {'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                           {'attrs': {'id': '2'}, 'value': ''}]},
                                            'meta_title': {'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                        {'attrs': {'id': '2'}, 'value': ''}]},
                                            'link_rewrite': {'language': [{'attrs': {'id': '1'}, 'value': ''},
                                                                          {'attrs': {'id': '2'}, 'value': ''}]},
                                            'name': {'language': [{'attrs': {'id': '1'}, 'value': str(nombre)},
                                                                  {'attrs': {'id': '2'}, 'value': str(nombre)}]},
                                            'description': {'language': [{'attrs': {'id': '1'}, 'value': str(descripcion)},
                                                                         {'attrs': {'id': '2'}, 'value': str(descripcion)}]},
                                            'description_short': {'language': [{'attrs': {'id': '1'}, 'value': str(descripcion)},
                                                                               {'attrs': {'id': '2'}, 'value': str(descripcion)}]},
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
                print(data_product)
                prestashop.add('products', data_product)


    #for i in df.index:


    #cat_prod = prestashop.search('categories', options={'filter[name]': str(categoria)})
    #data_product = {'product': {'id': '', 'id_manufacturer': str(manufacturer), 'id_supplier': '', 'id_category_default': cat_prod, 'new': '', 'cache_default_attribute': '', 'id_default_image': '', 'id_default_combination': '', 'id_tax_rules_group': '17', 'position_in_category': '', 'type': '', 'id_shop_default': '1', 'reference': str(referencia), 'supplier_reference': '', 'location': '', 'width': '', 'height': '', 'depth': '', 'weight': '', 'quantity_discount': '', 'ean13': '', 'isbn': '', 'upc': '', 'cache_is_pack': '', 'cache_has_attachments': '', 'is_virtual': '', 'state': '1', 'additional_delivery_times': '', 'delivery_in_stock': {'language': [{'attrs': {'id': '1'}, 'value': str(descrpcion)}, {'attrs': {'id': '2'}, 'value': str(descrpcion)}]}, 'delivery_out_stock': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'on_sale': '1', 'online_only': '', 'ecotax': '', 'minimal_quantity': '', 'low_stock_threshold': '', 'low_stock_alert': '', 'price': '1', 'wholesale_price': '', 'unity': '', 'unit_price_ratio': '', 'additional_shipping_cost': '', 'customizable': '', 'text_fields': '', 'uploadable_files': '', 'active': '0', 'redirect_type': '', 'id_type_redirected': '', 'available_for_order': '', 'available_date': '', 'show_condition': '', 'condition': '', 'show_price': '', 'indexed': '', 'visibility': '', 'advanced_stock_management': '', 'date_add': '', 'date_upd': '', 'pack_stock_type': '', 'meta_description': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'meta_keywords': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'meta_title': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'link_rewrite': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'name': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'description': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'description_short': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'available_now': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'available_later': {'language': [{'attrs': {'id': '1'}, 'value': ''}, {'attrs': {'id': '2'}, 'value': ''}]}, 'associations': {'categories': {'category': {'id': ''}}, 'images': {'image': {'id': ''}}, 'combinations': {'combination': {'id': ''}}, 'product_option_values': {'product_option_value': {'id': ''}}, 'product_features': {'product_feature': {'id': '', 'id_feature_value': ''}}, 'tags': {'tag': {'id': ''}}, 'stock_availables': {'stock_available': {'id': '', 'id_product_attribute': ''}}, 'accessories': {'product': {'id': ''}}, 'product_bundle': {'product': {'id': '', 'id_product_attribute': '', 'quantity': ''}}}}}
    #print(prestashop.add('products', data_product))

    #category = prestashop.get('categories',149379)
    #product = prestashop.get('products', 209223)
    #print(product)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #ps_web('Alim_1','13','Neus','Neus',True)
    df_completo = pd.read_excel('df_completo.xlsx')
    #ps_web_catego_producto(df_completo,'13')
    change_price()