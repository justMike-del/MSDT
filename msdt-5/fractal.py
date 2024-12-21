import tkinter as tk
import math

# Ширина и высота окна приложения
BOARD_WIDTH = 650
BOARD_HEIGHT = 600

# Класс содержит информацию о фрактале на определённом шаге
class GFractal:
    def __init__(self, gen=0):
        self.axiom = "F+F+F"  # начальное состояние
        self.rule = "F-F+F"
        self.angle = 2 * math.pi / 3 # угол поворота
        self.gen = gen  # шаг фрактала
        self.fractal = self.axiom

        for _ in range(gen):
            self.gen_up()

    def gen_up(self):
        self.fractal = self.fractal.replace("F", self.rule)
        self.gen += 1

    def gen_down(self):
        if self.gen > 0:
            self.fractal = self.fractal.replace(self.rule, "F")
            self.gen -= 1


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

# Панель для отрисовки фрактала
class DrawBoard(tk.Canvas):
    def __init__(self, master=None):
        super().__init__(master, bg="white")
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def draw_lines(self):
        self.delete("all")
        for line in self.lines:
            # Линии рисуются относительно центра экрана
            self.create_line(BOARD_WIDTH/2 + line.x1,
                             BOARD_HEIGHT/2 + line.y1,
                             BOARD_WIDTH/2 + line.x2,
                             BOARD_HEIGHT/2 + line.y2,
                             fill="black")

# Состояние "черепашки"
class State:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

# Отрисовка фрактала на панели
def draw_fractal(board, fractal):
    fract1 = [0, 0, 0, 0]  # [left, bottom, right, top]
    state = State(0, 0, 0)
    turtle_memory = [] # стек - память "черепашки"
    for step in fractal.fractal:
        new_state = choose_step(turtle_memory, state, step)
        if step == 'F':
            update_bounds(fract1, new_state.x, new_state.y)
            board.add_line(Line(state.x, state.y, new_state.x, new_state.y))
        state = new_state

    board.draw_lines()

# Изменение состояния в зависимости от входного шага
def choose_step(turtle_memory: list, state, step):
    x = state.x
    y = state.y
    angle = state.angle
    delta = 2 * math.pi / 3
    length = 10
    if step == 'F':
        x += round(length * math.cos(angle))
        y -= round(length * math.sin(angle))
    elif step == 'f':
        x += round(length * math.cos(angle))
        y -= round(length * math.sin(angle))
    elif step == '+':
        angle += delta
    elif step == '-':
        angle -= delta
    elif step == '[':
        turtle_memory.append(State(x, y, angle))
    elif step == ']':
        new_state = turtle_memory.pop()
        x = new_state.x
        y = new_state.y
        angle = new_state.angle
    return State(x, y, angle)

# Обновляет текущие границы фрактала
def update_bounds(bounds, x, y):
    if x < bounds[0]:
        bounds[0] = x
    if y < bounds[1]:
        bounds[1] = y
    if x > bounds[2]:
        bounds[2] = x
    if y > bounds[3]:
        bounds[3] = y


class FractalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Геометрические фракталы")
        self.geometry(str(BOARD_WIDTH)+"x"+str(BOARD_HEIGHT))

        self.board = DrawBoard(self)
        self.board.pack(fill=tk.BOTH, expand=True)

        self.axiom_label = tk.Label(self, text="Аксиома: F+F+F")
        self.axiom_label.pack()

        self.gen_spinbox = tk.Spinbox(self, from_=0, to=10)  # Ввод шага больше 10 сильно перегружает программу
        self.gen_spinbox.pack()

        self.draw_button = tk.Button(self, text="Отрисовка", command=self.draw_fractal)
        self.draw_button.pack()

    def draw_fractal(self):
        gen = int(self.gen_spinbox.get())
        fractal = GFractal(gen)
        draw_fractal(self.board, fractal)


if __name__ == "__main__":
    app = FractalApp()
    app.mainloop()
