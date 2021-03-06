import json

import mysql.connector
import requests

from constantes import IP,USER,PASSWORD,CREATE_CATEGORY,CREATE_PRODUIT,CREATE_FAVORI,DELETE_DOUBLONS,CREATE_TABSTORE,\
    CREATE_POSSESION
from model.category import Category
from model.produit import Produit

dic={0: Category("1","Produits à tartiner"),1: Category("2","Plats préparés"),
     2: Category("3","Céréales pour petit-déjeuner"),3: Category("4","Pizzas"),4: Category("5","Confiseries"),
     5: Category("6","Boissons")}


def drop_data():
    """ delete databasse """
    cnx=mysql.connector.connect(user=USER,password=PASSWORD,host=IP,database='')
    cur=cnx.cursor()
    cur.execute("DROP DATABASE pur_beurre")
    cnx.close()


def create_data():
    """ create a new databasse purbeurre"""
    cnx=mysql.connector.connect(user=USER,password=PASSWORD,host=IP,database='')
    cur=cnx.cursor()
    cur.execute("CREATE DATABASE pur_beurre")
    cnx.close()


def favory_read(data):
    """ read all favory in the table favori """

    data.req("SELECT * from favori ")
    row=data.req_return
    maxi=len(row)
    i=0
    nb_dispo=maxi
    print("nombre de produits correspondant :",maxi)
    if (nb_dispo > 0):
        while i < maxi:
            if data.getProduit(row[i][2]) is None:
                produit1=data.getProduit(row[i][1])
                print(i+1,produit1.nom,"\n")
            else:
                produit1=data.getProduit(row[i][1])
                produit2=data.getProduit(row[i][2])
                print(i+1,produit1.nom,"produit subtitué =>",produit2.nom,"\n")

            i+=1
    data.close()


def create_table(data):
    """ create the database produit , favori , categorie"""
    data.req(CREATE_CATEGORY)
    data.req(CREATE_PRODUIT)
    data.req(CREATE_FAVORI)
    data.req(CREATE_TABSTORE)
    data.req(CREATE_POSSESION)


def add_category(data,list):
    """add category"""
    requette="INSERT INTO category "\
             "(nom) values (%s)"
    data.req(requette,list)


# def add_category_db(data):
#     maxi = len(dic)
#     compteur = 0
#     while compteur < maxi:
#         add_category(data, str(dic[compteur].nom))
#         compteur += 1
#         print(str(dic[0].nom))


def add_entity(data):
    """retrieves and adds the products to the database """
    maxi=len(dic)
    compteur=0
    compteur_category=0
    compteur_produit=0
    while compteur < maxi:
        add_category(data,str(dic[compteur].nom))
        compteur+=1
    while compteur_category < 5:
        while compteur_produit < 100:
            try:
                print(compteur_category,str(dic[compteur_category].nom))
                r=requests.get("https://fr.openfoodfacts."
                               "org/cgi/search.pl?action=process"
                               "&tagtype_0=categories&tag_contains_"
                               "0=contains&tag_0="+str(dic[compteur_category].nom)+"&json=true&page_size=100")

                json_data=json.dumps(r.json())
                item_dict=json.loads(json_data)
                item_produc=item_dict["products"]
                i=0
            except Exception as e:
                print(e)
                print("Erreur Api")
            while i < 100:
                if "nutriscore_score" in item_produc[i]:
                    nutri=str(item_produc[i]["nutriscore_score"])
                    nom=str(item_produc[i]["product_name"]).replace("""'""","")
                    tab=str(item_produc[i]["stores"]).split(",")
                    tablen=len(tab)
                    tablen=tablen
                    cptstore=0

                    # store = str(tabIdStore)
                    # store = store.replace("[", "")
                    # store = store.replace("]", "")
                    produit=Produit(i,nom,compteur_category+1,"desc",item_produc[i]["url"],nutri)

                    requette="INSERT INTO produit ( nom ,"\
                             " category_id, description "\
                             ", url_produit, "\
                             "nutri_score ) values (%s, %s, %s, %s, %s)"
                    data.req(requette,produit.nom,produit.category_id,produit.description,produit.url,
                        str(produit.nutri_score))
                    data.req(
                        "select id from produit where nom ='"+produit.nom+"' and url_produit = '"+produit.url+"' and nutri_score = '"+str(
                            produit.nutri_score)+"'  ")
                    row=data.req_return

                else:
                    nutri="99"
                    produit=Produit(i,nom,compteur_category+1,"desc",item_produc[i]["url"],nutri)
                    requette="INSERT INTO produit ( nom ,"\
                             " category_id, description "\
                             ", url_produit, "\
                             "nutri_score ) values (%s, %s, %s, %s, %s)"
                    data.req(requette,produit.nom,produit.category_id,produit.description,produit.url,
                        str(produit.nutri_score))
                while cptstore < tablen:
                    # print("tab len ", tablen)
                    nom_store = tab[cptstore].replace(" ","-")
                    store = data.getStoreId(nom_store)
                    # print(store.nom, store.id)
                    requette="INSERT INTO possession (fk_produit_id"\
                             " ,fk_store_id  ) values (%s, %s)"

                    data.req(requette,row[0][0],int(store.id))
                    # print("tab index : ",tabIdStore[cptstore])
                    cptstore+=1
                i+=1
            compteur_category+=1
            if compteur_category == 6:
                break
    # l'on supprime les doublons
    req=DELETE_DOUBLONS
    data.req(req)


def add_store(data):
    """methode for add the name of store in the db"""
    cpt=0
    tab=[]
    print("loading")
    while cpt < 100:
        r=requests.get("https://fr.openfoodfacts.org/magasins.json")
        json_data=json.dumps(r.json())
        item_dict=json.loads(json_data)
        tab.append(item_dict["tags"][cpt])
        requette=" INSERT INTO STORE ( nom ) values (%s)"
        val=tab[cpt]["id"]
        data.req(requette,val)
        cpt+=1
        if cpt < 100:
            print(cpt,"%")
        else:
            print("finish")
