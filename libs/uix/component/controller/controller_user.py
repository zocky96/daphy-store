from libs.uix.component.dal.dal_user import DalUser
from libs.uix.component.moule.moule_user import User
class Controller_user:
    def __init__(self):
        self.dal = DalUser()
    def getFullName(self,user,passwd):
        return self.dal.getFullName(user,passwd)
    def modifyUser(self,nom,prenom,user,password,poste,email,id):
        obj_user = User(user,password,nom,prenom,poste,email)
        self.dal.modifyUser(obj_user,id)
    def showUsers(self,table):
        self.dal.showUsers(table)
    def deleteUser(self,id):
        self.dal.deleteUser(id)
    def saveUser(self,nom,prenom,user,password,poste,email):
        obj_user = User(user,password,nom,prenom,poste,email)
        self.dal.saveUser(obj_user)
    def login(self,user,passwd):
        login_obj=User(user, passwd,"","","","")
        return  self.dal.login(login_obj)


