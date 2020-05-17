from constantes import *
from data_edit import *
from classes import produit_entity, data_connect, category


def main():
    while True:
        try:
            data = data_connect(ip, user, password, db)
            home(data)
        except:
            create_data()
            data_init = data_connect(ip, user, password, db)
            create_table(data_init)
            add_entity(data_init)
            data_init.close()


# data = data_connect(ip, user, password, db)


# fonction permetant de crée la base de donnée
# creation de l'objet data


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
        req = "select * from produit where category_id ='" + str(choix) + "'"
        data.req(req)
        row_produit = data.req_return()
        maxi = len(row_produit)
        list_product = []
        i = 0
        print("nombre de produit dispo: laaaa", maxi)
        while i < maxi:
            product = produit_entity(row_produit[i][0],
                                     row_produit[i][1], row_produit[i][2],
                                     row_produit[i][3], row_produit[i][4],
                                     row_produit[i][5], row_produit[i][6])
            print(i + 1, product.nom)
            list_product.append(product)
            i += 1
        while True:
            try:

                choix_produit = int(input("Veuillez entrer un nombre :"))
                if choix_produit <= maxi:
                    break
            except ValueError:
                print("")
        print("produit selectionner", "\n")
        choix_produit = int(choix_produit)
        print("nom:", list_product[choix_produit - 1].nom)
        print("description:", list_product[choix_produit - 1].description)
        print("magasin:", list_product[choix_produit - 1].magasin)
        print("url:", list_product[choix_produit - 1].url)
        print("nutriScrore:",
              list_product[choix_produit - 1].nutri_score)

        if list_product[choix_produit - 1].nutri_score > 1:
            print("1 - trouver un substitue de "
                  "meilleur qualité   test boucle ?")
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
                value = 0
                while value == 0:
                    pro = list_product[choix_produit - 1]
                    value = list_product[choix_produit - 1].substitution(data,
                                                                         pro)
                data = data_connect(ip, user, password, db)
                home(data)
            elif choix_s == 2:
                pro = None
                list_product[choix_produit - 1].save(data, pro)
                data = data_connect(ip, user, password, db)
                home(data)
            elif choix_s == 3:
                data.close()
                data = data_connect(ip, user, password, db)
                home(data)
        else:
            # TOUT MARCHE
            print("il n'existe pas mieux! ")
            print("1 - Sauvegarder alliment.")
            print("2 - Nouvelle recherche.")
            while True:
                try:
                    choix_t = int(input("Veuillez entrer un nombre : "))
                    if choix_t <= 2 and choix_t > 0:
                        break
                except ValueError:
                    print("")
            if choix_t == 1:
                list_product[choix_produit - 1].save(data)
                data = data_connect(ip, user, password, db)
                home(data)
            else:
                data.close()
                data = data_connect(ip, user, password, db)
                home(data)

    elif choix == '2':
        favory_read(data)

    elif choix == '3':
        drop_data()
        create_data()
        data_init = data_connect(ip, user, password, db)
        create_table(data_init)
        add_entity(data_init)
        data_init.close()
        data = data_connect(ip, user, password, db)
        home(data)

    else:
        print("selectionner nombre proposez \n")
        home(data)
