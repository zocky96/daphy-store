from db.dbconnect import Connexion
class DalVente:
    def __init__(self):
        self.conn = Connexion()
        self.conn = self.conn.connect()
        self.cursor=self.conn.cursor()

    def cancelVente(self,id,nom_du_produit):
        self.cursor.execute("select quantite from vente where id=%s",[id])
        quantite_vendu=int(self.cursor.fetchall()[0][0])
        self.cursor.execute("select quantite from produit where nom_comercial=%s", [nom_du_produit])
        quantite_de_produit_restant = int(self.cursor.fetchall()[0][0])
        quantite_de_produit_a_restitue = quantite_de_produit_restant + quantite_vendu
        self.cursor.execute("update produit set quantite=%s where nom_comercial=%s",[quantite_de_produit_a_restitue,nom_du_produit])
        self.conn.commit()
        self.cursor.execute("delete from vente where id=%s",[id])
        self.conn.commit()
        
    def showVente(self,table):
        self.cursor.execute("select * from vente")
        rows=self.cursor.fetchall()
        table.row_data = rows
    def vente(self,Vente,date):
        self.cursor.execute("insert into vente(nom_du_produit,quantite,total,signature,date_de_vente) values(%s,%s,%s,%s,%s)",[Vente.getProductName(),int(Vente.getQuantite()),float(Vente.getTotal()),Vente.getSignature(),date])
        self.conn.commit()
        self.cursor.execute("select quantite from produit where nom_comercial=%s",[Vente.getProductName()])
        quantite_disponible = self.cursor.fetchall()[0][0]
        reste = int(quantite_disponible) - int(Vente.getQuantite())
        self.cursor.execute("update produit set quantite=%s where nom_comercial=%s",[reste,Vente.getProductName()])
        self.conn.commit()
