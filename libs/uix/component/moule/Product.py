class Product:
    def __init__(self,nom_comercial,nom_pharmaceutique,prix,quantite,nom_du_fournisseur,phone_fournisseur,type_de_produit):
        self.__nom_comercial=nom_comercial
        self.__nom_pharmaceutique=nom_pharmaceutique
        self.__prix=prix
        self.__quantite=quantite
        self.__nom_du_fournisseur=nom_du_fournisseur
        self.__phone_fournisseur=phone_fournisseur
        self.__type_de_produit=type_de_produit
    def getNomComercial(self):
        return self.__nom_comercial
    def getNomPharmaceutique(self):
        return self.__nom_pharmaceutique
    def getPrix(self):
        return self.__prix
    def getQuantite(self):
        return self.__quantite
    def getNomDuFournisseur(self):
        return self.__nom_du_fournisseur
    def getPhoneFournisseur(self):
        return self.__phone_fournisseur
    def getTypeOfProduct(self):
        return self.__type_de_produit
