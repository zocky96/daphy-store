from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivy.properties import StringProperty
from akivymd.uix.badgelayout import AKBadgeLayout
from kivymd_extensions.akivymd.uix.charts import AKBarChart
from kivy.lang import Builder
from hashlib import sha256
from kivy.factory import Factory
from kivy.metrics import dp
import os
import gc
from prettytable import from_db_cursor
from datetime import datetime
#-----------------------------------
from db.dbconnect import Connexion
from libs.uix.component.controller.controller_user import Controller_user
from libs.uix.component.controller.controllerVente import ControllerVente
from libs.uix.component.controller.controller_product import ControllerProduct
from libs.uix.component.controller.controller_cart import ControllerCart

#Window.borderless=True
#Window.minimize()
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
os.environ['my_manage_app']=os.getcwd()
kv_dir=os.environ['my_manage_app']+"/libs/uix/kv"
kv="""
<IconListItem>
     IconLeftWidget:
          icon: root.icon
#:import Login libs.uix.baseclass.login
#:import Home libs.uix.baseclass.home
#:import Cart libs.uix.baseclass.cart
#:import Recovery libs.uix.baseclass.recovery

ScreenManager:
     Login:
     Home:
     Cart:
     Recovery:
     

"""
class IconListItem(OneLineIconListItem):
    icon = StringProperty()
for file in os.listdir(kv_dir):
    with open(os.path.join(kv_dir,file)) as kv_text:
        Builder.load_string(kv_text.read())
class Manage(MDApp):
    def __int__(self,**kwargs):
        super().__init__(**kwargs)
        self.icon_resto_path=None
        self.resto = None
        self.user=None
        self.produit=None
        self.id_for_selected_row=None
        self.notification = 0
    def sendMail(self):
        email=self.screen.get_screen('recovery').ids.email.text
        self.screen.get_screen('recovery').ids.verification.add_widget(MDLabel(text="Entrer le code de verification",halign="center",font_style='H5'))
        code=MDTextField(mode="rectangle",size_hint_x=.8,pos_hint={"center_x":.5})
        self.screen.get_screen('recovery').ids.verification.add_widget(code)
        self.screen.get_screen('recovery').ids.verification.add_widget(MDRaisedButton(text="valider",pos_hint={"center_x":.5}))
        #self.screen.get_screen('recovery').ids.verification.add_widget(Widget)


    def imprimmer(self):
        date = self.Rapport.ids.date.text
        db_table = self.Rapport.ids.table.text
        print(db_table)
        if db_table == "tous":
            # produit
            self.cursor.execute('select * from produit where date_save=%s', [date])
            mytable = from_db_cursor(self.cursor)
            path_file = "Tout " + str(date) + '.txt'
            #path_file = path_file.replace('/', '_')
            path_file = "rapport/" + path_file
            with open(path_file, 'a') as rapport_file:
                rapport_file.write("                                   Daphy Store\n")
                rapport_file.write("                        'Produit cosmetique et pharmaceutique'\n")
                rapport_file.write("\n")
                rapport_file.write("                                      Produit\n")
                rapport_file.write("\n")
                rapport_file.write(str(mytable) + "\n")
                # retrait
                self.cursor.execute('select * from vente where date_de_vente=%s', [date])
                mytable = from_db_cursor(self.cursor)
                rapport_file.write("                                      Vente\n")
                rapport_file.write("\n")
                rapport_file.write(str(mytable) + "\n")
            os.startfile(os.path.abspath(path_file), 'print')
            Snackbar(text='Impression terminer').open()

        elif db_table == 'produit':
            self.cursor.execute('select * from produit where date_save=%s', [date])
            mytable = from_db_cursor(self.cursor)
            path_file = "produit " + str(date) + '.txt'
            #path_file = path_file.replace('/', '_')
            path_file = "rapport/" + path_file
            with open(path_file, 'a') as rapport_file:
                rapport_file.write("                                   Daphy Store\n")
                rapport_file.write("                        Produit cosmetique et pharmaceutique\n")
                rapport_file.write("\n")
                rapport_file.write("                                     Produit\n")
                rapport_file.write("\n")
                rapport_file.write(str(mytable) + "\n")
            os.startfile(os.path.abspath(path_file), 'print')
            Snackbar(text='Impression terminer').open()
        elif db_table == 'vente':
            self.cursor.execute('select * from vente where date_de_vente=%s', [date])
            mytable = from_db_cursor(self.cursor)
            path_file = "vente " + str(date) + '.txt'
            #path_file = path_file.replace('/', '_')
            path_file = "rapport/" + path_file
            with open(path_file, 'a') as rapport_file:
                rapport_file.write("                                   Daphy Store\n")
                rapport_file.write("                        Produit cosmetique et pharmaceutique\n")
                rapport_file.write("\n")
                rapport_file.write("                                      Vente\n")
                rapport_file.write("\n")
                rapport_file.write(str(mytable) + "\n")
            os.startfile(os.path.abspath(path_file), 'print')
            Snackbar(text='Impression terminer').open()
        else:
            Snackbar(text="Erreur lors de l'inpression").open()
    def on_cancel(self,ins,value):
        pass
    def on_save(self,ins,value,date):
        self.date_rapport = value
        self.Rapport.ids.date.text = str(self.date_rapport)
    def show_date(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save,on_cancel=self.on_cancel)
        date_dialog.open()
    def theRapport(self,text):
        self.theTables.dismiss()
        self.Rapport.ids.table.text = text
    def rapport(self):
        self.screen.get_screen('home').ids.container.clear_widgets()
        self.screen.get_screen('home').ids.container.add_widget(self.Rapport)
        tables = [{"text": 'tous', "viewclass": "OneLineListItem",
                         "on_release": lambda x='tous': self.theRapport(x)},{"text": 'produit', "viewclass": "OneLineListItem",
                         "on_release": lambda x='produit': self.theRapport(x)}, {"text": 'vente', "viewclass": "OneLineListItem",
                         "on_release": lambda x='vente': self.theRapport(x)}]
        self.theTables = MDDropdownMenu(width_mult=4, items=tables, caller=self.Rapport.ids.table)
    def backToLogin(self):
        self.root.current = 'login'
    def recovery(self):
        self.root.current = 'recovery'
    def deleteProduct(self):
        self.controlleur_produit.deleteProduct(self.id_for_selected_row)

        self.controlleur_produit.showProducts(self.table_produit)
        Snackbar(text='Produit suprimmer avec succes',bg_color=[62/255,193/255,163/255,1]).open()
    def modidyProduct(self):
        nom_du_produit = self.produit.ids.com_name.text
        nom_pharmaceutique = self.produit.ids.pharm_name.text
        prix = self.produit.ids.prix.text
        quantite = self.produit.ids.quantite.text
        nom_du_fournisseur = self.produit.ids.fournisseur_name.text
        phone_fournisseur = self.produit.ids.fournisseur_num.text
        type_de_produit = self.produit.ids.type.text
        if nom_du_produit == '' or nom_pharmaceutique == '' or prix == '' or quantite == '' or nom_du_fournisseur == "" or phone_fournisseur == '':
            Snackbar(text="L'un des champs sont vide").open()
        else:
            self.controlleur_produit.modifyProduct(nom_du_produit, nom_pharmaceutique, prix, quantite, nom_du_fournisseur,
                                          phone_fournisseur, type_de_produit, self.id_for_selected_row)
            self.controlleur_produit.showProducts(self.table_produit)
            self.clearProductFields()
            Snackbar(text= 'Produit modifier avec succes').open()
    def clearProductFields(self):
        self.produit.ids.com_name.text = ''
        self.produit.ids.pharm_name.text = ''
        self.produit.ids.prix.text = ''
        self.produit.ids.quantite.text =''
        self.produit.ids.fournisseur_name.text = ''
        self.produit.ids.fournisseur_num.text = ''
        self.produit.ids.type.text = ''
    def save_product(self):
        nom_du_produit = self.produit.ids.com_name.text
        nom_pharmaceutique = self.produit.ids.pharm_name.text
        prix = self.produit.ids.prix.text
        quantite = self.produit.ids.quantite.text
        nom_du_fournisseur = self.produit.ids.fournisseur_name.text
        phone_fournisseur = self.produit.ids.fournisseur_num.text
        type_de_produit = self.produit.ids.type.text
        if nom_du_produit == '' or nom_pharmaceutique == '' or prix == '' or quantite == '' or nom_du_fournisseur == "" or phone_fournisseur == '':
            Snackbar(text="kk").open()
        else:
            self.controlleur_produit.save_product(nom_du_produit, nom_pharmaceutique, prix, quantite, nom_du_fournisseur,
                                         phone_fournisseur, type_de_produit, datetime.now().date())
            self.controlleur_produit.showProducts(self.table_produit)
            self.clearProductFields()
            Snackbar(text="Produit enregistrer avec succes").open()


    def logout(self,*args):
        self.root.current='login'
        self.screen.get_screen('home').ids.container.clear_widgets()

    #------------------------------category----------------------------------------------------
    def checked_for_table_category(self, instance_table, current_row):
        self.id_for_selected_row = current_row[0]
        self.categorieX.ids.categorie.text = current_row[1]
        self.categorieX.ids.image.text = current_row[2]

    def Stat(self):
        indice_graph = []
        indice = 0
        graph_value = []
        self.stats.ids.layout.clear_widgets()
        rows = self.controlleur_produit.getStock()
        for value in rows:
            value_stock = value[0]
            quantite = value[1]
            percent = (quantite * 100) // value_stock
            percent = 100 - percent
            graph_value.append(percent)
            indice += 1
            indice_graph.append(indice)
        self.listProduit = []
        produit = self.controlleur_produit.getProductName()
        for produit in produit:
            self.listProduit.append(produit[0])
        self.chartX = AKBarChart(size_hint_y=None, height=dp(280), labels=True, label_size=15, anim=True)
        self.chartX.x_values = indice_graph
        self.chartX.y_values = graph_value
        self.chartX.x_labels = self.listProduit
        self.stats.ids.layout.add_widget(self.chartX)
        #--------------------------------------------------------

        self.screen.get_screen('home').ids.container.clear_widgets()
        self.screen.get_screen('home').ids.container.add_widget(self.stats)


    #------------------------------------------------------------------------------------------------------
    def set_item(self, text_item):
        self.food.ids.categorie.text=self.list_category[int(text_item)]
        self.menu.dismiss()

    def set_item_resto(self, text_item):
        self.food.ids.code_resto.text=self.list_resto_for_field[int(text_item)]
        self.menu_resto.dismiss()



    def checked_for_table_food(self, instance_table, current_row):
        self.id_for_selected_row = current_row[0]
        self.food.ids.code_resto.text = current_row[1]
        self.food.ids.nom_du_plat.text = current_row[2]
        self.food.ids.prix.text = current_row[3]
        self.food.ids.quantite.text = current_row[4]
        self.food.ids.categorie.text = current_row[5]
        self.food.ids.image.text = current_row[6]

    def checked_for_table_product(self, instance_table, current_row):
        self.id_for_selected_row = current_row[0]
        self.produit.ids.com_name.text = current_row[1]
        self.produit.ids.pharm_name.text = current_row[2]
        self.produit.ids.prix.text = current_row[3]
        self.produit.ids.quantite.text = current_row[4]
        self.produit.ids.fournisseur_name.text = current_row[5]
        self.produit.ids.fournisseur_num.text = current_row[6]
        self.produit.ids.type.text = current_row[7]

    def Produit(self):
        if self.poste=='Cassier':
            self.produit.ids.save.disabled = True
            self.produit.ids.delete.disabled = True
            self.produit.ids.modify.disabled = True
        elif self.poste == 'PDG':
            self.produit.ids.save.disabled = False
            self.produit.ids.delete.disabled = False
            self.produit.ids.modify.disabled = False
        self.screen.get_screen('home').ids.container.clear_widgets()
        self.screen.get_screen('home').ids.container.add_widget(self.produit)
        self.table_produit = MDDataTable(column_data=[("ID", dp(20)),
                                         ('nom commercial', dp(32)),
                                         ('nom pharmaceutique', dp(34)),
                                         ('prix', dp(20)),
                                         ('quantite', dp(20)),
                                         ('nom du fournisseur', dp(32)),
                                         ('phone du fournisseur', dp(34)),
                                         ('type de produit', dp(32)),
                                         ('date', dp(20)),
                                         ('Stock', dp(20))
                                         ],
                            row_data=[],
                            size_hint=(1, .45),
                            elevation=5,
                            pos_hint={'center_y': .2},
                            check=True,
                            use_pagination=True)
        self.produit.ids.table.add_widget(self.table_produit)
        self.controlleur_produit.showProducts(self.table_produit)
        self.table_produit.bind(on_check_press=self.checked_for_table_product)





    #------------------------------------------------------------------------------

    #----------------------------------produits---------------------------------------

        



    def checked_for_table_resto(self, instance_table, current_row):
        self.id_for_selected_row = current_row[0]
        self.resto.ids.nom.text = current_row[1]
        self.resto.ids.adresse.text = current_row[2]
        self.resto.ids.telephone.text = current_row[3]
        self.resto.ids.logo.text = current_row[4]
        self.resto.ids.close_hour.text = current_row[5]
        self.resto.ids.open_hour.text = current_row[6]
        self.resto.ids.slogan.text = current_row[7]
    def clear_resto_field(self):
        self.resto.ids.nom.text = ""
        self.resto.ids.adresse.text = ""
        self.resto.ids.telephone.text = ""
        self.resto.ids.logo.text = ""
        self.resto.ids.close_hour.text = ""
        self.resto.ids.open_hour.text = ""
        self.resto.ids.slogan.text = ""
    def dashboard(self):
        self.screen.get_screen('home').ids.container.clear_widgets()
        self.screen.get_screen('home').ids.container.add_widget(self.theDashboard)

       

    #---------------------------------------------------------------------------
    #-------------------------------user----------------------------------------
    def save_user(self):
        nom = self.user.ids.nom.text
        prenom = self.user.ids.prenom.text
        user_name = self.user.ids.user_name.text
        email = self.user.ids.email.text
        password = sha256(bytes(self.user.ids.password.text, "ascii")).hexdigest()
        conf_password = sha256(bytes(self.user.ids.conf_password.text, "ascii")).hexdigest()
        poste = self.user.ids.poste.text
        if password == conf_password:
            self.controlleur_user.saveUser(nom, prenom, user_name, password, poste, email)
            Snackbar(text="Utilisateur enregistrer avec succes").open()
            self.controlleur_user.showUsers(self.table_user)
            self.clear_user_fields()
        else:
            Snackbar(text="Mettre le meme mot de passe dans les deux champs").open()
    def delete_user(self):
        try:
            self.controlleur_user.deleteUser(self.id_for_selected_row)
            Snackbar(text="Suprimmer avec succes").open()
            self.controlleur_user.showUsers(self.table_user)
            self.clear_user_fields()
        except Exception as e:

            if "object has no attribute" in str(e):
                Snackbar(text="Selectionne un utilisateur").open()
                # toast(text="Selectionne un restaurent dans la table")
                pass

    def modify_user(self):
        nom = self.user.ids.nom.text
        prenom = self.user.ids.prenom.text
        user_name = self.user.ids.user_name.text
        email = self.user.ids.email.text
        password = sha256(bytes(self.user.ids.password.text, "ascii")).hexdigest()
        conf_password = sha256(bytes(self.user.ids.conf_password.text, "ascii")).hexdigest()
        poste = self.user.ids.poste.text
        if password == conf_password:
            self.controlleur_user.modifyUser(nom, prenom, user_name, password, poste, email, self.id_for_selected_row)
            Snackbar(text="Utilisateur modifier avec succes").open()
            self.controlleur_user.showUsers(self.table_user)
            self.clear_user_fields()
        else:
            Snackbar(text="Mettre le meme mot de passe dans les deux champs").open()
    def users(self):
        if self.poste=='Cassier':
            self.user.ids.save.disabled = True
            self.user.ids.delete.disabled = True
        elif self.poste =='PDG':
            self.user.ids.save.disabled = False
            self.user.ids.delete.disabled = False
        self.screen.get_screen('home').ids.container.clear_widgets()
        self.screen.get_screen('home').ids.container.add_widget(self.user)
        self.table_user = MDDataTable(column_data=[("ID", dp(30)),
                                         ("Nom", dp(30)),
                                         ("Prenom", dp(30)),
                                         ("Nom d'utilisateur", dp(30)),
                                         ("Poste", dp(30)),
                                         ("Email", dp(35)),
                                         ],
                            row_data=self.list_resto,
                            size_hint=(1, .45),
                            elevation=5,
                            check=True,
                            pos_hint={"center_x":.5},
                            use_pagination=True)
        self.table_user.bind(on_check_press=self.checked_for_table_user)
        self.user.ids.table.add_widget(self.table_user)
        self.controlleur_user.showUsers(self.table_user)
        listePoste = [
            {"text": 'Caissier', "viewclass": "OneLineListItem", "on_release": lambda x='Cassier': self.selectPoste(x)},
            {"text": "Gestionnaire de stock", "viewclass": "OneLineListItem", "on_release": lambda x='Gestionnaire de stock': self.selectPoste(x)},
            {"text": 'PDG', "viewclass": "OneLineListItem", "on_release": lambda x='PDG': self.selectPoste(x)},]
        self.posteMenu = MDDropdownMenu(width_mult=4, items=listePoste, caller=self.user.ids.poste)
    def selectPoste(self,text):
        self.posteMenu.dismiss()
        self.user.ids.poste.text = text

    def checked_for_table_user(self, instance_table, current_row):
        self.id_for_selected_row = current_row[0]
        self.user.ids.nom.text = current_row[1]
        self.user.ids.prenom.text = current_row[2]
        self.user.ids.user_name.text = current_row[3]
        self.user.ids.email.text = current_row[5]
        self.user.ids.poste.text = current_row[4]



    def clear_user_fields(self):
        self.id_for_selected_row = ''
        self.user.ids.nom.text = ''
        self.user.ids.prenom.text = ''
        self.user.ids.user_name.text = ''
        self.user.ids.email.text = ''
        self.user.ids.poste.text = ''
        self.user.ids.password.text = ''
        self.user.ids.conf_password.text = ''
    #-----------------------------------------------------------------------------
    def home(self):
        self.root.current='home'
    #------------------------------------order-----------------------------------------------
    def checked_for_table_vente(self, instance_table, current_row):
        self.id_for_selected_row = current_row[0]
        self.product_name = current_row[1]
    def clearCart(self):
        self.controlleur_cart.clearCart(self.table_cart)
        self.screen.get_screen('cart').ids.total_cash.text = "0 Gdes"
        self.screen.get_screen('home').ids.notification.text = str(0)
    def removeToCart(self):
        self.controlleur_cart.cancelCart(self.id_for_selected_row,self.table_cart)
        self.controlleur_cart.showCart(self.table_cart)
        self.screen.get_screen('cart').ids.total_cash.text = f"{self.controlleur_cart.getSum()} Gdes"
    def checked_for_table_cart(self, instance_table, current_row):
        self.id_for_selected_row = current_row[0]
    def pannier(self):
        self.root.current = 'cart'
        self.table_cart = MDDataTable(column_data=[("ID", dp(30)),
                                                    ('Nom du produit', dp(30)),
                                                    ('Quantite', dp(30)),
                                                    ('Prix', dp(30)),
                                                    ('Signature', dp(30)),
                                                    ('Date', dp(30)),
                                                    ('total', dp(30)),
                                                    ],
                                       row_data=[],
                                       size_hint=(.9, .59),
                                       elevation=5,
                                       pos_hint={'center_y': .53,'center_x':.5},
                                       check=True,
                                       use_pagination=True)

        self.controlleur_cart.showCart(self.table_cart)
        self.screen.get_screen('cart').ids.total_cash.text = f"{self.controlleur_cart.getSum()} Gdes"
        self.table_cart.bind(on_check_press=self.checked_for_table_cart)


        self.screen.get_screen('cart').ids.table.add_widget(self.table_cart)
    def show_cart_items(self):
        somme = 0

    def buyToCart(self):
        rows=self.controlleur_cart.getItemsInCart()
        for row in rows:
            product_name=row[1]
            quantite = row[2]
            prix = row[3]
            signature = row[4]
            date = row[5]
            total = row[6]
            self.controlleur_vente.vente(product_name,prix,quantite,total,signature,date)
            self.clearCart()
            Snackbar(text="Les produits ont ete vendu avec succes").open()
    def clearFieldVente(self):
        self.venteX.ids.nom_du_produit.text = ''
        self.venteX.ids.quantite.text = ''
    def addToCart(self):
        if self.venteX.ids.nom_du_produit.text == '' or self.venteX.ids.quantite.text == '':
            Snackbar(text="Selectionner un produit ou ajouter la quantite").open()
        else:
            #--------------------------------------------

            #-----------------------------------------
            info = self.controlleur_produit.getProductName()
            # --------------------test------------------------
            # -------------a efface --------------------------
            #self.signature = self.controlleur_user.getFullName('zock','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4')
            # -------------a efface-------------------------------------
            # -----------------------------------------------------------
            list_name = []
            list_price = []
            list_quantite = []
            for data in info:
                list_name.append(data[0])
                list_price.append(data[1])
                list_quantite.append(data[2])

            productName = self.venteX.ids.nom_du_produit.text
            index = list_name.index(productName)
            prix = list_price[index]
            client_quantite = self.venteX.ids.quantite.text

            quantite_disponible = list_quantite[index]
            if int(client_quantite) > int(quantite_disponible):
                Snackbar(text="cette quantite de produit n'est pas disponible").open()
            else:
                total = int(client_quantite) * prix
                date = datetime.now().date()


                self.clearFieldVente()
                self.id_cart += 1
                self.controlleur_cart.saveToCart(productName,client_quantite,total,prix,self.signature,date)
                toast(text=f"{productName} a ete ajouter au pannier")
                self.notification = self.controlleur_cart.countCart()[0][0]
                self.screen.get_screen('home').ids.notification.text = str(self.notification)
    def vendreProduct(self):
        info=self.controlleur_produit.getProductName()
        #--------------------test------------------------
        #-------------a efface --------------------------
        #self.signature = self.controlleur_user.getFullName('zock','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4')
        #-------------a efface-------------------------------------
        #-----------------------------------------------------------
      
        list_name = []
        list_price = []
        list_quantite = []
        for data in info:
            list_name.append(data[0])
            list_price.append(data[1])
            list_quantite.append(data[2])


        productName = self.venteX.ids.nom_du_produit.text
        index = list_name.index(productName)
        prix = list_price[index]
        client_quantite = self.venteX.ids.quantite.text

        quantite_disponible = list_quantite[index]
        if int(client_quantite) > int(quantite_disponible):
            Snackbar(text="cette quantite de produit n'est pas disponible").open()
        else:
            total = int(client_quantite) * prix
            date = datetime.now().date()
            self.controlleur_vente.vente(productName, prix, client_quantite, total, self.signature, date)
            self.controlleur_vente.showVente(self.table_vente)
            self.clearFieldVente()
            Snackbar(text='Produit vendu avec succes').open()
    def theProductsX(self,text):
        self.theProductsNames.dismiss()
        self.venteX.ids.nom_du_produit.text = text

    def cancelVente(self):
        self.controlleur_vente.cancelVente(self.id_for_selected_row, self.product_name)
        self.controlleur_vente.showVente(self.table_vente)
        Snackbar(text='vente annule').open()
    def Vente(self):
        self.screen.get_screen('home').ids.container.clear_widgets()
        #order = Factory.Vente()
        self.screen.get_screen('home').ids.container.add_widget(self.venteX)
        products=self.controlleur_produit.getProductName()
        product_nameX=[]
        for product in products:
            product_name=product[0]
            product_nameX.append(product_name)
   
        typeProduitX = [{"text": f'{name}', "viewclass": "OneLineListItem",
                            "on_release": lambda x=f'{name}': self.theProductsX(x)} for name in product_nameX]
        self.theProductsNames = MDDropdownMenu(width_mult=4, items=typeProduitX, caller=self.venteX.ids.nom_du_produit)
        self.table_vente = MDDataTable(column_data=[("ID", dp(30)),
                                              ('Nom du produit', dp(30)),
                                              ('Quantite', dp(30)),
                                              ('total', dp(30)),
                                              ('signature_autorise', dp(35)),
                                              ('date', dp(30)),

                                              ],
                                 row_data=[],
                                 size_hint=(1, .69),
                                 elevation=5,
                                 pos_hint={'center_y':.39},
                                 check=True,
                                 use_pagination=True)
        self.venteX.ids.table.add_widget(self.table_vente)
        self.controlleur_vente.showVente(self.table_vente)
        self.table_vente.bind(on_check_press=self.checked_for_table_vente)
    #------------------------------------------------------------------------------------------


    def rail_open(self):
        if self.screen.get_screen('home').ids.rail.rail_state == "open":

            self.screen.get_screen('home').ids.rail.rail_state = "close"
        else:
            self.screen.get_screen('home').ids.rail.rail_state = "open"
    def connect(self):
        user=self.screen.get_screen('login').ids.user.text
        passwd=sha256(bytes(self.screen.get_screen('login').ids.passwd.text,"ascii")).hexdigest()
        controlleur=Controller_user()
        rows=controlleur.login(user,passwd)

        if len(rows) > 0:
            self.root.current='home'
            self.screen.get_screen('login').ids.user.text = ''
            self.screen.get_screen('login').ids.passwd.text = ''
            self.signature,self.poste = self.controlleur_user.getFullName(user,passwd)
            self.dashboard()
        else:
            Snackbar(text="Erreur entre le bon mot de passe").open()
        

    def on_start(self):

        #self.chartX.x_labels = ['C++', 'Java', 'Python']
        #self.stats.ids.layout.add_widget(self.chartX)
        pass
    def theTypes(self,text):
        self.typeProduit.dismiss()
        self.produit.ids.type.text = text
    def build(self):
        self.title='Daphy Store'
        gc.collect()
        try:
            self.conn = Connexion()
            self.conn = self.conn.connect()
            self.cursor = self.conn.cursor()
        except Exception as e:
            Snackbar(text="koko").open()
        self.screen=Builder.load_string(kv)
        self.produit = Factory.Produit()
        self.theDashboard = Factory.Dashboard()
        self.Rapport = Factory.Rapport()
        self.user=Factory.Users()
        self.list_resto=[]
        self.produit_name = []
        self.list_cart = []
        self.notification = 0
        self.id_cart = 0
        self.venteX = Factory.Vente()
        self.controlleur_user=Controller_user()
        self.controlleur_produit=ControllerProduct()
        self.controlleur_vente = ControllerVente()
        self.controlleur_cart = ControllerCart()
        self.stats=Factory.Statistique()
        typeProduit=[{"text":'Comprime',"viewclass": "OneLineListItem","on_release": lambda x='Comprime': self.theTypes(x)},{"text":"Creme","viewclass": "OneLineListItem","on_release": lambda x='Creme': self.theTypes(x)},{"text":'Sirop',"viewclass":"OneLineListItem","on_release": lambda x='Sirop': self.theTypes(x)},{"text":'Piqure',"viewclass": "OneLineListItem","on_release": lambda x='Piqure': self.theTypes(x)},{"text":'Autres',"viewclass": "OneLineListItem","on_release": lambda x='Autres': self.theTypes(x)}]
        self.typeProduit=MDDropdownMenu(width_mult=4,items=typeProduit,caller=self.produit.ids.type)

        nbr_produit = self.controlleur_produit.countProduct()[0][0]
        self.theDashboard.ids.nbr_de_produit.text = str(nbr_produit)
        self.theDashboard.ids.type.text = str(self.controlleur_produit.getProductType())
        self.theDashboard.ids.somme.text = f"{self.controlleur_produit.getSommeCash()} Gdes"


        self.dashboard()




        return self.screen
Manage().run()
