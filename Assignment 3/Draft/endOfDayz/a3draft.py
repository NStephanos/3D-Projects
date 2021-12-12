"""
A GUI-based zombie survival game wherein the player has to reach
the hospital whilst evading zombies.
"""

# Replace these <strings> with your name, student number and email address.
__author__ = "<Your Name>, <Your Student Number>"
__email__ = "<Your Student Email>"


import tkinter as tk
from a2_solution import *
from constants import *
import math

# Uncomment the following imports to import the view classes that represent
# the GUI for each of the tasks that you implement in the assignment.
##from task1 import BasicGraphicalInterface
##from task2 import ImageGraphicalInterface
##from csse7030 import MastersGraphicalInterface



class AbstractGrid(tk.Canvas):
    def __init__ (self, master, rows, cols, width, height, **kwargs):
        self.master = master

    def get_bbox(self, position):
        return

    def pixel_to_position(self, pixel):
        return

    def get_position_center(self, position):
        return

    def annotate_position(self, position, text):
        return



class BasicMap(AbstractGrid):

    def draw_entity(self, position, tile_type):
        return

class InventoryView(AbstractGrid):
    def __init__(self, master, rows, **kwargs):
        self.master = master

    def draw(self, inventory):

        for (x, item) in enumerate(inventory._items):

            text_colour = 'black'

            if item._using:
                self.canvas.create_rectangle(
                    self.size * 50,
                    150 + 50 * x,
                    self.size * 50 + 200,
                    200 + 50 * x, 
                    fill = DARK_PURPLE,
                    tags = ('items')
                    )

                text_colour = 'white'
            
            self.canvas.create_text(
                (self.size * 50 + 50, 175 + 50 * x),
                text = item,
                fill = text_colour,
                tags = ('items')
                )

            self.canvas.create_text(
                (self.size * 50 + 50, 175 + 50 * x),
                text = item,
                fill = text_colour,
                tags = ('items')
                )

        return

    def toggle_item_activation(self, pixel, inventory):

        if (self.size * 50) < pixel[0] < (self.size * 50 + 200):
            x = math.floor((pixel[1] - 150)/ 50)


            item = inventory._items[x]
            if inventory.any_active():
                if item.is_active():
                    item.toggle_active()
                return
            item.toggle_active()

        return


class BasicGraphicalInterface():
    def __init__(self, root, size, game): 
        self.root = root
        self.size = size
        self.root.geometry(f"{self.size * 50 + 200}x{self.size * 50 + 100}")
        self.game = game

        self.canvas = tk.Canvas(self.root, bg='orange', 
            height = 100 + self.size * 50, 
            width = 200 + self.size * 50
            )
#title
        self.canvas.create_rectangle(
            0,
            0,
            200 + self.size * 50,
            100,
            fill = DARK_PURPLE
            )
#game
        self.canvas.create_rectangle(
            0,
            100,
            self.size * 50,
            100 + self.size * 50, 
            fill = LIGHT_BROWN 
            )
#inventory
        self.canvas.create_rectangle(
            self.size * 50,
            100,
            200 + self.size * 50,
            200 + self.size * 50, 
            fill = LIGHT_PURPLE  
            )

        self.canvas.create_text(
            (self.size * 50 + 100, 125),
            text = 'Inventory',
            fill = DARK_PURPLE,
            )

        self.canvas.pack()

        self.after = False

    def get_crossbow(self):
        for item in self.game.get_player()._inventory._items:
            if item.display() == 'C':
                return item

    def press(self, e):

        key = e.char
        direction = None

        if key == 'w':
            direction = UP
        elif key == 's':
            direction = DOWN
        elif key == 'a':
            direction = LEFT
        elif key == 'd':
            direction = RIGHT
        else:
            direction = None

        if direction != None:
            self.move(direction)


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

                print('crossbow')
                print(direction)
                print(key)

                player = self.game.get_player()

                # Fire the weapon in the indicated direction, if possible.
                if direction in DIRECTIONS:
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

    def inventory_click(self, event):

        pixel = (event.x, event.y)

        print(pixel)


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

    def play(self, game):
        """
        The play method implements the game loop, constantly prompting the user
        for their action, performing the action and printing the game until the
        game is over.

        
        Parameters:
            game: The game to start playing.
        """

        self.root.bind('<Button-1>', self.inventory_click)

        self.root.bind('<KeyPress>', self.press)
        
        won_game = False
        lost_game = False

        while not won_game and not lost_game:
            self.canvas.delete("items")

            if self.after == False:
                self.root.after(1000, self.step)
                self.after = True
                self.root.after(1000, self.bad_choices)

            self.draw(game)
            self.root.update()

            #action = input(ACTION_PROMPT)
            #self.handle_action(game, action)

            if game.has_won():
                print(WIN_MESSAGE)
                won_game = True

            if not won_game and game.has_lost():
                print(LOSE_MESSAGE)
                lost_game = True
        
        return


    def bad_choices(self):
        self.after = False
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
    	gui = MastersGraphicalInterface

    app = gui(root, game.get_grid().get_size(), game)
    app.play(game)


if __name__ == '__main__':
    main()

























