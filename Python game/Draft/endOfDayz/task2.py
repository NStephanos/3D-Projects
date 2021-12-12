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
