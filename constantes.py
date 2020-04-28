ip = "127.0.0.1"
user = "root"
password = ""
db = "pur_beurre"
url = "https://fr.openfoodfacts.org/categories.json"
create_category = "CREATE TABLE category(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100))"

create_produit = "CREATE TABLE produit ( id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) ," \
                 " produit_id INT UNSIGNED NOT NULL,description TEXT, magasin VARCHAR(100) ,url_produit TEXT , nutri_score varchar(10)" \
                 " , CONSTRAINT fk_client_numero   foreign key (produit_id) references  category (id) )"
create_favori = "CREATE TABLE favori(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) , produit_id INT UNSIGNED NOT NULL , url TEXT , CONSTRAINT fk_client_numero foreign key (produit_id) references  category (id) )"

dic = {0: "Produits à tartiner", 1: "Plats préparés", 2: "Céréales pour petit-déjeuner", 3: "Pizzas",
       4: "Confiseries", 5: "Boissons"}
