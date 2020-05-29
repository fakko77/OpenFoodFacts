import mysql.connector
from model.produit import Produit


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
                              row[0][4], row[0][5], row[0][6])
            return product
