"""
A GUI-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

# Replace these <strings> with your name, student number and email address.
__author__ = "<Your Name>, <Your Student Number>"
__email__ = "<Your Student Email>"


import tkinter as tk
from PIL import Image,  ImageTk
from a2_solution import *
from constants import *
import math

# Uncomment the following imports to import the view classes that represent
# the GUI for each of the tasks that you implement in the assignment.
##from task1 import BasicGraphicalInterface
##from task2 import ImageGraphicalInterface
##from csse7030 import MastersGraphicalInterface



class BasicGraphicalInterface():
    def __init__(self, root, game): 
        self.root = root
        self.game = game
        self.size = self.game.get_grid().get_size()
        self.tick = False


    def draw_backdrop(self):
        self.root.geometry(f"{self.size * CELL_SIZE + INVENTORY_WIDTH}x{self.size * CELL_SIZE + BANNER_HEIGHT}")
        self.canvas = tk.Canvas(self.root, 
            width = self.size * CELL_SIZE + INVENTORY_WIDTH,
            height = self.size * CELL_SIZE + BANNER_HEIGHT
            )
#title
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
#game
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


    def get_crossbow(self):
        for item in self.game.get_player()._inventory._items:
            if item.display() == 'C':
                return item


    def movement(self, key):
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


    def shoot(self, key):
        if self.get_crossbow() != None:
            if self.get_crossbow().is_active():
                if key == 'u':
                    direction = UP
                elif key == 'j':
                    direction = DOWN
                elif key == 'h':
                    direction = LEFT
                elif key == 'k':
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


    def press(self, pressed):
        key = pressed.char
        self.movement(key)
        self.shoot(key)
        return


    def inventory_click(self, event):
        pixel = (event.x, event.y)
        InventoryView.toggle_item_activation(self, pixel, self.game.get_player()._inventory)
        return


    def draw(self, game):
        mapping = game.get_grid().serialize()
        player = game.get_player()

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

        InventoryView.draw(self, player._inventory)
        return


    def move(self, direction):
        self.game.move_player(self.game.direction_to_offset(direction))
        return


    def step(self):
        self.game.step()
        return


    def ticker(self):
        self.tick = False
        return 


    def play(self):
        """
        The play method implements the game loop, constantly prompting the user
        for their action, performing the action and printing the game until the
        game is over.

        
        Parameters:
            game: The game to start playing.
        """
        self.root.bind('<Button-1>', self.inventory_click)
        self.root.bind('<KeyPress>', self.press)
        self.draw_backdrop()
        won_game = False
        lost_game = False

        while not won_game and not lost_game:
            self.canvas.delete("items")

            if self.tick == False:
                self.root.after(1000, self.step)
                self.tick = True
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
    def draw(self, inventory):
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
        if (self.size * CELL_SIZE) < pixel[0] < (self.size * CELL_SIZE + INVENTORY_WIDTH):
            if (BANNER_HEIGHT + CELL_SIZE) < pixel[1] < (BANNER_HEIGHT + CELL_SIZE + len(inventory._items) * CELL_SIZE):
                inventory_position = (math.floor((pixel[1] - BANNER_HEIGHT - CELL_SIZE)/CELL_SIZE))
                item = inventory._items[inventory_position]
                if inventory.any_active():
                    if item.is_active():
                        item.toggle_active()
                    return
                item.toggle_active()
        return




class StatusBar():
    def __init__(self, timer):
        self.timer = timer
        self.moves = 0


    def draw(seld, self):
        self.canvas.create_text(
            (200, CELL_SIZE * self.size + 135),
            text = f'{seld.timer} seconds',
            tags = ('items')
            )   

        self.canvas.create_text(
            (350, CELL_SIZE * self.size + 135),
            text = f'{seld.moves} moves',
            tags = ('items')
            )   
        return

    def quit_button(self, root):
        quit()
        return

    def restart_button(self):
        
        return    





class ImageGraphicalInterface(BasicGraphicalInterface):
    """

    """
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.size = self.game.get_grid().get_size()
        self.tick = False
        self.img_ref = []
        self.statbar = StatusBar(0)

    def draw_img(self, position, img):
        image = ImageTk.PhotoImage(file = img)
        self.img_ref.append(image)
        self.canvas.create_image(position[0], position[1], image = image, tags = ('items'))
        return

    def save_game(self):

        return

    def load_game(self):

        return

    def draw_backdrop(self):
        self.root.geometry(f"{self.size * CELL_SIZE + INVENTORY_WIDTH}x{self.size * CELL_SIZE + BANNER_HEIGHT + CELL_SIZE * 2}")
        self.canvas = tk.Canvas(self.root, 
            height = self.size * CELL_SIZE + BANNER_HEIGHT + CELL_SIZE, 
            width = self.size * CELL_SIZE + INVENTORY_WIDTH
            )


        menu = tk.Menu(self.root)
        filemenu = tk.Menu(menu)
        
        menu.add_cascade(label="File", menu = filemenu)
        filemenu.add_command(label="Restart game", command = self.statbar.restart_button)
        filemenu.add_command(label="Save game", command = self.save_game)
        filemenu.add_command(label="Load game", command = self.load_game)
        filemenu.add_command(label="Quit", command = self.statbar.quit_button)

        self.root.config(menu = menu)
        
#title
        #self.draw_img((50, 50), 'images/banner.png')
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
            text = 'Timer',
            )   

        self.canvas.create_text(
            (350, CELL_SIZE * self.size + 115),
            text = 'Moves Made',
            )   
#status bar buttons
        exit_button = tk.Button(self.root, text = "Restart Game", command = self.statbar.restart_button)
        exit_button.place(x = 500, y = (CELL_SIZE * self.size + 110))
        restart_button = tk.Button(self.root, text = "Exit Game", command = self.statbar.quit_button)
        restart_button.place(x = 500, y = (CELL_SIZE * self.size + 150))
#pack
        self.canvas.pack()
        return


    def draw(self, game):
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
            self.draw_img((x * 50 + 25, y * 50 + 125), img)

        InventoryView.draw(self, player._inventory)
        self.statbar.draw(self)
        return


    def step(self):
        self.game.step()
        self.statbar.timer += 1
        return

    def move(self, direction):
        self.game.move_player(self.game.direction_to_offset(direction))
        self.statbar.moves += 1
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



















