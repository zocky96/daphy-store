import random
import psutil
import string
from ursina import *
from math import cos,sin,sqrt
from ursina.prefabs.first_person_controller import FirstPersonController
def code():
    chiffres = string.digits
    rand=random.sample(chiffres,6)
    liste=[]
    i=1
    for x in rand:
        liste.append(x)
        i+=1
        if i==4:
            liste.append('-')
    return ''.join(liste)
def Get_connected_usb_keys():
    keys = []
    list_disk = psutil.disk_partitions()
    for disk in list_disk:
        print(disk)
        if disk.opts == 'cdrom':
            pass
        else:
            if "removable" in disk.opts:
                keys.append(disk.device)
app=Ursina()

class Votex(Button):
    def __init__(self, posi=(0,0,0)):
        super().__init__()
        self.model='cube'
        self.position=posi
        self.color=color.color(0,0,random.uniform(0.9,1))
        self.parent=scene
        self.texture = 'white_cube'
        self.origin_y = 0.5
        self.highlight_color = color.lime
    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                Votex(posi=self.position + mouse.normal)
            if key == "right mouse down":
                destroy(self)
class Pers(Button):
    def __init__(self):
        super().__init__()
        self.parent = scene
        self.model = 'cube'
        self.color = color.red
        
    def input(self, key):
        if key == "up arrow":
            z = self.position.z
            z += 1
            pos = (self.position.x,self.position.y,z)
            self.position = pos
            pos_cam = (cam.position.x,cam.position.y,z)
            #cam.position = pos_cam
            cam.rotation=cos(45)
            cam.fov=83
        if key == "down arrow":
            z = self.position.z
            z -= 1
            pos = (self.position.x,self.position.y,z)
            self.position = pos
            pos_cam = (cam.position.x,cam.position.y,z)
            #cam.position = pos_cam
        if key == "left arrow":
            x = self.position.x
            x -= 1
            pos = (x,self.position.y,self.position.z)
            self.position = pos
            pos_cam = (x,cam.position.y,cam.position.z)
            #cam.position = pos_cam

        if key == "right arrow":
            x = self.position.x
            x += 1
            pos = (x,self.position.y,self.position.z)
            self.position = pos
            pos_cam = (x,cam.position.y,cam.position.z)
            cam.position = pos_cam
            cam.fov=83

def update():
    pass
for x in range(15):
    for z in range(15):
        Votex(posi=(x,0,z))
player=FirstPersonController()
h=Pers()
cam = camera
app.run()