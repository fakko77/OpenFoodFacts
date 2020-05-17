import mysql.connector


class data_connect:
    def __init__(self, ip, user, password, db):
        self.ip = ip
        self.user = user
        self.password = password
        self.db = db
        self.con = mysql.connector.connect(
            host=ip,
            port=3306,
            user=user,
            password=password,
            database=db)
        self.cur = self.con.cursor()

    def req(self, req):
        cur = self.cur
        cur.execute(req)

    def req_return(self):
        cur = self.cur
        return cur.fetchall()

    def close(self):
        con = self.con
        return con.close()


class produit_entity:
    def __init__(self, id, nom, category_id,
                 description, magasin, url, nutri_score):
        self.id = id
        self.nom = nom
        self.category_id = str(category_id)
        self.description = description
        self.magasin = magasin
        self.url = str(url)
        self.nutri_score = int(nutri_score)

    def save(self, data, produitSub):
        if produitSub is None:

            req = "INSERT INTO favori (nom,category_id,url)" \
                  " values ('" + self.nom + "','" \
                    "" + self.category_id + "','" + self.url + "')"
            data.req(req)
            data.close()
        else:
            req = "INSERT INTO favori (nom,category_id,url," \
                  "id_subtitue,nom_subtitue,url_subtitue)" \
                  " values ('" + self.nom + "','" \
                            "" + self.category_id + "','" + self.url + "'," \
                            "'" + str(produitSub.id) + "'," \
                            "'" + produitSub.nom + "'," \
                            "'" + produitSub.url + "')"
            data.req(req)
            data.close()

    def substitution(self, data, pro):

        produitid = self.category_id
        nutri = str(self.nutri_score)
        data.req("SELECT * from produit where category_id = '" + produitid +
                 "'  and nutri_score < " + nutri + " ")
        row = data.req_return()
        maxi = len(row)
        list_product = []
        i = 0
        nb_dispo = maxi
        print("nombre de produits correspondant heo:", nb_dispo)
        if nb_dispo > 0:
            while i < maxi:
                product = produit_entity(row[i][0], row[i][1],
                                         row[i][2], row[i][3],
                                         row[i][4], row[i][5], row[i][6])
                print(i + 1, product.nom)
                list_product.append(product)
                i += 1
            while True:
                try:
                    choix_produit = int(input("Veuillez entrer un "
                                              "nombre  (dans classes 1) : "))
                    if maxi >= choix_produit > 0:
                        break
                except ValueError:
                    print("")

            print("produit selectionner", "\n")
            choix_produit = int(choix_produit)
            print("nom:", list_product[choix_produit - 1].nom)
            print("description:", list_product[choix_produit - 1].description)
            print("magasin:", list_product[choix_produit - 1].magasin)
            print("url:", list_product[choix_produit - 1].url)
            print("nutriScrore:", list_product[choix_produit - 1].nutri_score)
            print("1 - trouver un substitue de meilleur "
                  "qualité  (dans classes 1 p 2) ?")
            print("2 - Sauvegarder alliment.")
            print("3 - Nouvelle recherche.")
            while True:
                try:
                    choix = int(input("Veuillez entrer un nombre : "))
                    if maxi >= choix_produit > 0:
                        break
                except ValueError:
                    print("")
            if choix == 1:
                pro = list_product[choix_produit - 1]
                list_product[choix_produit - 1].substitution(data, pro)
            elif choix == 2:
                list_product[choix_produit - 1].save(data, pro)
                return 1
            else:
                data.close()
                return 1
        else:
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
                produit = produit_entity(self.id, self.nom,
                                         self.category_id,
                                         self.description,
                                         self.magasin, self.url,
                                         self.nutri_score)
                produit.save(data)
                return 1

            else:
                data.close()
                return 1


class category:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
