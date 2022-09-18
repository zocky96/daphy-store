from libs.uix.component.moule.Product import Product
from libs.uix.component.dal.dal_product import DalProduct
class ControllerProduct:
    def __init__(self):
        self.dal=DalProduct()

    def countProduct(self):
        return self.dal.countProduct()
    def showProducts(self,table):
        self.dal.showProducts(table)
    def modifyProduct(self,nom_comercial,nom_pharmaceutique,prix,quantite,nom_du_fournisseur,phone_fournisseur,type_de_produit,id):
        obj_product = Product(nom_comercial, nom_pharmaceutique, prix, quantite, nom_du_fournisseur, phone_fournisseur,type_de_produit)
        self.dal.modifyProduct(obj_product,id)
    def save_product(self,nom_comercial,nom_pharmaceutique,prix,quantite,nom_du_fournisseur,phone_fournisseur,type_de_produit,date):
        obj_product=Product(nom_comercial,nom_pharmaceutique,prix,quantite,nom_du_fournisseur,phone_fournisseur,type_de_produit)
        self.dal.saveProduct(obj_product,date)
    def deleteProduct(self,id):
        self.dal.deleteProduct(id)
    def getProductName(self):
        return self.dal.getProductName()

    def getProductType(self):
        return self.dal.getProductType()

    def getSommeCash(self):
        return self.dal.getSommeCash()

    def getStock(self):
        return self.dal.getStock()