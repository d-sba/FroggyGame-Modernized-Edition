import time
from tkinter import CENTER, font
import keyboard
from PIL import Image,ImageTk

intervalo_segundos=5


class Avion:
    def __init__(self,y,w,h):
        self.x=0
        self.y=y
        self.w=w
        self.h=h
        self.v=20
        self.imagen=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/1er cuatri/Programacion avanzada/RANITAOFICIAL/avion.png").resize((self.w, self.h)))
        self.estado=False
        self.tiempo_inicio=0
    
    def mover(self):
        self.y+=self.v
        if self.y+self.h/2>800:
            self.y=-100
            self.estado=False
            self.tiempo_inicio=time.time()

    def activacion(self,ranita):
        if time.time()-self.tiempo_inicio>intervalo_segundos and not self.estado:
            self.estado=True
            self.x=ranita.x-10
    
    def pinta(self,canvas):
        canvas.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h,fill="brown")
        canvas.create_image(self.x + (self.w / 2), self.y + (self.h / 2), anchor=CENTER, image=self.imagen)

class Pantalla:
    def __init__(self,x,y,modo):
        self.posx=x
        self.posy=y
        self.tiempo_inicio=time.time()
        self.imagen=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/1er cuatri/Programacion avanzada/RANITAOFICIAL/pantallainicio.png").resize((2*self.posx,2*self.posy)))
    

    def pintar_pantalla(self,canvas,modo,vida):
        canvas.delete("all") 

        #SELECCION DE IMAGEN
        if modo==2:
            self.imagen=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/Programacion avanzada/1er cuatri/RANITAOFICIAL/atropellada.png").resize((2*self.posx,2*self.posy)))
        if modo==3:
            self.imagen=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/Programacion avanzada/1er cuatri/RANITAOFICIAL/guanyadora.png").resize((2*self.posx,2*self.posy)))
        if modo==4:
            self.imagen=ImageTk.PhotoImage(Image.open("C:/Users/dasab/Desktop/UNIVERSIDAD/5. Quinto/Programacion avanzada/1er cuatri/RANITAOFICIAL/ahogada.png").resize((2*self.posx,2*self.posy)))

        canvas.create_image(400, 350, anchor=CENTER, image=self.imagen)
        
        
        
        #CUADRADO DE TEXTO
        x1,y1=300,450
        x2,y2=500,500
        x=[x1,x2,y1,y2]

        if modo==2:
            x[0]=170
            x[1]=430
        elif modo!=1:
            x[0]-=35
            x[1]+=35
            if modo==3:
                x[2]+=25
                x[3]+=25
            if modo==4:
                x[0]-=45
                x[1]-=45
  
        texto="hola"
        if modo==1:
            texto="Pulsa espacio para jugar"
        elif modo==2 or modo==3 or modo==4:
            texto="Pulsa espacio para jugar de nuevo"


        #CODIGO AVION
        tiempo_visible = 1.1
        tiempo_entre_apariciones = 0.5

        tiempo_transcurrido = time.time() - self.tiempo_inicio
        if tiempo_transcurrido % (tiempo_visible + tiempo_entre_apariciones) < tiempo_visible:
            canvas.create_rectangle(x[0], x[2], x[1], x[3], fill="light pink")
            canvas.create_text((x[0] + x[1]) / 2, (x[2] + x[3]) / 2, text=texto, fill="black", font=font.Font(family="TkFixedFont", size=12, weight="bold"))

        if keyboard.is_pressed('space'):
            modo=0
            vida.cont=1
            vida.estado=False
        return modo

  
def marcador_vidas(vida,canvas):
    if vida.estado==False:
        texto="Vidas: 0"
    else: 
        texto="Vidas: 1"

    x1,y1=720,10
    x2,y2=790,40
    canvas.create_rectangle(x1,y1,x2,y2,fill="grey")
    canvas.create_text((x1+x2)/2,(y1+y2)/2,text=texto,fill="white", font=("Arial",12))
