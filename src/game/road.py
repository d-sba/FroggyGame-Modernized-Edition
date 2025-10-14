import random
from tkinter import CENTER, PhotoImage
import os
from PIL import Image,ImageTk

class Carril:
    def __init__(self,y,h):
        self.y=y
        self.h=h
        self.cotxes_en_el_carril=[]
        self.direccion=random.choice([1,-1])

    def road_painter(self,w):
        w.create_rectangle(0,self.y,800,self.y+self.h,fill="grey")


    class Cotxe:
        def __init__(self,x,w,v,carril):
            self.x=x
            self.w=w
            self.v=carril.direccion*v
            self.y=carril.y+5
            self.h=carril.h-10
            self.estado=True

            BASE_PATH = os.path.dirname(__file__)

            if carril.direccion==-1:
                if self.w==90:                                       
                    self.imagen_camion=ImageTk.PhotoImage(Image.open(os.path.join(BASE_PATH, "assets", "camion2.png")).resize((self.w, self.h)))
                if self.w==60:
                    self.imagen_camion=ImageTk.PhotoImage(Image.open(os.path.join(BASE_PATH, "assets", "coche2.png")).resize((self.w, self.h)))
            else:
                if self.w==90:
                    self.imagen_camion=ImageTk.PhotoImage(Image.open(os.path.join(BASE_PATH, "assets", "camion.png")).resize((self.w, self.h)))
                if self.w==60:
                    self.imagen_camion=ImageTk.PhotoImage(Image.open(os.path.join(BASE_PATH, "assets", "coche.png")).resize((self.w, self.h)))

        def mover(self):
            self.x+=self.v
            if self.x>800:
                self.x=-self.w
            if self.x+self.w<0:
                self.x=800-self.w

        def pinta_coche(self,w):
            if self.estado:
                w.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h, fill="red")
                w.create_image(self.x + (self.w / 2), self.y + (self.h / 2), anchor=CENTER, image=self.imagen_camion)


    def llena_el_carril(self, anchuras):
        num_coches = random.randint(3, 5)
        v = random.randint(1, 10)

        forbidden_positions = []  
        max_intentos = 100 

        for _ in range(num_coches):
            intentos = 0
            colocado = False

            while not colocado and intentos < max_intentos:
                w = random.choice(anchuras)
                x = random.randint(w, 800 - w)  
                nuevo_intervalo = (x - 20, x + w + 20) 

                if not any(not (nuevo_intervalo[1] < i or nuevo_intervalo[0] > f) for i, f in forbidden_positions):
                    # No hay colisión → colocamos el coche
                    forbidden_positions.append(nuevo_intervalo)
                    nuevo_coche = self.Cotxe(x, w, v, self)
                    self.cotxes_en_el_carril.append(nuevo_coche)
                    colocado = True

                intentos += 1

        

class PowerUp:
    def __init__(self,x,y,v):
        self.x=x
        self.y=y
        self.v=v
        self.w=30
        self.h=30
        self.estado=False
        self.cont=1
        self.imagen=PhotoImage(file="C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/1er cuatri/Programacion avanzada/RANITAOFICIAL/vida.png").subsample(10,10)

    def moure(self):
        self.x+=self.v
        if self.x>=800:
            self.x=0
    
    def pinta_vida(self,w):
        if not self.estado and self.cont==1:
            w.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h, outline="")
            w.create_image(self.x+self.w/2,self.y+self.h/2,anchor=CENTER, image=self.imagen)