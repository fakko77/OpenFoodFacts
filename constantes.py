
ip = "127.0.0.1"
user = "root"
password = ""
db = "pur_beurre"
url = "https://fr.openfoodfacts.org/categories.json"
create_category = "CREATE TABLE category(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100))"

create_produit = "CREATE TABLE produit ( id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) ," \
                 " category_id INT UNSIGNED NOT NULL,description TEXT, magasin VARCHAR(100) ,url_produit TEXT , nutri_score varchar(10)" \
                 " , CONSTRAINT fk_client_numero   foreign key (category_id) references  category (id) )"
create_favori = "CREATE TABLE favori(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) , category_id INT UNSIGNED NOT NULL , url TEXT , CONSTRAINT fk_client_numero foreign key (category_id) references category (id) , id_subtitue int(11) NULL ,nom_subtitue VARCHAR(100) NULL , url_subtitue TEXT NULL) "

delete_doublons = "DELETE produit FROM produit LEFT OUTER JOIN ( SELECT MIN(id) as id, nom FROM produit GROUP BY nom ) " \
          "AS table_1 ON produit .id = table_1.id WHERE table_1.id IS NULL"


