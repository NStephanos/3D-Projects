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