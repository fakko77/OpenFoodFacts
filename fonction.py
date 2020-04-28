import requests
import json
from constantes import *
from classes import *


def main():
    try:
        data = data_connect(ip, user, password, db)
        home(data)
    except:
        create_data()
        data = data_connect(ip, user, password, db)
        home(data)


# data = data_connect(ip, user, password, db)
# close = data.close

# fonction permetant de crée la base de donnée
def create_data():
    data_create = data_connect(ip, user, password, "")
    data_create.req("DROP DATABASE IF EXISTS pur_beurre")
    data_create.req("CREATE DATABASE IF NOT EXISTS pur_beurre")
    data_create.close_conn()
    #data_create.close


# creation de l'objet data


# creation des tables category , produit , favori voir constantes.py
def create_table(data):
    data.req(create_category)
    data.req(create_produit)
    data.req(create_favori)
    #data.close


# l'on ajoute les categories et leurs produit à l'aide de l'api dans la base de donnée
def add_entity(data):
    maxi = len(dic)
    compteur = 0
    compteur_category = 0
    compteur_produit = 0
    while compteur < maxi:
        requette = "INSERT INTO category " \
                   "(nom) values ('" + str(dic[compteur]) + "')"
        data.req(requette)
        compteur += 1
    while compteur_category < 5:
        while compteur_produit < 100:
            print(compteur_category, str(dic[compteur_category]))
            url = "https://fr.openfoodfacts.org/cgi/search.pl?action=process" \
                  "&tagtype_0=categories&tag_contains_" \
                  "0=contains&tag_0=" + str(dic[compteur_category]) + "&json=" \
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

                    requette = "INSERT INTO produit ( nom , produit_id, description , magasin , url_produit, " \
                               "nutri_score ) values " \
                               "('" + nom + "','" + str(compteur_category) + "','description','" + store + "','" + str(
                        item_produc[i]["url"]) + "','" + nutri + "')"
                    data.req(requette)

                else:
                    nutri = "99"
                    requette = "INSERT INTO produit ( nom , produit_id, description , magasin , url_produit, " \
                               "nutri_score ) values ('" + nom + "','" + str(
                        compteur_category) + "','description','" + store + "','" + str(
                        item_produc[i]["url"]) + "','" + nutri + "')"
                    data.req(requette)
                i += 1
                # print(compteur_category)
            compteur_category += 1
            if compteur_category == 6:
                #data.close
                break
    # l'on supprime les doublons
    req = "DELETE produit FROM produit LEFT OUTER JOIN ( SELECT MIN(id) as id, nom FROM produit GROUP BY nom ) " \
          "AS table_1 ON produit .id = table_1.id WHERE table_1.id IS NULL"
    data.req(req)
    #data.close
    print("Finis")


# fonction permettant de trouver un produit de meilleurs qualité
def product_substitution(id_category, nutriscore, data):
    data.req("SELECT * from produit where produit_id = '" + str(id_category) + "'  and nutri_score < '" + str(
        nutriscore) + "' ")
    row = data.req_return()
    maxi = len(row)
    i = 0
    nb_dispo = maxi
    print("nombre de produits correspondant :", nb_dispo)
    if (nb_dispo > 0):
        while i < maxi:
            print(i + 1, row[i][1])
            i += 1
        while True:
            try:
                choix_produit = int(input("Veuillez entrer un nombre : "))
                if choix_produit <= maxi and choix_produit > 0:
                    break
            except ValueError:
                print("")

        choix_produit = int(choix_produit) - 1
        print("produit selectionner", "\n")
        print("nom:", row[int(choix_produit)][1])
        print("description:", row[int(choix_produit)][3])
        print("magasin:", row[int(choix_produit)][4])
        print("url:", row[int(choix_produit)][5])
        print("nutriScrore:", row[int(choix_produit)][6])
        # data.close()
        id_category = row[int(choix_produit)][2]
        nutriscore = row[int(choix_produit)][6]
        nom = row[int(choix_produit)][1]
        url = row[int(choix_produit)][5]
        search(id_category, nutriscore, nom, url, data)
    else:
        search(id_category, nutriscore, data)
        # data.close()


def home(data):
    print("1 - Quel aliment souhaitez-vous remplacer ?")
    print("2 - Retrouver mes aliments substitués.")
    print("3 - recrée base")
    choix = input("Veuillez entrer un nombre : ")

    if choix == '1':

        data.req("SELECT * from category ")
        row = data.req_return()
        maxi = len(row)
        i = 0
        print("nombre de categories dispo:", maxi)
        while i < maxi:
            print(i + 1, row[i][1])
            i += 1
        while True:
            try:
                choix = int(input("Veuillez selectionné une category : "))
                if choix <= maxi and choix > 0:
                    break
            except ValueError:
                print("")

        choix = int(choix) - 1
        req = "select * from produit where produit_id ='" + str(choix) + "'"
        data.req(req)
        row_produit = data.req_return()
        maxi = len(row_produit)
        i = 0
        print("nombre de produit dispo:", maxi)
        while i < maxi:
            print(i, row_produit[i][1])
            i += 1
        while True:
            try:
                choix_produit = int(input("Veuillez entrer un nombre :"))
                if choix_produit <= maxi:
                    break
            except ValueError:
                print("")
        print("produit selectionner", "\n")
        print("nom:", row_produit[int(choix_produit)][1])
        print("description:", row_produit[int(choix_produit)][3])
        print("magasin:", row_produit[int(choix_produit)][4])
        print("url:", row_produit[int(choix_produit)][5])
        print("nutriScrore:", row_produit[int(choix_produit)][6])
        # print(row_produit[int(choix_produit)][0])

        id_category = row_produit[int(choix_produit)][2]
        nutriscore = row_produit[int(choix_produit)][6]
        nom = row_produit[int(choix_produit)][1]
        url = row_produit[int(choix_produit)][5]
        search(id_category, nutriscore, nom, url, data)
    elif choix == '2':
        data.req("SELECT * from favori ")
        row = data.req_return()
        maxi = len(row)
        i = 0
        nb_dispo = maxi
        print("nombre de produits correspondant :", maxi)
        if (nb_dispo > 0):
            while i < maxi:
                print(i + 1, row[i][1], "\n")
                i += 1
        home(data)
    elif choix == '3':
        create_data()
        create_table(data)
        add_entity(data)
        home(data)

    else:
        print("selectionner nombre proposez \n")
        home(data)


# fonction permet en partie de sauvegarder les produits favoris
def search(id_category, nutriscore, nom, url, data):
    val_nutri = int(nutriscore)
    if (val_nutri > 1):

        print("1 - trouver un substitue de meilleur qualité ?")
        print("2 - Sauvegarder alliment.")
        print("3 - Nouvelle recherche.")
        while True:
            try:
                choix_s = int(input("Veuillez entrer un nombre : "))
                if choix_s <= 3 and choix_s > 0:
                    break
            except ValueError:
                print("")

        if choix_s == 1:
            product_substitution(id_category, nutriscore, data)
        elif choix_s == 2:
            save(nom, id_category, url, data)

        elif choix_s == 3:
            home(data)
    else:
        print("il n'existe pas mieux!")
        print("1 - Sauvegarder alliment.")
        print("2 - Nouvelle recherche.")

        while True:
            try:
                choix_ = int(input("Veuillez entrer un nombre : "))
                if choix_ <= 2 and choix_ > 0:
                    break
            except ValueError:
                print("")
        if choix_ == '1':

            save(nom, id_category, url, data)
        else:
            home(data)


def save(nom, id_category, url, data):
    req = "INSERT INTO favori (nom,produit_id,url )" \
          " values ('" + str(nom) + "','" \
                                    "" + str(id_category) + "','" + str(url) + "')"

    data.req(req)
    #data.close
    home(data)
