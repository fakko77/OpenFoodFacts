import mysql.connector
import requests
import json
from fonction import *
from classes import produit_entity, data_connect, category

dic = {0: category("1", "Produits à tartiner"),
       1: category("2", "Plats préparés"),
       2: category("3", "Céréales pour petit-déjeuner"),
       3: category("4", "Pizzas"),
       4: category("5", "Confiseries"),
       5: category("6", "Boissons")}


def drop_data():
    cnx = mysql.connector.connect(user=user, password=password,
                                  host=ip,
                                  database='')

    cur = cnx.cursor()
    cur.execute("DROP DATABASE pur_beurre")
    cnx.close()


def create_data():
    cnx = mysql.connector.connect(user=user, password=password,
                                  host=ip,
                                  database='')

    cur = cnx.cursor()
    cur.execute("CREATE DATABASE pur_beurre")
    cnx.close()


def favory_read(data):
    from fonction import home
    data.req("SELECT * from favori ")
    row = data.req_return()
    maxi = len(row)
    i = 0
    nb_dispo = maxi
    print("nombre de produits correspondant :", maxi)
    if (nb_dispo > 0):
        while i < maxi:
            print(i + 1, row[i][1], "/produit subtitué =>", row[i][5], "\n")
            i += 1
    data.close()
    data = data_connect(ip, user, password, db)
    home(data)


# creation des tables category , produit , favori voir constantes.py
def create_table(data):
    data.req(create_category)
    data.req(create_produit)
    data.req(create_favori)


# l'on ajoute les categories et leurs produit
# à l'aide de l'api dans la base de donnée
def add_entity(data):
    maxi = len(dic)
    compteur = 0
    compteur_category = 0
    compteur_produit = 0
    while compteur < maxi:
        requette = "INSERT INTO category " \
                   "(nom) values ('" + str(dic[compteur].nom) + "')"
        data.req(requette)
        compteur += 1
    while compteur_category < 5:
        while compteur_produit < 100:
            print(compteur_category, str(dic[compteur_category].nom))
            url = "https://fr.openfoodfacts." \
                  "org/cgi/search.pl?action=process" \
                  "&tagtype_0=categories&tag_contains_" \
                  "0=contains&tag_0=" + str(dic[compteur_category].nom) + "&json=" \
                                                                          "true&page_size=100"
            payload = {}
            headers = {}
            response = requests.request("GET", url,
                                        headers=headers, data=payload)
            json_data = json.dumps(response.json())
            item_dict = json.loads(json_data)
            item_produc = item_dict["products"]
            i = 0
            while i < 100:
                if "nutriscore_score" in item_produc[i]:
                    nutri = str(item_produc[i]["nutriscore_score"])
                    nom = str(item_produc[i]["product_name"]).replace("""'""", "")
                    store = str(item_produc[i]["stores"]).replace("""'""", "")
                    produit = produit_entity(i, nom, compteur_category, "desc", store, item_produc[i]["url"], nutri)

                    # print("INSERT INTO produit ( nom , category_id, description , magasin , url_produit, " \
                    #            "nutri_score ) values ('" + produit.nom + "','" + produit.category_id + "','"+ produit.description+ "', '" + produit.magasin + "','" + produit.url + "','" + str(produit.nutri_score) + "')")
                    #

                    requette = "INSERT INTO produit ( nom , category_id, description , magasin , url_produit, " \
                               "nutri_score ) values ('" + produit.nom + "','" + produit.category_id + "','" + produit.description + "', '" + produit.magasin + "','" + produit.url + "','" + str(produit.nutri_score) + "')"
                    data.req(requette)

                else:
                    nutri = "99"
                    produit = produit_entity(i, nom, compteur_category, "desc", store, item_produc[i]["url"], nutri)
                    requette = "INSERT INTO produit ( nom , category_id, description , magasin , url_produit, " \
                               "nutri_score ) values ('" + produit.nom + "','" + produit.category_id + "','" + produit.description + "', '" + produit.magasin + "','" + produit.url + "','" + str(produit.nutri_score) + "')"
                    data.req(requette)
                i += 1
            compteur_category += 1
            if compteur_category == 6:
                break
    # l'on supprime les doublons
    req = delete_doublons
    data.req(req)