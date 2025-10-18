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

    def road_painter(self,w)->None:
        '''
        Function to paint the road

        Attributes:
        -----------
            self.y (int): Road initial position.
            self.h (int): Road height in pixels.


        Returns
        -----------
            None
        '''
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

        def mover(self)->None:
            '''
           Function to move the frog

            Attributes:
            -----------
                self.x (int): Car's current X position (top-left corner).
                self.w (int): Car's width in pixels.
                self.v (int): Car's velocity or step size for the next move.


            Returns
            -----------
                None
            '''
            self.x+=self.v
            if self.x>800:
                self.x=-self.w
            if self.x+self.w<0:
                self.x=800-self.w

        def pinta_coche(self,w):
            '''
            Function to paint the road

            Attributes
            -----------
                self.x (int): Car's current X position (top-left corner).
                self.w (int): Car's width in pixels.
                self.v (int): Car's velocity or step size for the next move.
                self.y (int): Car's current Y position.
                self.h (int): Car's height in pixels.


            Parameters
            -----------
                w (Canvas)
            Returns


            -----------
                None
            '''
            if self.estado:
                w.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h, fill="red")
                w.create_image(self.x + (self.w / 2), self.y + (self.h / 2), anchor=CENTER, image=self.imagen_camion)


    def llena_el_carril(self, anchuras:list[int])->None:
        """
        Populates the lane with a random number of cars.

        This method generates between 3 and 5 cars, assigning them a common
        random velocity. It then places them along the lane, ensuring they
        do not overlap by maintaining a 20-pixel safety margin around each car.

        Attributes:
        -----------
            cotxes_en_el_carril (list): A list of `Cotxe` instances in the lane,
                which this method appends to.

        Parameters:
        -----------
            anchuras (list[int]): A list of possible integer widths from which
                to randomly select for each new car.

        Return:
        -----------
            None

        Side Effects:
        -----------
            Appends the newly created `Cotxe` instances to the
            `self.cotxes_en_el_carril` list, modifying the object's state.
        """
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

        BASE_PATH = os.path.dirname(__file__)
        self.imagen=PhotoImage(Image.open(os.path.join(BASE_PATH, "assets", "vida.png"))).subsample(10,10)

    def moure(self)->None:
        """
        Moves the object horizontally according to its velocity.

        Increments the object's horizontal position (`x`) by its velocity (`v`).
        If the object moves past the right screen boundary (800 pixels),
        its position is reset to the left boundary (0), creating a wrap-around effect.

        Attributes:
        -----------
            self.x (int): The horizontal coordinate of the object, which is modified.
            self.v (int): The horizontal velocity of the object.

        Parameters:
        -----------
            None

        Return:
        -----------
            None

        Side Effects:
        -----------
            Modifies the value of the `self.x` attribute.
        """
        self.x+=self.v
        if self.x>=800:
            self.x=0
    
    def pinta_vida(self,w)->None:
        """Draws the object's image on the canvas under specific conditions.

        This method renders the object on the provided canvas widget, but only if
        its state (`self.estado`) is `False` and its counter (`self.cont`) is exactly 1.
        It first draws an outline-less rectangle to clear the previous frame
        before drawing the new image.

        Attributes:
            self.estado (bool): A flag representing the object's state. Drawing occurs if `False`.
            self.cont (int): A counter that must be equal to 1 for the object to be drawn.
            self.x (int): The horizontal coordinate for drawing.
            self.y (int): The vertical coordinate for drawing.
            self.w (int): The width of the object.
            self.h (int): The height of the object.
            imagen (PhotoImage): The image asset to be rendered.

        Parameters:
            w (tkinter.Canvas): The canvas widget where the object will be drawn.

        Return:
            None

        Side Effects:
            Draws graphics (a rectangle and an image) onto the passed canvas `w`.
        """
        if not self.estado and self.cont==1:
            w.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h, outline="")
            w.create_image(self.x+self.w/2,self.y+self.h/2,anchor=CENTER, image=self.imagen)