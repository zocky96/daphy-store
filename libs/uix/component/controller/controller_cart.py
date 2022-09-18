from libs.uix.component.dal.dalCart import DalCart
from libs.uix.component.moule.moule_cart import Cart
class ControllerCart:
    def __init__(self):
        self.dal=DalCart()

    def saveToCart(self,nom_du_produit,quantite,total,prix,signature,datee):
        obj_cart=Cart(nom_du_produit,quantite,total,prix)
        self.dal.saveToCart(obj_cart,signature,datee)

    def getSum(self):
        return self.dal.getSum()

    def getItemsInCart(self):
        return self.dal.getItemsInCart()
    def clearCart(self, table):
        self.dal.clearCart(table)
    def countCart(self):
        return self.dal.countCart()
    def showCart(self,table):
        self.dal.showCart(table)
    def cancelCart(self,id,table):
        self.dal.cancelCart(id,table)
