from tkinter import CENTER, PhotoImage, Canvas
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

    def limites(self)->int:
        '''
        Function to check that the frog is within bounds. It is assumed that the canvas is 800x700

        We don't check collision with the upper bound, because if the frog has arrived to the upper limit, 
        then the game is over


        Attributes:
        -----------
            self.x (int): Frog's current X position (top-left corner).
            self.y (int): Frog's current Y position (top-left corner).
            self.w (int): Frog's width in pixels.
            self.h (int): Frog's height in pixels.
            self.v (int): Frog's velocity or step size for the next move.


        Returns
        -----------
        int: A code indicating different behaviours:
            1. Collision with the left Border
            2. Collision with the bottom 
            3. Collision with the right border
            4. No Collison
        '''
        if self.x-self.v<0:
            return 1
        elif self.x+self.w+self.v>800:
            return 3
        elif self.y+self.h+self.v>700:
            return 2
        else:
            return 0


    def movimientos(self,direccion: str)->None:
        '''
        Function to move the frog

        Attributes:
        -----------
            self.moverse_a_saltos (Dict): a dictionary containing the 4 different possible directions (arrows in the keyboard) as keys and True/False
                as values. This ensures that the frog moves with each press of the keyboards, and that keeping it pushed doesn't make the frog
                to move continously
            self.viajera (Bool): It indicates if the frog is in a certain state where it can't move to any direction (self.viajera=True)

        Parameters:
        -----------
            direccionn(string): it indicates the desired direction to move the frog to (as entered by keyboard)
        '''
        if self.moverse_a_saltos[direccion] and not self.viajera:
            if direccion=='up arrow':
                self.y-=self.v        
            elif direccion=='down arrow' and self.limites()!=2:
                self.y+=self.v
            elif direccion=='right arrow'and self.limites()!=3:
                self.x+=self.v
            elif direccion=='left arrow' and self.limites()!=1:
                self.x-=self.v


    def tecla(self)->None:
        """
        Handles keyboard input to trigger single-shot character movements.

        Attributes:
        -----------
            self.moverse_a_saltos (dict[str, bool]): A dictionary tracking key states.
                Keys are key names (e.g., 'up', 'w'), and values are flags
                indicating if the key press has already been processed (True)
                or is ready to be processed (False).

        Side Effects:
            - Modifies the boolean values within the `self.moverse_a_saltos` dictionary.
            - Calls the `self.moverse()` method upon a valid key press.
        """
        for i in self.moverse_a_saltos:
            if keyboard.is_pressed(i):
                if not self.moverse_a_saltos[i]:
                    self.moverse_a_saltos[i]=True
                    self.movimientos(i)
            if not keyboard.is_pressed(i):
                self.moverse_a_saltos[i]=False


    def detecta_choque(self,cotxe,powerup,modo:int)->int:
        '''
        Function to detect collisions. If the user has an extra life, the object which it has collided with dissapears.

        Attributes:
        -----------
            self.x (int): Frog's current X position (top-left corner).
            self.y (int): Frog's current Y position (top-left corner).
            self.viajera (Bool): It indicates if the frog is in a certain state where it can't collide

            
        Parameters:
        -----------
            cotxe (Class Cotxe): The objects it might collide with
            powerup (Class Powerup): The extralife
            moodo (int): It indicates the game status


        Returns
        -----------
        int: A code indicating the game status

        Side Effects
        -----------
            Modifies `cotxe.estado` to False if a collision having the power-up activated happens.
            Modifies `powerup.estado` and `powerup.cont` upon consumption.
        '''
        if self.viajera==False and cotxe.estado==True and (cotxe.x<self.x<cotxe.x+cotxe.w or cotxe.x+cotxe.w>self.x+self.w>cotxe.x) and (self.y<=cotxe.y+cotxe.h<=self.y+self.h or self.y<=cotxe.y<=self.y+self.h):
            if powerup.estado==True:
                cotxe.estado=False
                powerup.estado=False
                powerup.cont+=1
            else:
                modo=2
        return modo
            


    def pasajera(self,canales,powerup,modo:int)->int:
        '''
        Manages the frog's state within the river channels.

        This function checks if the frog is on a moving log and updates its
        position to move along with it. If the frog is in the water but not
        on a log, it triggers a game-over state, potentially consuming a
        power-up as an extra life.

        Attributes:
        -----------
            self.x (int): The frog's current X-coordinate.
            self.y (int): The frog's current Y-coordinate.
            self.w (int): The frog's width.
            self.h (int): The frog's height.
            self.viajera (bool): A flag indicating if the frog is in a state
                where it is considered to be in the water.

        Parameters:
        -----------
            canales (list): A list of channel objects that contain logs.
            powerup (Powerup): The power-up object that can be used as an extra life.
            modo (int): The current game mode/status.

        Returns:
        -----------
            int
                The updated game mode. Returns 4 if the frog falls into the
                water without a power-up or is carried off-screen by a log.
        '''
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

    def pasajera_avion (self,avion)->None:
        '''
        Handles the frog's interaction with the airplane, allowing it to board and disembark.

        This method checks if the frog has landed on the airplane. If so, it sets
        the frog's state to "passenger" (`self.viajera`), locking its position
        relative to the plane and matching its velocity. It also handles the
        logic for dropping the frog off once it reaches the bottom of the screen.

        Attributes:
        -----------
            self.viajera (bool): A flag that is True when the frog is riding the plane.
            self.x (int): The frog's X-coordinate, which is modified by this function.
            self.y (int): The frog's Y-coordinate, which is modified by this function.
            self.v (int): The frog's velocity, which is synchronized with the plane.
            self.w (int): The frog's width, used for collision detection.

        Parameters:
        -----------
            avion (Avion): The airplane object the frog interacts with. It must have
                x, y, w, h, and v attributes.

        Returns:
        -----------
            None
                This function does not return any value; it modifies the frog's
                attributes directly (side effects).
        '''
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

    def ganadora(self,modo:int)->int:
        '''
        Determines if the user has won and the game is over

        Attributes:
        -----------
            self.y (int): The frog's Y-coordinate, which is modified by this function.
            self.h (int): The frog's height

        Parameters:
        -----------
            modo (int): A code indicating the game status

        Returns:
        -----------
            None
                This function does not return any value; it modifies the game status
        '''
        if self.y+self.h/2<50:
            return 3
        return modo

    def coger_powerup(self,powerup)->None:
        '''
        Checks for a collision with a power-up and collects it if they touch.

        This method determines if the frog's bounding box overlaps with the
        power-up's bounding box. If a collision is detected, it activates
        the power-up by setting its 'estado' attribute to True.

        Attributes:
        -----------
            self.x (int): The frog's current X-coordinate.
            self.y (int): The frog's current Y-coordinate.
            self.w (int): The frog's width.
            self.h (int): The frog's height.

        Parameters:
        -----------
            powerup (Powerup): The power-up object to check against. It must
                have x, y, w, h, and a modifiable 'estado' attribute.

        Returns:
        -----------
            None
                This function does not return a value. It directly modifies
                the state of the power-up object.
        '''
        if self.x<=powerup.x+powerup.w<=self.x+self.w and (self.y<=powerup.y+powerup.h<=self.y+self.h or self.y<=powerup.y<=self.y+self.h):
            powerup.estado=True


    def pinta_ranita(self,w: Canvas)->None:
        '''
        Checks for a collision with a power-up and collects it if they touch.

        This method determines if the frog's bounding box overlaps with the
        power-up's bounding box. If a collision is detected, it activates
        the power-up by setting its 'estado' attribute to True.

        Attributes:
        -----------
            self.x (int): The frog's current X-coordinate.
            self.y (int): The frog's current Y-coordinate.
            self.w (int): The frog's width.
            self.h (int): The frog's height.

        Parameters:
        -----------
            w (Canvas): The canvas where the frog will be painted

        Returns:
        -----------
            None
                This function does not return a value. It directly modifies
                the state of the power-up object.
        '''
        w.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h, fill="green")
        w.create_image(self.x+(self.w/2),self.y+(self.h/2),anchor=CENTER,image=self.imagen)