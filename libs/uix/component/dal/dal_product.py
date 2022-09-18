from db.dbconnect import Connexion
class DalProduct:
    def __init__(self):
        self.conn=Connexion()
        self.conn = self.conn.connect()
        self.cursor=self.conn.cursor()
    def getProductType(self):
        self.conn.close()
        self.conn = Connexion()
        liste = []
        self.conn = self.conn.connect()
        self.cursor = self.conn.cursor()
        self.cursor.execute("select type_produit from produit")
        rows=self.cursor.fetchall()
        for row in rows:
            theType=row[0]
            if theType in liste:
                pass
            else:
                liste.append(theType)
        return len(liste)
    def countProduct(self):
        self.conn.close()
        self.conn = Connexion()
        self.conn = self.conn.connect()
        self.cursor = self.conn.cursor()
        self.cursor.execute("select count(*) from produit")
        nbr=self.cursor.fetchall()
        return nbr
    def showProducts(self,table):
        self.conn.close()
        self.conn=Connexion()
        self.conn = self.conn.connect()
        self.cursor = self.conn.cursor()
        self.cursor.execute("select * from produit")
        rows=self.cursor.fetchall()
        table.row_data=rows
    def modifyProduct(self,Produit,id):
        self.cursor.execute("update produit set nom_comercial=%s,nom_pharmaceutique=%s,prix=%s,quantite=%s,nom_du_fournisseur=%s,phone_fournisseur=%s,type_produit=%s where id=%s",[Produit.getNomComercial(),Produit.getNomPharmaceutique(),Produit.getPrix(),Produit.getQuantite(),Produit.getNomDuFournisseur(),Produit.getPhoneFournisseur(),Produit.getTypeOfProduct(),int(id)])
        self.conn.commit()
    def deleteProduct(self,id):
        self.cursor.execute("delete from produit where id=%s",[id])
        self.conn.commit()
    def saveProduct(self,Produit,date):
        self.cursor.execute("insert into produit(nom_comercial,nom_pharmaceutique,prix,quantite,nom_du_fournisseur,phone_fournisseur,type_produit,date_save,stock) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",[Produit.getNomComercial(),Produit.getNomPharmaceutique(),Produit.getPrix(),Produit.getQuantite(),Produit.getNomDuFournisseur(),Produit.getPhoneFournisseur(),Produit.getTypeOfProduct(),date,Produit.getQuantite()])
        self.conn.commit()

    def getProductName(self):
        self.cursor.execute("select nom_comercial,prix,quantite from produit")
        rows=self.cursor.fetchall()
        return rows
    def getStock(self):
        self.conn.close()
        self.conn = Connexion()
        self.conn = self.conn.connect()
        self.cursor = self.conn.cursor()
        self.cursor.execute("select stock,quantite from produit")
        rows = self.cursor.fetchall()
        return rows
    def getSommeCash(self):
        self.conn.close()
        self.conn = Connexion()
        self.conn = self.conn.connect()
        self.cursor = self.conn.cursor()
        self.cursor.execute("select prix,quantite from produit")
        cash=self.cursor.fetchall()
        my_cash = 0
        for data in cash:
            price=float(data[0])
            quantite = data[1]
            somme = price * quantite
            my_cash += somme
        return my_cash