"""
A GUI-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

# Replace these <strings> with your name, student number and email address.
__author__ = "<Noah Stephanos>, <44309912>"
__email__ = "<n.stephanos@uqconnect.edu.au>"

import math
import tkinter as tk
from PIL import Image,  ImageTk
from a2_solution import *
from constants import *

'''

This file references a completely unchanged a2_solution and constants

IKJL are used as up down left right to fire the crossbow

'''


class BasicGraphicalInterface():
    '''
    The Basic GUI class holds all the vairables and logic needed to draw the game
    '''
    def __init__(self, root, game): 
        '''
        The GUI class is constructed from tkinter and the game object

        Parameters:
            root: The tkinter object
            game: the game object
        '''
        self.root = root
        self.game = game
        self.size = self.game.get_grid().get_size()
        self.tick = True


    def draw_backdrop(self):
        '''
        draw_backdrop will initilise the GUI and the canvas needed for the game
        it is called by the play function before gameplay starts
        it will draw the backdrop elements that the game elements will go on top of
        '''
        self.root.geometry(f"{self.size * CELL_SIZE + INVENTORY_WIDTH}x{self.size * CELL_SIZE + BANNER_HEIGHT}")
        self.canvas = tk.Canvas(self.root, 
            width = self.size * CELL_SIZE + INVENTORY_WIDTH,
            height = self.size * CELL_SIZE + BANNER_HEIGHT
            )

#title card
        self.canvas.create_rectangle(
            0,
            0,
            self.size * CELL_SIZE + INVENTORY_WIDTH,
            BANNER_HEIGHT,
            fill = DARK_PURPLE
            )
        self.canvas.create_text(
            ((self.size * CELL_SIZE + INVENTORY_WIDTH)/2, BANNER_HEIGHT/2),
            text = 'End of DayZ',
            fill = 'White',

            )
#game board
        self.canvas.create_rectangle(
            0,
            BANNER_HEIGHT,
            self.size * CELL_SIZE,
            self.size * CELL_SIZE + BANNER_HEIGHT, 
            fill = LIGHT_BROWN 
            )

#inventory
        self.canvas.create_rectangle(
            self.size * CELL_SIZE,
            BANNER_HEIGHT,
            self.size * CELL_SIZE + INVENTORY_WIDTH,
            self.size * CELL_SIZE + INVENTORY_WIDTH, 
            fill = LIGHT_PURPLE  
            )

        self.canvas.create_text(
            (self.size * CELL_SIZE + INVENTORY_WIDTH/2, BANNER_HEIGHT + CELL_SIZE/2),
            text = 'Inventory',
            fill = DARK_PURPLE,
            )

        self.canvas.pack()
        return


    def press(self, pressed):
        '''
        press will be called on any key press and determain what action is to be taken

        Parameters:
            presses: The key that was pressed
        '''
        key = pressed.char
        self.movement(key)
        self.shoot(key)
        return


    def inventory_click(self, event):
        '''
        click will be called on any click and determain what action is to be taken

        Parameters:
            event: The x,y position that was clicked
        '''
        pixel = (event.x, event.y)
        InventoryView.toggle_item_activation(self, pixel, self.game.get_player()._inventory)
        return

    def movement(self, key):
        '''
        checks if the key pressed is a valid move and calls the move function if valid

        Parameters:
            key: The key that was pressed
        '''
        direction = None
        if key == 'w':
            direction = UP
        elif key == 's':
            direction = DOWN
        elif key == 'a':
            direction = LEFT
        elif key == 'd':
            direction = RIGHT

        if direction in DIRECTIONS:
            self.move(direction)
        return

    def move(self, direction):
        '''
        calles the moveplayer function from a2 to move the player position

        Parameters:
            direction: The direction to move
        '''
        self.game.move_player(self.game.direction_to_offset(direction))
        return

    def get_crossbow(self):
        '''
        returns the crossbow object
        '''
        for item in self.game.get_player()._inventory._items:
            if item.display() == 'C':
                return item

    def shoot(self, key):
        '''
        handles the real time shooting logic 

        Parameters:
            key: The key that was pressed

        NOTE: the keys IKJL are used in place of arrow keys to shoot the crossbow 
              because tkinter wouldnt recognise arrow keys dunno why
        '''
        if self.get_crossbow() != None:
            if self.get_crossbow().is_active():
                if key == 'i':
                    direction = UP
                elif key == 'k':
                    direction = DOWN
                elif key == 'j':
                    direction = LEFT
                elif key == 'l':
                    direction = RIGHT
                else:
                    direction = None

                # Fire the weapon in the indicated direction, if possible.
                if direction in DIRECTIONS:
                    player = self.game.get_player()
                    start = self.game.get_grid().find_player()
                    offset = self.game.direction_to_offset(direction)
                    if start is None or offset is None:
                        return  # Should never happen.

                    # Find the first entity in the direction player fired.
                    first = first_in_direction(
                        self.game.get_grid(), start, offset
                    )

                    # If the entity is a zombie, kill it.
                    if first is not None and first[1].display() in ZOMBIES:
                        position, entity = first
                        self.game.get_grid().remove_entity(position)
        return

    def draw(self, game):
        '''
        draw will check the game grid for objects and draw 
        every entitiy in the grid as well as the players inventory

        Parameters:
            game: The game object
        '''
        mapping = game.get_grid().serialize()

        for (position, token) in mapping.items():
            (x, y) = position
            text_colour = 'black'
            if token == 'P' or token == 'H':
                colour = DARK_PURPLE
                text_colour = 'white'
            elif token == 'C' or token == 'G':
                colour = LIGHT_PURPLE                
            else:
                colour = LIGHT_GREEN

#draw objects
            self.canvas.create_rectangle(
                x * 50,
                y * 50 + 100,
                x * 50 + 50,
                y * 50 + 150, 
                fill = colour,
                tags = ('items')
                )

            self.canvas.create_text(
                (x * 50 + 25, y * 50 + 125),
                text = token,
                fill = text_colour,
                tags = ('items')
                )

#draw inventory
        player = game.get_player()
        InventoryView.draw(self, player._inventory)
        return

    def step(self):
        '''
        Calls the step function
        '''
        self.game.step()
        return

    def ticker(self):
        '''
        resets the game tick
        '''
        self.tick = True
        return 

    def play(self):
        """
        The play method implements the game loop, clearing and drawing the game board
        gameplay will stop when the player has won or lost
        """
        self.root.bind('<Button-1>', self.inventory_click)
        self.root.bind('<KeyPress>', self.press)
        self.draw_backdrop()
        won_game = False
        lost_game = False

        while not won_game and not lost_game:
            self.canvas.delete("items")

            #The game tick moves once every second to call step for 
            #entities other than the player
            if self.tick == True:
                self.root.after(1000, self.step)
                self.tick = False
                self.root.after(1000, self.ticker)

            self.draw(self.game)
            self.root.update()

            if self.game.has_won():
                print(WIN_MESSAGE)
                won_game = True

            if not won_game and self.game.has_lost():
                print(LOSE_MESSAGE)
                lost_game = True
        return







class InventoryView(BasicGraphicalInterface):
    '''
    subclass of the GUI handles drawing the items onto the inventory 
    and handles the activation and deactivation of the items
    '''
    def draw(self, inventory):
        '''
        draw this will draw all the items in the players inventory onto the inventory
        section of the GUI

        Parameters:
            inventory: The invetory object
        '''
        for (inventory_position, item) in enumerate(inventory._items):
            text_colour = 'black'
            if item._using:
                text_colour = 'white'
                self.canvas.create_rectangle(
                    self.size * CELL_SIZE,
                    150 + CELL_SIZE * inventory_position,
                    self.size * CELL_SIZE + INVENTORY_WIDTH,
                    200 + CELL_SIZE * inventory_position, 
                    fill = DARK_PURPLE,
                    tags = ('items')
                    )
#text
            self.canvas.create_text(
                (self.size * CELL_SIZE + CELL_SIZE, 175 + CELL_SIZE * inventory_position),
                text = item,
                fill = text_colour,
                tags = ('items')
                )
        return


    def toggle_item_activation(self, pixel, inventory):
        '''
        this will take the pixel that was clicked and check which inventory item that matches to
        and will activate or deactivate the item appropriately 

        Parameters:
            pixel: the pixel that was clicked
            inventory: The invetory object
        '''
        if (self.size * CELL_SIZE) < pixel[0] < (self.size * CELL_SIZE + INVENTORY_WIDTH):
            #check if click was in the inventory section
            if (BANNER_HEIGHT + CELL_SIZE) < pixel[1] < (BANNER_HEIGHT + CELL_SIZE + len(inventory._items) * CELL_SIZE):
                #check which item was clicked on
                inventory_position = (math.floor((pixel[1] - BANNER_HEIGHT - CELL_SIZE)/CELL_SIZE))
                item = inventory._items[inventory_position]
                #toggel the item activation
                if inventory.any_active():
                    if item.is_active():
                        item.toggle_active()
                    return
                item.toggle_active()
        return









class ImageGraphicalInterface(BasicGraphicalInterface):
    """
    The Image GUI is a continuation of the basic GUI and will draw images onto the canvas 
    instead of rectangles as well as implement the aditional functionality of task2
    """
    def __init__(self, root, game):
        '''
        The GUI class is constructed from tkinter and the game object

        Parameters:
            root: The tkinter object
            game: the game object
        '''
        self.root = root
        self.game = game
        self.size = self.game.get_grid().get_size()
        self.tick = True
        self.img_ref = []
        self.statbar = StatusBar(0)

    def draw_img(self, position, img, tag):
        '''
        method for drawing images onto the canvas
        and stored the image reference for tkinter

        Parameters:
            position: The position of the image
            img: the path to the image
            tag: the tag for the image
        '''
        image = ImageTk.PhotoImage(file = img)
        self.img_ref.append(image)
        self.canvas.create_image(position[0], position[1], image = image, tags = (tag))
        return


    def draw_backdrop(self):
        '''
        draw_backdrop will initilise the GUI and the canvas needed for the game
        it is called by the play function before gameplay starts
        it will draw the backdrop elements that the game elements will go on top of

        real sorry about this one tkinter is a nightmare

        it will draw all the individual objects and store the references tkinter needs
        in the gui object
        '''
        self.root.geometry(f"{self.size * CELL_SIZE + INVENTORY_WIDTH}x{self.size * CELL_SIZE + BANNER_HEIGHT + CELL_SIZE * 2}")
        self.canvas = tk.Canvas(self.root, 
            height = self.size * CELL_SIZE + BANNER_HEIGHT + CELL_SIZE, 
            width = self.size * CELL_SIZE + INVENTORY_WIDTH
            )

#file menu
        menu = tk.Menu(self.root)
        filemenu = tk.Menu(menu)
    
        menu.add_cascade(label="File", menu = filemenu)
        filemenu.add_command(label="Restart game", command = self.statbar.restart_button)
        filemenu.add_command(label="Save game", command = self.save_game)
        filemenu.add_command(label="Load game", command = self.load_game)
        filemenu.add_command(label="Quit", command = self.statbar.quit_button)

        self.root.config(menu = menu)
        
#title
        image = Image.open('images/banner.png')
        image = image.resize((600, 100), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        self.banner = image
        self.canvas.create_image(350, 50, image = image)

#gameboard
        image = ImageTk.PhotoImage(file = 'images/tileable_background.png')
        self.tile = image
        for x in range(self.size):
            for y in range(self.size):
                self.canvas.create_image((CELL_SIZE * x + 25), (CELL_SIZE * y + 125), image = image)

#inventory
        self.canvas.create_rectangle(
            self.size * CELL_SIZE,
            BANNER_HEIGHT,
            self.size * CELL_SIZE + INVENTORY_WIDTH,
            self.size * CELL_SIZE + BANNER_HEIGHT, 
            fill = LIGHT_PURPLE  
            )

        self.canvas.create_text(
            (self.size * CELL_SIZE + INVENTORY_WIDTH/2, BANNER_HEIGHT + CELL_SIZE/2),
            text = 'Inventory',
            fill = DARK_PURPLE,
            )

#status bar
        self.canvas.create_rectangle(
            0,
            self.size * CELL_SIZE + BANNER_HEIGHT,
            self.size * CELL_SIZE + INVENTORY_WIDTH,
            self.size * CELL_SIZE + BANNER_HEIGHT + CELL_SIZE, 
            fill = 'white',
            outline = 'white'
            )

        image = ImageTk.PhotoImage(file = 'images/chaser.png')
        self.runner = image
        self.canvas.create_image(50, (CELL_SIZE * self.size + 125), image = image)

        image = ImageTk.PhotoImage(file = 'images/chasee.png')
        self.chase = image
        self.canvas.create_image((CELL_SIZE * self.size + 150), (CELL_SIZE * self.size + 125), image = image)

        self.canvas.create_text(
            (200, CELL_SIZE * self.size + 115),
            text = 'Timer')   

        self.canvas.create_text(
            (350, CELL_SIZE * self.size + 115),
            text = 'Moves Made')   

#status bar buttons
        exit_button = tk.Button(self.root, text = "Restart Game", command = self.statbar.restart_button)
        exit_button.place(x = 500, y = (CELL_SIZE * self.size + 110))

        restart_button = tk.Button(self.root, text = "Exit Game", command = self.statbar.quit_button)
        restart_button.place(x = 500, y = (CELL_SIZE * self.size + 150))
#pack
        self.canvas.pack()
        return



    def step(self):
        '''
        same as before but increments the timer every step
        '''
        self.game.step()
        self.statbar.timer += 1
        return

    def move(self, direction):
        '''
        same as before but increments the move count every player move
        '''
        self.game.move_player(self.game.direction_to_offset(direction))
        self.statbar.moves += 1
        return

    def save_game(self):
        '''

        '''
        print('game saved')
        return

    def load_game(self):
        '''

        '''
        print('game loaded')
        return

    def draw(self, game):
        '''
        draw will check the game grid for objects and draw 
        every entitiy in the grid as well as the players inventory

        Parameters:
            game: The game object
        '''
        mapping = game.get_grid().serialize()
        player = game.get_player()
        self.img_ref = []

        for (position, token) in mapping.items():
            (x, y) = position
            if token == 'P':
                img = 'images/hero.png'
            elif token == 'H':
                img = 'images/hospital.png'
            elif token == 'C':
                img = 'images/crossbow.png'
            elif token == 'G':
                img = 'images/garlic.png'
            elif token in ZOMBIES:
                img = 'images/zombie.png'                
#draw objects
            self.draw_img((x * 50 + 25, y * 50 + 125), img, 'items')

        InventoryView.draw(self, player._inventory)
        self.statbar.draw(self)
        return



class StatusBar():
    '''
    statusbar class for holding all the information in the statusbar 
    as well as drawing the timers and counters
    '''
    def __init__(self, timer):
        '''
        starts the timer and counter

        Parameters:
            timer: initilaises the timer
        '''
        self.timer = timer
        self.moves = 0

    def draw(test, self):
        '''
        draw will check the game grid for objects and draw 
        every entitiy in the grid as well as the players inventory

        Parameters:
            test: imma be real chief
            self: this just works
        '''
        self.canvas.create_text(
            (200, CELL_SIZE * self.size + 135),
            text = f'{test.timer} seconds',
            tags = ('items')
            )   

        self.canvas.create_text(
            (350, CELL_SIZE * self.size + 135),
            text = f'{test.moves} moves',
            tags = ('items')
            )   
        return

    def quit_button(self):
        '''
        quits
        '''
        quit()
        return

    def restart_button(self):
        print('game restarted')
        return    



def main() -> None:
    """Entry point to gameplay."""
    game = advanced_game(MAP_FILE)

    root = tk.Tk()
    root.title(TITLE)

    if TASK == 1:
    	gui = BasicGraphicalInterface
    elif TASK == 2:
    	gui = ImageGraphicalInterface
    else:
    	gui = BasicGraphicalInterface

    app = gui(root, game)
    app.play()


if __name__ == '__main__':
    main()



















