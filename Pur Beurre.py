from fonction import *
from classes import *

home()

#SELECT COUNT(nom), nom FROM produit GROUP BY nom HAVING COUNT(nom) > 1
#DELETE produit FROM produit LEFT OUTER JOIN ( SELECT MIN(id) as id, nom FROM produit GROUP BY nom ) AS table_1 ON produit .id = table_1.id WHERE table_1.id IS NULL

 
