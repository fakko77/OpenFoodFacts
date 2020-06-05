IP = "127.0.0.1"
USER = "root"
PASSWORD = ""
DB = "pur_beurre"
URL = "https://fr.openfoodfacts.org/categories.json"
CREATE_CATEGORY = "CREATE TABLE category(id INT PRIMARY" \
                  " KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100))"

CREATE_PRODUIT = "CREATE TABLE produit ( id INT PRIMARY KEY NOT NULL " \
                 "AUTO_INCREMENT,nom VARCHAR(100) ," \
                 " category_id INT UNSIGNED NOT NULL,description" \
                 " TEXT, magasin VARCHAR(100)" \
                 " ,url_produit TEXT , nutri_score varchar(10)" \
                 " , CONSTRAINT fk_client_numero   foreign key (category_id)" \
                 " references  category (id) )"
CREATE_FAVORI = "CREATE TABLE favori(id INT PRIMARY KEY " \
                " NOT NULL AUTO_INCREMENT" \
                ",id_sub INT(11), id_subtitue INT(11) NUll " \
                " ,CONSTRAINT FK_Produit " \
                " FOREIGN KEY (id_sub)REFERENCES produit(id)," \
                " CONSTRAINT FK_Produit_subitue  FOREIGN KEY (id_subtitue)" \
                "REFERENCES produit(id)) "

DELETE_DOUBLONS = "DELETE produit FROM produit " \
                  "LEFT OUTER JOIN ( SELECT MIN(id) " \
                  "as id, nom FROM produit GROUP BY nom ) " \
          "AS table_1 ON produit .id = table_1.id WHERE" \
                  " table_1.id IS NULL"
