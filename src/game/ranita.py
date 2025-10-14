from tkinter import CENTER, PhotoImage
import keyboard
import os

class Rana:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.w=40
        self.h=40
        self.v=50
        self.viajera=False
        self.moverse_a_saltos={'up arrow':False,'down arrow':False,'right arrow':False,'left arrow':False}

        
        BASE_PATH = os.path.dirname(__file__)
        img_path = os.path.join(BASE_PATH, "assets", "ranita.png")
        self.imagen=PhotoImage(file=img_path).subsample(16,16)

    def limites(self):
        if self.x-self.v<0:
            return 1
        elif self.y+self.h+self.v>700:
            if self.x+self.w+self.v>800:
                return 3
            else:
                return 2
        else:
            return 0


    def movimientos(self,direccion):
        if self.moverse_a_saltos[direccion] and not self.viajera:
            if direccion=='up arrow':
                self.y-=self.v        
            elif direccion=='down arrow' and self.limites()!=2:
                self.y+=self.v
            elif direccion=='right arrow'and self.limites()!=3:
                self.x+=self.v
            elif direccion=='left arrow' and self.limites()!=1:
                self.x-=self.v


    def tecla(self):
        for i in self.moverse_a_saltos:
            if keyboard.is_pressed(i):
                if not self.moverse_a_saltos[i]:
                    self.moverse_a_saltos[i]=True
                    self.movimientos(i)
            if not keyboard.is_pressed(i):
                self.moverse_a_saltos[i]=False


    def detecta_choque(self,cotxe,powerup,modo):
        if self.viajera==False and cotxe.estado==True and (cotxe.x<self.x<cotxe.x+cotxe.w or cotxe.x+cotxe.w>self.x+self.w>cotxe.x) and (self.y<=cotxe.y+cotxe.h<=self.y+self.h or self.y<=cotxe.y<=self.y+self.h):
            if powerup.estado==True:
                cotxe.estado=False
                powerup.estado=False
                powerup.cont+=1
            else:
                modo=2
        return modo
            


    def pasajera(self,canales,powerup,modo):
        for canal in canales:
            for tronco in canal.troncos_en_el_canal:
                if tronco.y-5<=self.y+self.h<=tronco.y+tronco.h:
                    if tronco.x<=self.x+self.w/2<=tronco.x+tronco.w:
                        self.x+=tronco.v
                        if self.x+self.w/2<0 or self.x+self.w/2>800:
                            return 4
                        return modo
            if canal.y<self.y<canal.y+canal.h and self.viajera==False:
                if powerup.estado:
                    powerup.estado=False
                    powerup.cont=2
                    self.x=380
                    self.y=305
                else:
                    modo=4
        return modo

    def pasajera_avion (self,avion):
        if (avion.x<self.x<avion.x+avion.w or avion.x<self.x+self.w<avion.x+avion.w) and avion.y+avion.h>self.y>avion.y:
            self.viajera=True
            self.x=avion.x+10
            self.y=avion.y+50
            self.v=avion.v
        
        if self.y>654 and self.viajera:
            self.y=655
            self.x=avion.x+avion.w+10
            self.v=50
            self.viajera=False

    def ganadora(self,modo):
        if self.y+self.h/2<50:
            return 3
        return modo

    def coger_powerup(self,powerup):
        if self.x<=powerup.x+powerup.w<=self.x+self.w and (self.y<=powerup.y+powerup.h<=self.y+self.h or self.y<=powerup.y<=self.y+self.h):
            powerup.estado=True


    def pinta_ranita(self,w):
        w.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h, fill="green")
        w.create_image(self.x+(self.w/2),self.y+(self.h/2),anchor=CENTER,image=self.imagen)