from db.dbconnect import Connexion
class DalCart:
    def __init__(self):
        self.conn = Connexion()
        self.conn = self.conn.connect()
        self.cursor=self.conn.cursor()

    def cancelCart(self,id,table):
        self.cursor.execute("delete from cart where id=%s",[id])
        self.conn.commit()
        self.showCart(table)
    def clearCart(self,table):
        self.cursor.execute("delete from cart ")
        self.conn.commit()
        self.showCart(table)
    def getSum(self):
        self.cursor.execute("select sum(total) from cart")
        row = self.cursor.fetchall()[0][0]
        return row
    def saveToCart(self,Cart,signature,datee):
        self.cursor.execute(
            "insert into cart(nom_du_produit,quantite,total,prix,signature,datee) values(%s,%s,%s,%s,%s,%s)",
            [Cart.getNomDuProduit(), int(Cart.getQuantite()), float(Cart.getTotal()),float(Cart.getPrice()),signature,datee])
        self.conn.commit()
    def showCart(self,table):
        self.cursor.execute("select * from Cart")
        rows=self.cursor.fetchall()
        table.row_data = rows
    def getItemsInCart(self):
        self.cursor.execute("select * from Cart")
        rows = self.cursor.fetchall()
        return rows
    def countCart(self):
        self.cursor.execute("select count(*) from Cart")
        rows=self.cursor.fetchall()
        return rows

