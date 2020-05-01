import mysql.connector
from constantes import *


class data_connect:
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


    def req(self, req):
        cur = self.cur
        cur.execute(req)

    def req_return(self):
        cur = self.cur
        return cur.fetchall()
    def close(self):
        con = self.con
        return con.close()

