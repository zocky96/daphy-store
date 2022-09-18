from libs.uix.component.dal.dalVente import DalVente
from libs.uix.component.moule.vente import Vente
class ControllerVente:
    def __init__(self):
        self.dal=DalVente()

    def showVente(self,table):
        self.dal.showVente(table)
    def cancelVente(self,id,nom_du_produit):
        self.dal.cancelVente(id,nom_du_produit)
    def vente(self,nom_du_produit,prix,quantite,total,signature,date):
        obj_vente=Vente(nom_du_produit,prix,quantite,total,signature)
        self.dal.vente(obj_vente,date)