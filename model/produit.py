

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
        row = data.req_return
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
