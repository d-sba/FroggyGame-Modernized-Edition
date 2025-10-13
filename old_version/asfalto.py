import random
from tkinter import CENTER, PhotoImage
from PIL import Image,ImageTk

class Carril:
    def __init__(self,y,h):
        self.y=y
        self.h=h
        self.cotxes_en_el_carril=[]
        self.direccion=random.choice([1,-1])

    def pinta_carril(self,w):
        w.create_rectangle(0,self.y,800,self.y+self.h,fill="grey")


    class Cotxe:
        def __init__(self,x,w,v,carril):
            self.x=x
            self.w=w
            self.v=carril.direccion*v
            self.y=carril.y+5
            self.h=carril.h-10
            self.estado=True


            if carril.direccion==-1:
                if self.w==90:                                       
                    self.imagen_camion=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/1er cuatri/Programacion avanzada/RANITAOFICIAL/camion2.png").resize((self.w, self.h)))
                if self.w==60:
                    self.imagen_camion=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/1er cuatri/Programacion avanzada/RANITAOFICIAL/coche2.png").resize((self.w, self.h)))
            else:
                if self.w==90:
                    self.imagen_camion=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/1er cuatri/Programacion avanzada/RANITAOFICIAL/camion.png").resize((self.w, self.h)))
                if self.w==60:
                    self.imagen_camion=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/1er cuatri/Programacion avanzada/RANITAOFICIAL/coche.png").resize((self.w, self.h)))

        def moure(self):
            self.x+=self.v
            if self.x>800:
                self.x=-self.w
            if self.x+self.w<0:
                self.x=800-self.w

        def pinta_cotxe(self,w):
            if self.estado:
                w.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h, fill="red")
                w.create_image(self.x + (self.w / 2), self.y + (self.h / 2), anchor=CENTER, image=self.imagen_camion)


    def llena_el_carril(self,anchuras):
        num_coches=random.randint(3,5)
        for i in range(num_coches):
            x=random.randint(0,750)
            w=random.choice(anchuras)
            v=random.randint(1,10)
            nuevo_cotxe=self.Cotxe(x,w,v,self)
            self.cotxes_en_el_carril.append(nuevo_cotxe)

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