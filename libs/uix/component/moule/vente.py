class Vente:
    def __init__(self,nom_du_produit,prix,quantite,total,signature):
        self.__nom_du_produit = nom_du_produit
        self.__quantite = quantite
        self.__total = total
        self.__prix=prix
        self.__signature=signature
    def getSignature(self):
        return self.__signature
    def getPrix(self):
        return self.__prix
    def getQuantite(self):
        return self.__quantite
    def getTotal(self):
        return self.__total
    def getProductName(self):
        return self.__nom_du_produit