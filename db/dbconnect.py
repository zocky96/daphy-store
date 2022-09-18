import mysql.connector
class Connexion:
    def connect(self):
        self.create_db()
        conn=None
        try:
            conn=mysql.connector.connect(host="127.0.0.1",user="root",passwd="",database="daphy_store",use_pure=True)
            self.create_tables(conn)
        except:
            pass
        return conn
    def create_db(self):
        try:
            conn=mysql.connector.connect(host="127.0.0.1",user="root",passwd='')
            cursor=conn.cursor()
            cursor.execute("create database daphy_store")
            conn.commit()
            connx=self.connect()
            self.create_tables(connx)
        except:
            pass

    def create_tables(self,conn):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "create table users(id int primary key auto_increment,nom varchar(255),prenom varchar(255),user varchar(255),poste varchar(255),passwd blob,log_date date,tentative int,blocker varchar(255),email varchar(255),confirm_code varchar(255),deja_bloquer varchar(255))")
            conn.commit()
            cursor.execute(
                "insert into users(nom,prenom,user,poste,passwd,email,blocker,deja_bloquer,tentative) values('desir','renaldo','zock','adm','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','zocky58@gmail.com','False','False',0)")
            conn.commit()
        except:
            pass
        try:
            cursor.execute("create table cart (id int primary key auto_increment,nom_du_produit varchar(255),quantite int,prix decimal(14.4),signature varchar(255),datee date,total decimal(14.4))")
            conn.commit()
        except:
            pass
        try:
            cursor.execute(
                "create table produit(id int primary key auto_increment,nom_comercial varchar(255),nom_pharmaceutique varchar(255),prix decimal(14.4),quantite int,nom_du_fournisseur varchar(255),phone_fournisseur varchar(255),type_produit varchar(255),date_save varchar(255),stock int)")
            conn.commit()
        except:
            pass
        try:
            cursor.execute(
                "create table vente(id int primary key auto_increment,nom_du_produit varchar(255),quantite int,total decimal(14.4),signature varchar(255),date_de_vente date)")
            conn.commit()
        except:
            pass


