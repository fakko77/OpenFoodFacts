from databasse import create_data, create_table, add_entity
from classes import Dataconnect, Home
from constantes import ip, user, password, db


def main():
    """ launches  the app """
    while True:
        try:
            data = Dataconnect(ip, user, password, db)
            home = Home(data)
            home.start()
        except Exception as e:
            print(e)
            create_data()
            data_init = Dataconnect(ip, user, password, db)
            create_table(data_init)
            add_entity(data_init)
            data_init.close()
