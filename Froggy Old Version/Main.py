from tkinter import *
import time
from asfalto import *
from rio import *
from ranita import *
from extras import *

'''MODOS:

0. Juego en sí
1. Pantalla inicio
2. Atropello
3. Victoria
4. Caida al rio


'''



tk=Tk()
w=Canvas(tk,width=800,height=700)
w.pack()

random.seed()

#PART 0: INICIALIZAR EL JUEGO (Creación de los elementos)
altura_carril=50
altura_rio=50
inicio_asfalto=550
inicio_rio=250
anchuras_posibles_coches=[60,90]
anchuras_posibles_troncos=[100,175]

carriles=[]
canales=[]
for i in range(5):
    carriles.append(Carril(inicio_asfalto-i*altura_carril,altura_carril))
    canales.append(Canal(inicio_rio-i*altura_rio,altura_rio))

for i in range(5):
    carriles[i].llena_el_carril(anchuras_posibles_coches)
    canales[i].llena_el_canal(anchuras_posibles_troncos)


ranita=Rana(375,655)

#EXTRAS
avion=Avion(5,60,100)
i=random.randint(0,4)
vida=PowerUp(400,carriles[i].y+10,6.8)


modo=1
pantalla=Pantalla(400,350,modo)

while True:
    if modo!=0:
        modo=pantalla.pintar_pantalla(w,modo,vida)
        #Para asgurarme de que todo vuelva al estado inicial cuando salgo de alguna de las pantallas
        ranita.x=375
        ranita.y=655
        avion.tiempo_inicio=time.time()
        avion.y=-200
    else:
        w.delete("all")
        avion.activacion(ranita)

        playa=ImageTk.PhotoImage(Image.open("arena.png").resize((800,100)))
        w.create_image(400,650,anchor=CENTER,image=playa)
        w.create_image(400,300,anchor=CENTER,image=playa)
        w.create_image(400,25,anchor=CENTER,image=playa)


        #PART 1.1: MOVIMENT GRANOTA
        ranita.tecla()

        #PART 1.2 MOVIMENT ELEMENTS
        for carril in carriles:
            for cotxe in carril.cotxes_en_el_carril:
                cotxe.moure()

        for canal in canales:
            for tronco in canal.troncos_en_el_canal:
                tronco.moure()

        vida.moure()


        #PART 2: DETECCIÓ XOCS
        for carril in carriles:
            for cotxe in carril.cotxes_en_el_carril:
                modo=ranita.detecta_choque(cotxe,vida,modo)

        modo=ranita.pasajera(canales,vida,modo)
        ranita.pasajera_avion(avion)
        ranita.coger_powerup(vida)

        #PART 3: PINTAR PANTALLA
        for carril in carriles:
            carril.pinta_carril(w)
            for cotxe in carril.cotxes_en_el_carril:
                cotxe.pinta_cotxe(w)

        vida.pinta_vida(w)
 
        for canal in canales:
            canal.pinta_canal(w)
            for tronco in canal.troncos_en_el_canal:
                tronco.pinta_tronco(w)

        if avion.estado:
            avion.mover()
            avion.pinta(w)

        marcador_vidas(vida,w)
        modo=ranita.ganadora(modo)
        ranita.pinta_ranita(w)

    w.update()
    time.sleep(50/1000)