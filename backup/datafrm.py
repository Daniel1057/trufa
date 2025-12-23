import pandas as pd
import os
from sqlalchemy import create_engine
import pymysql


def carga_tarifa_beta():
    tarifa = pd.read_excel('TARIFA.xlsx')
    sqlEngine = create_engine('mysql+pymysql://Minemas_R:b1EppZu9bX6vhvMf@endurorecambios.com/Alim')
    dbConnection = sqlEngine.connect()
    tarifa.to_sql(name='tarifa_beta', con=dbConnection, if_exists='replace', index=False)
    dbConnection.close()

def carga_pruebas():
    tarifa = pd.read_excel('TARIFA.xlsx')
    print("Elimina duplicados")
    tarifa = tarifa.drop_duplicates()
    print ("Inserta datos")
    sqlEngine = create_engine('mysql+pymysql://root:admin@172.18.0.2/prestashop')
    dbConnection = sqlEngine.connect()
    tarifa.to_sql(name='tarifa_beta', con=dbConnection, if_exists='replace', index=False)
    dbConnection.close()

def cambio_ref_b(dominio,usuario,pswd,basedatos):
    dbConecction = pymysql.connect(host = '172.18.0.2',user='root',passwd = 'admin',db='prestashop')
    cur = dbConecction.cursor()
    sql_change_name = "update Alim.`tarifa_beta` a, nuevaendurorecambios.ps_product b,nuevaendurorecambios.ps_product_lang c set c.name = c.name + " - "+ b.reference  where Preu = 0 and Descripcion like '#%' and reference = cod and b.id_manufacturer = 13 and c.id_shop = b.id_shop_default and c.id_product = b.id_product"
    sql_change_ref_ps_product = "update Alim.`tarifa_beta` a, nuevaendurorecambios.ps_product b set b.reference=replace(replace(a.Descripcion,'.','') ,'#','')  where Preu = 0 and Descripcion like '#%' and reference = cod and b.id_manufacturer = 13"
    sql_change_ref_ps_product_att = "update  prestashop.ps_product b, prestashop.ps_product_attribute c set c.reference = b.reference  where b.reference <> c.reference and b.id_product = c.id_product and b.id_manufacturer = 13"
    try:
        cur.execute(sql_change_name)
        print("Update ps_product_name")
        dbConecction.commit()
        cur.execute(sql_change_ref_ps_product)
        print("Update referencias en ps_product")
        dbConecction.commit()
        cur.execute(sql_change_ref_ps_product_att)
        print("Igualando referencias entre ps_product y ps_product_attribute")
        dbConecction.commit()

    except Exception as e:
        print (e)
        dbConecction.rollback()
    dbConecction.close()



def actualiza_price(manufacturer, shop):
    dbConecction = pymysql.connect(host = '172.18.0.2',user='root',passwd = 'admin',db='prestashop')
    cur = dbConecction.cursor()
    sql_carga_temporal = "insert into Alim_update_price select id_product,price,preu,reference from ps_product, tarifa_beta where `id_shop_default` = "+str(shop)+" and `id_manufacturer` = "+str(manufacturer)+" and reference = cod and price <> Preu group by id_product,price,preu,reference"
    sql_ps_product = "update ps_product a,Alim_update_price b set a.price = Preu where `id_shop_default` = "+str(shop)+" and `id_manufacturer` = "+str(manufacturer)+" and a.id_product = b.id_product and Preu > 0"
    sql_ps_product_shop ="update ps_product_shop r, Alim_update_price b set r.price = Preu where r.id_shop = "+str(shop)+" and r.id_product = b.id_product and Preu > 0"
    sql_ps_product_shop_reference="update ps_product_attribute r, Alim_update_price s set r.`reference` = s.reference  where r.id_product = s.id_product and Preu > 0"
    sql_ps_product_shop_price = "update ps_product_attribute r, Alim_update_price s set r.`price` = s.Preu  where r.id_product = s.id_product and Preu > 0"
    sql_ps_product_attribute_shop="update ps_product_attribute_shop r, Alim_update_price s set r.price = s.preu where r.id_shop = "+str(shop)+" and r.id_product = s.id_product and Preu > 0"
    try:

        cur.execute("DELETE FROM Alim_update_price")
        print("Borrado tabla precios")
        dbConecction.commit()
        cur.execute(sql_carga_temporal)
        print("Carga de precios para la tienda "+str(shop)+" para manufacturer " + str(manufacturer))
        dbConecction.commit()
        cur.execute(sql_ps_product)
        print ("Update sql products")
        dbConecction.commit()
        cur.execute(sql_ps_product_shop)
        print("Update sql products shop")
        dbConecction.commit()
        cur.execute(sql_ps_product_shop_reference)
        print("Update sql products shop reference")
        dbConecction.commit()
        cur.execute(sql_ps_product_shop_price)
        print("Update sql products shop price")
        dbConecction.commit()
        cur.execute(sql_ps_product_attribute_shop)
        print("Update sql products shop attribute shop")
        dbConecction.commit()
    except Exception as e:
        print (e)
        dbConecction.rollback()

    dbConecction.close()
if __name__ == '__main__':
    carga_pruebas()
    actualiza_price(13,1)


#
#





