class User:
    def __init__(self,user,passwd,nom,prenom,poste,email):
        self.__user_name = user
        self.__password = passwd
        self.__nom = nom
        self.__prenom = prenom
        self.__poste = poste
        self.__email = email

    def getUserName(self):
        return self.__user_name
    def getPassord(self):
        return self.__password
    def getNom(self):
        return self.__nom
    def getPrenom(self):
        return self.__prenom
    def getPoste(self):
        return self.__poste
    def getEmail(self):
        return self.__email