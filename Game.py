from tkinter import *
from copy import deepcopy

class GameOfLife(object):
    def __init__(self, window_height=480, window_width=640, cell_size=15):
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
        # создаём кнопки
        self.button_step = Button(self.frame, text='Step', command=self.step)
        self.button_clear = Button(self.frame, text='Clear', command=self.clear)
        self.button_step_x5 = Button(self.frame, text='Step x5', command=self.step_x5)
        self.button_start = Button(self.frame, text='Start', command=self.start)
        self.button_stop = Button(self.frame, text='Stop', command=self.stop)
        # пакуем кнопки
        self.button_step_x5.pack(side='left')
        self.button_start.pack(side='left')
        self.button_clear.pack(side='left')
        self.button_step.pack(side='right')
        self.button_stop.pack(side='left')
        # биндим действия мышкой
        self.canvas.bind('<B1-Motion>', self.mouse_bind)
        self.canvas.bind('<ButtonPress>', self.mouse_bind)
        # создаём массив
        self.matrix = []
        temp_list = []
        for i in range(self.field_height):
            for j in range(self.field_width):
                temp_cell = self.cell(self.canvas, self.cell_size, i, j)
                temp_list.append(temp_cell)
            self.matrix.append(deepcopy(temp_list))
            temp_list.clear()
        self.start_key = True

    def run(self):
        self.root.mainloop()

    class cell(object):
        def __init__(self, canvas, cell_size, row, column):
            self.row = row
            self.column = column
            self.alive = False
            self.status = False
            self.print = canvas.create_rectangle(2 + cell_size * column, 2 + cell_size * row, cell_size + cell_size *
                                            column - 2, cell_size + cell_size * row - 2, fill="white")

    def update_cell(self, i, j):
        count = 0
        if i - 1 != -1 and j - 1 != -1 and self.matrix[i - 1][j - 1].alive:
                count += 1
        if j - 1 != -1 and self.matrix[i][j - 1].alive:
                count += 1
        if i - 1 != -1 and self.matrix[i - 1][j].alive:
                count += 1
        if i + 1 != self.field_height and j + 1 != self.field_width and self.matrix[i + 1][j + 1].alive:
                count += 1
        if i - 1 != -1 and j + 1 != self.field_width and self.matrix[i - 1][j + 1].alive:
                count += 1
        if i + 1 != self.field_height and j - 1 != -1 and self.matrix[i + 1][j - 1].alive:
                count += 1
        if i + 1 != self.field_height and self.matrix[i + 1][j].alive:
                count += 1
        if j + 1 != self.field_width and self.matrix[i][j + 1].alive:
                count += 1
        if count == 3 and not self.matrix[i][j].alive:
            self.matrix[i][j].status = True
            return
        if self.matrix[i][j].alive and count > 3:
            self.matrix[i][j].status = True
            return
        if self.matrix[i][j].alive and count < 2:
            self.matrix[i][j].status = True
            return

    def clear(self):
        for i in range(self.field_height):
            for j in range(self.field_width):
                self.canvas.itemconfig(self.matrix[i][j].print, fill="white")
                self.matrix[i][j].alive = False

    def update_field(self):
        for i in range(self.field_height):
            for j in range(self.field_width):
                if self.matrix[i][j].status:
                    self.matrix[i][j].status = False
                    if self.matrix[i][j].alive:
                        self.matrix[i][j].alive = False
                        self.canvas.itemconfig(self.matrix[i][j].print, fill="white")
                    else:
                        self.matrix[i][j].alive = True
                        self.canvas.itemconfig(self.matrix[i][j].print, fill="yellow")

    def step(self):
        for i in range(self.field_height):
            for j in range(self.field_width):
                self.update_cell(i, j)
        self.update_field()

    def step_x5(self):
        for i in range(5):
            self.step()

    def mouse_bind(self, mouse):
        i = (mouse.y - 3) // self.cell_size
        j = (mouse.x - 3) // self.cell_size
        if i >= self.field_height or j >= self.field_width:
            return
        self.canvas.itemconfig(self.matrix[i][j].print, fill="yellow")
        self.matrix[i][j].alive = True

    def start(self):
        pass

    def stop(self):
        pass
