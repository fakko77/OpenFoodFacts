import mysql.connector
from constantes import ip, user, password, db


class Dataconnect:
    """ connection class """

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

    def req(self, req, *req2):
        """allows you to make a request  """
        if req2 is None:
            cur = self.cur
            cur.execute(req)
        else:
            cur = self.cur
            cur.execute(req, req2)

    def req_return(self):
        """ return result of the request """
        cur = self.cur
        return cur.fetchall()

    def close(self):
        """ close the connexion """
        con = self.con
        return con.close()

    def getProduit(self, idproduit):
        if idproduit is None:
            return None
        else:
            cur = self.cur
            cur.execute("select * from produit where id ='"
                        + str(idproduit) + "'")
            row = cur.fetchall()
            product = Produit(row[0][0], row[0][1],
                              row[0][2], row[0][3],
                              row[0][4], row[0][5], row[0][6])
            return product


class Produit:
    """ class allowing to create a product """

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
        """ class method for save a favory product in the databasse """
        if produitSub is None:
            req = "INSERT INTO favori (id_sub)"\
                  " values (%s)"
            data.req(req, str(self.id))
            data.close()
        else:
            req = "INSERT INTO favori (id_sub,id_subtitue)"\
                  " values (%s,%s)"
            data.req(req, str(self.id), str(produitSub.id))
            data.close()

    def substitution(self, data, pro):
        """class method for find a  better product """

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
                product = Produit(row[i][0], row[i][1],
                                  row[i][2], row[i][3],
                                  row[i][4], row[i][5], row[i][6])
                print(i + 1, product.nom)
                list_product.append(product)
                i += 1
            while True:
                try:
                    choix_produit = int(input("Veuillez entrer un "
                                              "nombre  : "))
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
                  "qualité  ?")
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
                produit = Produit(self.id, self.nom,
                                  self.category_id,
                                  self.description,
                                  self.magasin, self.url,
                                  self.nutri_score)
                produit.save(data)
                return 1

            else:
                data.close()
                return 1


class Category:
    """ class for creat a category """

    def __init__(self, id, nom):
        self.id = id
        self.nom = nom


class Home:
    """class home """

    def __init__(self, data):
        self.data = data

    def choix(self, val):
        """class method for check the result """
        while True:
            try:
                choix = int(input("Veuillez entrer un nombre : "))
                if choix <= val and choix > 0:
                    return choix
                    break
            except ValueError:
                print("")

    def search(self, home):
        """class method for browse the category and the product  """
        data = self.data
        data.req("SELECT * from category ")
        row = data.req_return()
        maxi = len(row)
        i = 0
        print("nombre de categories dispo:", maxi)
        while i < maxi:
            print(i + 1, row[i][1])
            i += 1

        choix = home.choix(maxi) - 1
        req = "select * from produit where category_id ='" + str(choix) + "'"
        data.req(req)
        rowproduit = data.req_return()
        maxi = len(rowproduit)
        list_product = []
        i = 0
        print("nombre de produit dispo:", maxi)
        while i < maxi:
            product = Produit(rowproduit[i][0],
                              rowproduit[i][1], rowproduit[i][2],
                              rowproduit[i][3], rowproduit[i][4],
                              rowproduit[i][5], rowproduit[i][6])
            print(i + 1, product.nom)
            list_product.append(product)
            i += 1

        choixproduit = home.choix(maxi)
        print("produit selectionner", "\n")
        choixproduit = int(choixproduit)
        print("nom:", list_product[choixproduit - 1].nom)
        print("description:", list_product[choixproduit - 1].description)
        print("magasin:", list_product[choixproduit - 1].magasin)
        print("url:", list_product[choixproduit - 1].url)
        print("nutriScrore:",
              list_product[choixproduit - 1].nutri_score)

        if list_product[choixproduit - 1].nutri_score > 1:
            print("1 - trouver un substitue de "
                  "meilleur qualité  ?")
            print("2 - Sauvegarder alliment.")
            print("3 - Nouvelle recherche.")
            choixs = home.choix(3)
            if choixs == 1:
                value = 0
                while value == 0:
                    pro = list_product[choixproduit - 1]
                    value = list_product[choixproduit - 1].substitution(data,
                                                                        pro)
                data = Dataconnect(ip, user, password, db)
                home.start()
            elif choixs == 2:
                pro = None
                list_product[choixproduit - 1].save(data, pro)
                data = Dataconnect(ip, user, password, db)
                home.start()
            elif choixs == 3:
                data.close()
                data = Dataconnect(ip, user, password, db)
                home.start()
        else:
            # TOUT MARCHE
            print("il n'existe pas mieux! ")
            print("1 - Sauvegarder alliment.")
            print("2 - Nouvelle recherche.")
            choixt = home.choix(2)
            if choixt == 1:
                list_product[choixproduit - 1].save(data)
                data = Dataconnect(ip, user, password, db)
                home.start()
            else:
                data.close()
                data = Dataconnect(ip, user, password, db)
                home.start()

    def start(self):
        """class method for lunch the home """
        data = self.data
        home = Home(data)
        # test = data.getProduit(1)
        # print(test.nom)
        print("1 - Quel aliment souhaitez-vous remplacer ?")
        print("2 - Retrouver mes aliments substitués.")
        print("3 - recrée base")
        choix = home.choix(3)
        if choix == 1:
            home.search(home)

        elif choix == 2:
            from databasse import favory_read
            data.close()
            data = Dataconnect(ip, user, password, db)
            favory_read(data)

        elif choix == 3:
            from databasse import create_table, drop_data,\
                create_data, add_entity
            drop_data()
            create_data()
            data_init = Dataconnect(ip, user, password, db)
            create_table(data_init)
            add_entity(data_init)
            data_init.close()
