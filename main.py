from data.databasse import create_data, create_table, add_entity, add_store
from view.home import Home
from data.data import Dataconnect
from constantes import IP, USER, PASSWORD, DB
import mysql.connector


def main():
    """ launches  the app """
    while True:
        try:
            data = Dataconnect(IP, USER, PASSWORD, DB)
        except mysql.connector.Error as err:
            print(err)
            print("Error Code:", err.errno)
            print("SQLSTATE", err.sqlstate)
            print("Message", err.msg)
            #afficher de l'erreur precise
            create_data()
            data_init = Dataconnect(IP, USER, PASSWORD, DB)
            create_table(data_init)
            add_store(data)
            add_entity(data_init)
            data_init.close()
        home = Home(data)
        home.start()
    # data = Dataconnect(IP, USER, PASSWORD, DB)
    # add_entity(data)



