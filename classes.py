import mysql.connector


class data_connect:
    def __init__(self,ip,user,password,db):

        self.ip = ip
        self.user = user
        self.password = password
        self.db = db
        
        conn = mysql.connector.connect(
        host= ip,
        port=3306,
        user= user ,
        password= password,
        database= db )
        cur = conn.cursor(buffered=True)
        self.con = conn
        self.cur = cur
        self.close = conn.close

    def req(self,req):
        cur = self.cur
        cur.execute(req)

    def req_return(self):
        cur = self.cur
        return cur.fetchall()
    
        


    
    
        
        
        
        
    
