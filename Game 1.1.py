from tkinter import Canvas, Tk, Frame, BOTH, Button


class GameOfLife(object):
    # input: height of the game window, width of the game window, the cell size of the playing field in pixels
    def __init__(self, window_height=480, window_width=640, cell_size=15):
        self.UPDATE_SPEED = 300  # frequents of game field updating in ms
        self.root = Tk()
        self.root.title("GameOfLife")
        self.window_height = window_height
        self.window_width = window_width
        self.cell_size = cell_size
        config_string = "{0}x{1}".format(self.window_width, self.window_height + 32)
        self.root.geometry(config_string)
        self.field_height = self.window_height // self.cell_size
        self.field_width = self.window_width // self.cell_size
        self.canvas = Canvas(self.root, height=self.window_height)
        self.canvas.pack(fill=BOTH)
        self.frame = Frame(self.root)
        self.frame.pack(side='bottom')
        # creating buttons
        self.button_step = Button(self.frame, text='Step', command=self.step)
        self.button_clear = Button(self.frame, text='Clear', command=self.clear)
        self.button_start = Button(self.frame, text='Start', command=self.start)
        self.button_stop = Button(self.frame, text='Stop', command=self.stop)
        self.button_start.pack(side='left')
        self.button_clear.pack(side='right')
        self.button_step.pack(side='right')
        self.button_stop.pack(side='left')
        # setting mouse events
        self.canvas.bind('<B1-Motion>', self.mouse_bind)
        self.canvas.bind('<ButtonPress>', self.mouse_bind)
        # creating array
        self.matrix = []
        for i in range(self.field_height):
            row_of_gaming_field = []
            for j in range(self.field_width):
                row_of_gaming_field.append(self.cell(self.canvas, self.cell_size, i, j))
            self.matrix.append(row_of_gaming_field)
        # start_key is a flag that necessary to control the revival of the playing field
        self.start_key = True

    # this function starts the game
    def run(self):
        self.root.mainloop()

    # class determining the cell of the playing field
    class cell(object):
        def __init__(self, canvas, cell_size, row, column):
            self.row = row
            self.column = column
            self.alive = False
            self.need_to_update = False
            self.print = canvas.create_rectangle(2 + cell_size * column, 2 + cell_size * row, cell_size + cell_size *
                                            column - 2, cell_size + cell_size * row - 2, fill="white")

    # this function updates the state of the cell
    # input: i, j coordinates of the cell in the playing field
    def update_cell(self, i, j):
        alive_neighbourhoods = 0
        if i - 1 > -1 and j - 1 > -1 and self.matrix[i - 1][j - 1].alive:
                alive_neighbourhoods += 1
        if j - 1 > -1 and self.matrix[i][j - 1].alive:
                alive_neighbourhoods += 1
        if i - 1 > -1 and self.matrix[i - 1][j].alive:
                alive_neighbourhoods += 1
        if i + 1 < self.field_height and j + 1 < self.field_width and self.matrix[i + 1][j + 1].alive:
                alive_neighbourhoods += 1
        if i - 1 > -1 and j + 1 < self.field_width and self.matrix[i - 1][j + 1].alive:
                alive_neighbourhoods += 1
        if i + 1 < self.field_height and j - 1 > -1 and self.matrix[i + 1][j - 1].alive:
                alive_neighbourhoods += 1
        if i + 1 < self.field_height and self.matrix[i + 1][j].alive:
                alive_neighbourhoods += 1
        if j + 1 < self.field_width and self.matrix[i][j + 1].alive:
                alive_neighbourhoods += 1
        if alive_neighbourhoods == 3 and not self.matrix[i][j].alive:
            self.matrix[i][j].need_to_update = True
        elif self.matrix[i][j].alive and alive_neighbourhoods > 3:
            self.matrix[i][j].need_to_update = True
        elif self.matrix[i][j].alive and alive_neighbourhoods < 2:
            self.matrix[i][j].need_to_update = True
            return

    # function that cleans the playing field
    def clear(self):
        for i in range(self.field_height):
            for j in range(self.field_width):
                self.canvas.itemconfig(self.matrix[i][j].print, fill="white")
                self.matrix[i][j].alive = False

    # function that redraws the playing field
    def update_field(self):
        for i in range(self.field_height):
            for j in range(self.field_width):
                if self.matrix[i][j].need_to_update:
                    self.matrix[i][j].need_to_update = False
                    if self.matrix[i][j].alive:
                        self.matrix[i][j].alive = False
                        self.canvas.itemconfig(self.matrix[i][j].print, fill="white")
                    else:
                        self.matrix[i][j].alive = True
                        self.canvas.itemconfig(self.matrix[i][j].print, fill="yellow")

    # function that updates and redraws the playing field
    def step(self):
        for i in range(self.field_height):
            for j in range(self.field_width):
                self.update_cell(i, j)
        self.update_field()

    # set the mouse actions
    def mouse_bind(self, mouse):
        i = (mouse.y - 3) // self.cell_size
        j = (mouse.x - 3) // self.cell_size
        if i >= self.field_height or j >= self.field_width:
            return
        self.canvas.itemconfig(self.matrix[i][j].print, fill="yellow")
        self.matrix[i][j].alive = True

    # enables constant updating the game field
    def start(self):
        self.start_key = True
        self.field_revival()

    # constant updating the game field
    def field_revival(self):
        self.step()
        if self.start_key:
            self.root.after(self.UPDATE_SPEED , lambda: self.field_revival())

    # disables constant updating the game field
    def stop(self):
        self.start_key = False

