import random
from tkinter import CENTER, PhotoImage
from PIL import Image,ImageTk

class Canal:
    def __init__(self,y,h):
        self.y=y
        self.h=h
        self.troncos_en_el_canal=[]
        self.direccion=random.choice([-1,1])

    def pinta_canal(self,w):
        w.create_rectangle(0,self.y,800,self.y+self.h,fill="blue")


    class Tronco:
        def __init__(self,x,w,v,canal):
            self.x=x
            self.w=w
            self.v=canal.direccion*v
            self.y=canal.y+5
            self.h=canal.h-10
            self.estado=True

            if canal.direccion==1:
                self.imagen=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/1er cuatri/Programacion avanzada/RANITAOFICIAL/tronco.png").resize((self.w, self.h)))
            else:
                self.imagen=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/1er cuatri/Programacion avanzada/RANITAOFICIAL/tronco2.png").resize((self.w, self.h)))
                

        def moure(self):
            self.x+=self.v
            #no se si la primera condicion es necesaria
            if self.v>0 and self.x+(self.w)/2>800:
                self.x=-(self.w)/2
            if self.v<0 and self.x+(self.w)/2<0:
                self.x=800-(self.w)/2            
            
        def pinta_tronco(self,w):
            if self.estado:
                w.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h, fill="orange")
                w.create_image(self.x + (self.w / 2), self.y + (self.h / 2), anchor=CENTER, image=self.imagen)




    def llena_el_canal(self, anchuras):
        num_troncos=random.randint(2, 3)
        v=random.randint(3, 10)
        canal_lleno=set()

        for i in range(num_troncos):
            w=random.choice(anchuras)
            x=random.randint(0,750)
            nuevo_tronco=self.Tronco(x,w,v,self)
            while any(pos in canal_lleno for pos in range(x,x+w+5)):
                x=random.randint(0,750)
            
            nuevo_tronco.x=x
            canal_lleno.update(range(x,x+w+5))
            self.troncos_en_el_canal.append(nuevo_tronco)


