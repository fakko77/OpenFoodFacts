CREATE TABLE category(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100));
CREATE TABLE produit ( id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) ,
produit_id INT UNSIGNED NOT NULL,description TEXT, magasin VARCHAR(100) ,url_produit TEXT , nutri_score varchar(10) ,
CONSTRAINT fk_client_numero   foreign key (produit_id) references  category (id) );
CREATE TABLE favori(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) , produit_id INT UNSIGNED NOT NULL ,
url TEXT , CONSTRAINT fk_client_numero foreign key (produit_id) references  category (id) );