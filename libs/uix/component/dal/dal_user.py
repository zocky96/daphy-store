from db.dbconnect import Connexion
class DalUser:
    def __init__(self):
        self.conn=Connexion()
        self.conn=self.conn.connect()
        self.cursor=self.conn.cursor()
    def getFullName(self,user,passwd):
        self.cursor.execute("select nom,prenom,poste from users where user=%s and passwd=%s",[user,passwd])
        row=self.cursor.fetchall()[0]
        return [f"{str(row[0]).capitalize()} {str(row[1]).capitalize()}",row[2]]
    def saveUser(self,user):
        self.cursor.execute("insert into users (nom,prenom,user,poste,passwd,tentative,blocker,email) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                            [user.getNom(),user.getPrenom(),user.getUserName(),user.getPoste(),user.getPassord(),0,'False',user.getEmail()])
        self.conn.commit()
    def deleteUser(self,id):
        self.cursor.execute("delete from users where id=%s",[id])
        self.conn.commit()
    def modifyUser(self,user,id):
        liste = [user.getNom(),user.getPrenom(),user.getUserName(),user.getPoste(),user.getPassord(),user.getEmail(),id]
        print(liste)
        self.cursor.execute("update users set nom=%s ,prenom=%s ,user=%s ,poste=%s ,passwd=%s, email=%s where id=%s",
                            liste)
        self.conn.commit()
    def showUsers(self,table):
        self.cursor.execute("select * from users")
        rows=self.cursor.fetchall()
        liste=[]
        for row in rows:
            ligne =(row[0],row[1],row[2],row[3],row[4],row[9])
            liste.append(ligne)
        table.row_data=liste
    def login(self,Login):
        self.cursor.execute("select * from users where user=%s and passwd=%s", [Login.getUserName(), Login.getPassord()])
        rows = self.cursor.fetchall()
        return rows