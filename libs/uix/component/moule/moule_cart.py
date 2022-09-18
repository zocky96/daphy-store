class Cart:
    def __init__(self,nom_du_produit,quantite,total,prix):
        self.__nom_du_produit = nom_du_produit
        self.__quantite = quantite
        self.__prix = prix
        self.__total = total
    def getPrice(self):
        return self.__prix
    def getNomDuProduit(self):
        return self.__nom_du_produit
    def getQuantite(self):
        return self.__quantite
    def getTotal(self):
        return self.__total