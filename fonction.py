import mysql.connector
import requests
import json
import time



url = "https://fr.openfoodfacts.org/categories.json"
#url = "https://fr.openfoodfacts.org/states.json"

def create_data():
    cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="")
    cur = cnx.cursor()
    cur.execute("DROP DATABASE IF EXISTS pur_beurre")
    cur.execute("CREATE DATABASE IF NOT EXISTS pur_beurre ")
    cnx.close()
    
def create_table():
    cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="pur_beurre")
    cur = cnx.cursor()
    cur.execute("CREATE TABLE category(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100))")
    cur.execute("CREATE TABLE produit ( id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) , produit_id INT UNSIGNED NOT NULL,description TEXT , magasin VARCHAR(100) ,url_produit TEXT , nutri_score varchar(10) , CONSTRAINT fk_client_numero   foreign key (produit_id) references  category (id) )")
    cur.execute("CREATE TABLE favori(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) , produit_id INT UNSIGNED NOT NULL , url TEXT , CONSTRAINT fk_client_numero   foreign key (produit_id) references  category (id) )")
    cnx.close()
def ajout_category():
    cnx = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="",
    database="pur_beurre")
    dic = {}
    dic[0] = "Produits à tartiner"
    dic[1] = "Plats préparés"
    dic[2] = "Céréales pour petit-déjeuner"
    dic[3] = "Pizzas"
    dic[4] = "Confiseries"
    dic[5] = "Boissons"
    maxi = len(dic)
    compteur = 0
    compteur_category = 0
    compteur_produit = 0
    cur = cnx.cursor()
    while compteur < maxi :
        req = "INSERT INTO category (nom ) values ('"+ str(dic[compteur]) +"')"
        req = str(req) 
        #print(type(req))
        #print(req)
        cur.execute(req)
        compteur+=1
    while compteur_category < 5:
        while compteur_produit < 100:
            print(compteur_category,str(dic[compteur_category]))
            url = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0="+ str(dic[compteur_category])+"&json=true&page_size=100"
            payload = {}
            headers= {}
            response = requests.request("GET", url, headers=headers, data = payload)
            json_data = json.dumps(response.json())
            item_dict = json.loads(json_data)
            item_produc = item_dict["products"]
            i = 0
            while i < 100:
                if "nutriscore_score" in item_produc[i]:
                    nutri = str(item_produc[i]["nutriscore_score"])
                    nom = str(item_produc[i]["product_name"]).replace("""'""", "")
                    store = str(item_produc[i]["stores"]).replace("""'""", "")
                   
                    req = "INSERT INTO produit ( nom , produit_id, description , magasin , url_produit, nutri_score ) values ('" + nom + "','" + str(
                        compteur_category) + "','description','" + store +"','" + str(item_produc[i]["url"])+"','" + nutri  +"')"
                    cur.execute(req)
                    
                else:
                    nutri = "99"
                    req = "INSERT INTO produit ( nom , produit_id, description , magasin , url_produit, nutri_score ) values ('" + nom + "','" + str(
                        compteur_category) + "','description','" + store +"','" + str(item_produc[i]["url"])+"','" + nutri  +"')"
                    cur.execute(req)
                i+=1
                #print(compteur_category)
            compteur_category+=1
            if compteur_category == 6:
                break
    req = "DELETE produit FROM produit LEFT OUTER JOIN ( SELECT MIN(id) as id, nom FROM produit GROUP BY nom ) AS table_1 ON produit .id = table_1.id WHERE table_1.id IS NULL"
    cur.execute(req)
    cnx.close()
    print("Finis")

                    
                #req = "INSERT INTO category (id , nom , produit_id, description , magasin , url_produit, nutri_score ) values ('"+ str(i) + "','"+ str(item_produc[i]["product_name"]) +"','"+ str(compteur_category) + "','"+ str(item_produc[i]["data_sources_tags"]) + "','"+ str(item_produc[i]["url"]) + "','"+ str(item_produc[i]["nutrition-score-fr"]) + "')"
                
                    
                                
                
                
                
        
        
    

def product_substitution(id_category,nutriscore):
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="pur_beurre")
    cur = cnx.cursor()
    cur.execute("SELECT * from produit where produit_id = '" + str(id_category) +"'  and nutri_score < '" + str(nutriscore) +"' ")
    row = cur.fetchall()
    maxi = len(row)
    i = 0
    nb_dispo = cur.rowcount
    print("nombre de produits correspondant :", cur.rowcount)
    if(nb_dispo > 0):
        while i < maxi:
            print(i + 1 ,row[i][1])
            i += 1
        while True:
            try:
                choix_produit  = int(input("Veuillez entrer un nombre : "))
                if choix_produit <= maxi  and choix_produit > 0:
                    break
            except ValueError:
                print("")
        
        choix_produit = int(choix_produit)-1
        print("produit selectionner","\n")
        print("nom:",row[int(choix_produit)][1])
        print("description:",row[int(choix_produit)][3])
        print("magasin:",row[int(choix_produit)][4])
        print("url:",row[int(choix_produit)][5])
        print("nutriScrore:",row[int(choix_produit)][6])
        cnx.close()
        id_category = row[int(choix_produit)][2]
        nutriscore = row[int(choix_produit)][6]
        nom = row[int(choix_produit)][1]
        url = row[int(choix_produit)][5]
        save(id_category,nutriscore,nom,url)
    else:
        save(id_category,nutriscore)
        
    
    
def home():
    print("1 - Quel aliment souhaitez-vous remplacer ?")
    print("2 - Retrouver mes aliments substitués.")
    print("3 - recrée base")
    choix =input("Veuillez entrer un nombre : ")

    if choix == '1':
        cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="pur_beurre")
        cur = cnx.cursor()
        cur.execute("SELECT * from category ")
        row = cur.fetchall()
        maxi = len(row)
        i = 0
        print("nombre de categories dispo:", cur.rowcount)
        while i < maxi:
            print(i + 1 ,row[i][1])
            i += 1
        while True:
            try:    
                choix =int(input("Veuillez selectionné une category : "))
                if choix <= maxi  and choix > 0:
                    break
            except ValueError:
                print("")
        
        choix = int(choix) - 1 
        req = "select * from produit where produit_id ='" + str(choix)+ "'"
        cur.execute(req)
        row_produit = cur.fetchall()
        maxi = len(row_produit)
        i = 0
        print("nombre de produit dispo:", cur.rowcount)
        while i < maxi:
            print(i,row_produit[i][1])
            i += 1
        while True:
            try:    
                choix_produit  =int(input("Veuillez entrer un nombre :"))
                if choix_produit <= maxi:
                    break
            except ValueError:
                print("")
        print("produit selectionner","\n")
        print("nom:",row_produit[int(choix_produit)][1])
        print("description:",row_produit[int(choix_produit)][3])
        print("magasin:",row_produit[int(choix_produit)][4])
        print("url:",row_produit[int(choix_produit)][5])
        print("nutriScrore:",row_produit[int(choix_produit)][6])
        #print(row_produit[int(choix_produit)][0])
        cnx.close()
        id_category = row_produit[int(choix_produit)][2]
        nutriscore = row_produit[int(choix_produit)][6]
        nom = row_produit[int(choix_produit)][1]
        url = row_produit[int(choix_produit)][5]
        save(id_category,nutriscore,nom,url)
        
 
    elif choix == '2':
        cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="pur_beurre")
        cur = cnx.cursor()
        cur.execute("SELECT * from favori ")
        row = cur.fetchall()
        maxi = len(row)
        i = 0
        nb_dispo = cur.rowcount
        print("nombre de produits correspondant :", cur.rowcount)
        if(nb_dispo > 0):
            while i < maxi:
                print(i + 1 ,row[i][1],"\n")
                i += 1
        home()
    elif choix == '3': 
        create_data()
        create_table()
        ajout_category()
        home()
            
    else :
        print("selectionner nombre proposez \n")
        home()
def save(id_category,nutriscore,nom,url):
    val_nutri = int(nutriscore)
    if (val_nutri > 0):
        print("DANS SAVE")
        print("1 - trouver un substitue de meilleur qualité ?")
        print("2 - Sauvegarder alliment.")
        print("3 - Nouvelle recherche.")
        while True:
            try:
                choix_s  = int(input("Veuillez entrer un nombre : "))
                if choix_s <= 3 and choix_s > 0:
                    break
            except ValueError:
                print("")
        

        if choix_s == 1:
            product_substitution( id_category,nutriscore)
        elif choix_s == 2:
            cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="pur_beurre")
            cur = cnx.cursor()
            req = "INSERT INTO favori (nom,produit_id,url ) values ('"+ str(nom) +"','"+ str(id_category) +"','"+ str(url) +"')"
            req = str(req)
            cur.execute(req)
            cnx.close()
            home()
        elif choix_s == 3 :
            home()
    else:
        print("il n'existe pas mieux!")
        print("1 - Sauvegarder alliment.")
        print("2 - Nouvelle recherche.")
        choix_  =input("Veuillez entrer un nombre : ")
        if(choix_ == '1'):
            cnx = mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="",
            database="pur_beurre")
            cur = cnx.cursor()
            req = "INSERT INTO favori (nom,produit_id,url ) values ('"+ str(nom) +"','"+ str(id_category) +"','"+ str(url) +"')"
            req = str(req)
            cur.execute(req)
            cnx.close()
            home()
        else:
            home()


##        payload = {}
##        headers= {}
##        response = requests.request("GET", url, headers=headers, data = payload)
##        print(response)
##        #print(response.text)
##        print(type(response))
##        json_data = json.dumps(response.json())
##        item_dict = json.loads(json_data)
##        item = len(item_dict["tags"])
##        print("quantité ",item)
##        x = 0
##        categories = []
##   
##        while x < 500:
##           
##            print ( x, item_dict["tags"][x]["name"] )
##            x+=1 
##        choixs =input("Veuillez entrer un nombre : ")
##        choixs = int(choixs)
##        url_item = item_dict["tags"][choixs]["url"]+".json"
##        print(url_item)
##        payload = {}
##        headers= {}
##        response_produc = requests.request("GET", url_item, headers=headers, data = payload)
##
##    
##        json_produc = json.dumps(response_produc.json())
##        produc_dict = json.loads(json_produc)
##        item_produc_len = len(produc_dict["products"])
##        item_produc = produc_dict["products"]
##        
##        print("nombre de produit:",item_produc_len)
##        i = 0
##        categories = []
##   
##        while i < item_produc_len:
##           
##            print ( i, item_produc[i]["product_name"] )
##            i+=1
##            
##        choix_alliment =input("Veuillez choisir un alliment: ")
##        choix_alliment = int(choix_alliment)
##        print (  item_produc[choix_alliment]["product_name"] )
##        print(item_produc[choix_alliment])
##        print(item_produc[choix_alliment]["image_nutrition_small_url"])
        
        
       
            
        

