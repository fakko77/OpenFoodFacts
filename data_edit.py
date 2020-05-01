import mysql.connector
from constantes import *


def drop_data():
    cnx = mysql.connector.connect(user=user, password=password,
                                  host=ip,
                                  database='')

    cur = cnx.cursor()
    cur.execute("DROP DATABASE pur_beurre")
    cnx.close()






def create_data():
    cnx = mysql.connector.connect(user=user, password=password,
                                  host=ip,
                                  database='')

    cur = cnx.cursor()
    cur.execute("CREATE DATABASE pur_beurre")
    cnx.close()


