CREATE TABLE category(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100));


CREATE TABLE produit ( id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) ,
produit_id INT UNSIGNED NOT NULL,description TEXT, magasin VARCHAR(100) ,url_produit TEXT , nutri_score varchar(10) ,
CONSTRAINT fk_client_numero   foreign key (category_id) references  category (id) );



CREATE TABLE favori(id INT PRIMARY KEY  NOT NULL AUTO_INCREMENT,id_sub INT(11), id_subtitue INT(11) NUll  ,CONSTRAINT FK_Produit  FOREIGN KEY (id_sub)REFERENCES produit(id),
CONSTRAINT FK_Produit_subitue  FOREIGN KEY (id_subtitue) REFERENCES produit(id))


CREATE TABLE store ( id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,nom VARCHAR(100) )


CREATE TABLE possession (fk_produit_id INT(11) , fk_store_id INT(11),CONSTRAINT FK_PRODUIT FOREIGN KEY (fk_produit_id)REFERENCES produit(id)
,CONSTRAINT FK_STORE FOREIGN KEY (fk_store_id)REFERENCES store(id))