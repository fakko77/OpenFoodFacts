import mysql.connector
from model.produit import Produit
from model.store import Store


class Dataconnect:
    """ connection class """

    def __init__(self, ip, user, password, db):
        self.ip = ip
        self.user = user
        self.password = password
        self.db = db
        self.con = mysql.connector.connect(
            host=ip,
            port=3306,
            user=user,
            password=password,
            database=db)
        self.cur = self.con.cursor()

    def req(self, req, *req2):
        """allows you to make a request  """
        if req2 is None:
            cur = self.cur
            cur.execute(req)
        else:
            cur = self.cur
            cur.execute(req, req2)

    @property
    def req_return(self):
        """ return result of the request """
        cur = self.cur
        return cur.fetchall()

    def close(self):
        """ close the connexion """
        con = self.con
        return con.close()

    def getProduit(self, idproduit):
        if idproduit is None:
            return None
        else:
            cur = self.cur
            cur.execute("select * from produit where id ='"
                        + str(idproduit) + "'")
            row = cur.fetchall()
            product = Produit(row[0][0], row[0][1],
                              row[0][2], row[0][3],
                              row[0][4], row[0][5])
            return product

    def getStore(self, idstore):
        """method class for retrieve a store according to id """
        if idstore == "101":
            store = Store(101, "unknown")
            return store
        else:
            cur = self.cur
            cur.execute("SELECT * FROM `store`"
                        " WHERE id = '" + str(idstore) + "'")
            row = cur.fetchall()
            store = Store(row[0][0], row[0][1])
            return store

    def getStoreId(self, storename):
        """method class for retrieve a store according to name """
        try:
            cur = self.cur
            cur.execute("SELECT * FROM `store`"
                        " WHERE nom = '" + str(storename) + "'")
            row = cur.fetchall()
            store = Store(row[0][0], row[0][1])
            return store
        except:
            store = Store(101, "unknown")
            return store

    def getMagasin(self,idproduit,category):
        """method class for retrieve list of store id """
        cur = self.cur
        cur.execute("SELECT * FROM `possesion`"
                    " WHERE PK_PRODUIT_ID = '" + str(idproduit) +
                    "' and `PK_CATEGORY_ID` = '" + str(category) + "'  ")
        row = cur.fetchall()
        cpt = 0
        max = len(row)
        tab = []
        while cpt < max:
            tab.append(row[cpt][1])
            cpt += 1
        return tab




