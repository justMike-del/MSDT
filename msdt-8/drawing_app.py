import tkinter as tk
from tkinter import ttk
import random
import math
from PIL import Image, ImageDraw, ImageTk

class Main:
    def __init__(self):
        # Инициализация главного окна приложения
        self.frame = FramePanel()
        self.frame.mainloop()

class FramePanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drawing Application")
        self.geometry("600x650")
        self.resizable(False, False)

        # Создание панели вкладок и доски для рисования
        self.board = DrawBoard(self)
        self.tabbed_panel = ttk.Notebook(self)

        self.setup_tabs()
        self.setup_layout()

    # настройка вкладок для различных опций рисования
    def setup_tabs(self):
        self.tabbed_panel.add(
            InputLineControlPanel(self.board, self),
            text="Прямая, естественный")
        self.tabbed_panel.add(
            InputLineControlPanel(self.board, self, algorithm='bresenham'),
            text="Прямая, Брезенхама")
        self.tabbed_panel.add(
            InputCurcleControlPanel(self.board, self),
            text="Окружность, естественный")
        self.tabbed_panel.add(
            InputCurcleControlPanel(self.board, self, algorithm='bresenham'),
            text="Окружность, Брезенхама")
        self.tabbed_panel.add(
            InputLissajousControlPanel(self.board, self),
            text="Лиссажу")  # Кривые Лиссажу
        self.tabbed_panel.add(
            FugureFillControlPanel(self.board, self, algorithm='modified'),
            text="Модифицированный с затравкой")
        self.tabbed_panel.add(
            FugureFillControlPanel(self.board, self, algorithm='bark'),
            text="Короеда")

    # размещение панели вкладок и панели рисования в главном окне
    def setup_layout(self):
        self.tabbed_panel.pack(expand=1, fill='both')
        self.board.pack(expand=1, fill='both')

class DrawBoard(tk.Canvas):
    # Инициализация доски для рисования
    def __init__(self, master):
        super().__init__(master, bg="white")
        # Создание изображения, которое сохраняет состояние доски
        self.image = Image.new("RGBA", (550, 430), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.create_image(0, 0, anchor='nw', image=self.image_tk)

    # Обновление отображаемого изображения
    def paint(self):
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.create_image(0, 0, anchor='nw', image=self.image_tk)

    # Рисование точки по указанным координатам
    def draw_point(self, x, y, color="black"):
        self.draw.point((x, y), fill=color)
        self.paint()

    # Очистка доски для рисования
    def clear_board(self):
        self.image = Image.new("RGBA", (550, 430), (255, 255, 255))  # Сброс изображения
        self.paint()

# Панель для ввода параметров отрисовки линий
class InputLineControlPanel(tk.Frame):
    def __init__(self, board, master, algorithm='natural'):
        super().__init__(master)
        self.board = board
        # Создание полей ввода для начальных и конечных точек
        self.start_x = tk.Entry(self, width=3)
        self.start_y = tk.Entry(self, width=3)
        self.end_x = tk.Entry(self, width=3)
        self.end_y = tk.Entry(self, width=3)

        self.create_widgets(algorithm)

    # Создание меток и кнопок для панели управления
    def create_widgets(self, algorithm):
        tk.Label(self, text="Начальная точка:").grid(row=0, column=0)
        tk.Label(self, text="Конечная точка:").grid(row=1, column=0)
        # Размещение полей ввода в сетке
        self.start_x.grid(row=0, column=1)
        self.start_y.grid(row=0, column=2)
        self.end_x.grid(row=1, column=1)
        self.end_y.grid(row=1, column=2)
        draw_button = tk.Button(self, text="Отрисовка", command=self.draw_line)
        draw_button.grid(row=2, column=0, columnspan=2)
        clear_button = tk.Button(self, text="Очистить", command=self.clear_board)
        clear_button.grid(row=2, column=2)
        random_button = tk.Button(self, text="Рандом", command=self.random_points)
        random_button.grid(row=2, column=3)

    # Функция отрисовки линии
    def draw_line(self):
        x0 = int(self.start_x.get())
        y0 = int(self.start_y.get())
        x1 = int(self.end_x.get())
        y1 = int(self.end_y.get())
        Algorithms.natural_line_drawing(self.board, (x0, y0), (x1, y1))
        self.board.paint()

    # Очистка панели рисования
    def clear_board(self):
        self.board.clear_board()

    # Генерация случайных координат и обновление полей ввода
    def random_points(self):
        x0 = random.randint(0, 450)
        y0 = random.randint(0, 450)
        x1 = random.randint(0, 450)
        y1 = random.randint(0, 450)
        self.start_x.delete(0, tk.END)
        self.start_y.delete(0, tk.END)
        self.end_x.delete(0, tk.END)
        self.end_y.delete(0, tk.END)
        self.start_x.insert(0, str(x0))
        self.start_y.insert(0, str(y0))
        self.end_x.insert(0, str(x1))
        self.end_y.insert(0, str(y1))
        self.draw_line()

# Панель для ввода параметров отрисовки окружности
class InputCurcleControlPanel(tk.Frame):
    def __init__(self, board, master, algorithm='natural'):
        super().__init__(master)
        self.board = board

        # Создание полей ввода для центра и радиуса
        self.center_x = tk.Entry(self, width=3)
        self.center_y = tk.Entry(self, width=3)
        self.radius_value = tk.Entry(self, width=3)
        self.create_widgets(algorithm)

    # Создание меток и кнопок для панели управления
    def create_widgets(self, algorithm):
        tk.Label(self, text="Центр:").grid(row=0, column=0)
        tk.Label(self, text="Радиус:").grid(row=1, column=0)
        self.center_x.grid(row=0, column=1)
        self.center_y.grid(row=0, column=2)
        self.radius_value.grid(row=1, column=1)
        draw_button = tk.Button(self, text="Отрисовка", command=self.draw_circle)
        draw_button.grid(row=2, column=0, columnspan=2)
        clear_button = tk.Button(self, text="Очистить", command=self.clear_board)
        clear_button.grid(row=2, column=2)
        random_button = tk.Button(self, text="Рандом", command=self.random_circle)
        random_button.grid(row=2, column=3)

    # Функция отрисовки окружности
    def draw_circle(self):
        # Получение параметров из полей ввода
        x0 = int(self.center_x.get())
        y0 = int(self.center_y.get())
        r = int(self.radius_value.get())
        Algorithms.natural_circle_drawing(self.board, (x0, y0), r)
        self.board.paint()

    # Очистка панели рисования
    def clear_board(self):
        self.board.clear_board()

    # Генерация окружности со случайными параметрами
    def random_circle(self):
        x0 = random.randint(150, 350)  # x-координата центра
        y0 = random.randint(150, 350)  # y-координата центра
        r = random.randint(10, 200)  # радиус
        self.center_x.delete(0, tk.END)
        self.center_y.delete(0, tk.END)
        self.radius_value.delete(0, tk.END)
        self.center_x.insert(0, str(x0))
        self.center_y.insert(0, str(y0))
        self.radius_value.insert(0, str(r))
        self.draw_circle()

# Панель для ввода параметров отрисовки кривых Лиссажу
class InputLissajousControlPanel(tk.Frame):
    def __init__(self, board, master):
        super().__init__(master)
        self.board = board
        self.center_x = tk.Entry(self, width=3)
        self.center_y = tk.Entry(self, width=3)
        self.radius_x = tk.Entry(self, width=3)
        self.radius_y = tk.Entry(self, width=3)
        self.freq_x = tk.Entry(self, width=3)  # частота по х
        self.freq_y = tk.Entry(self, width=3)  # частота по y

        self.create_widgets()

    # Создание меток и кнопок для панели управления
    def create_widgets(self):
        tk.Label(self, text="Центр:").grid(row=0, column=0)
        tk.Label(self, text="Радиусы:").grid(row=1, column=0)
        tk.Label(self, text="Частоты:").grid(row=2, column=0)
        self.center_x.grid(row=0, column=1)
        self.center_y.grid(row=0, column=2)
        self.radius_x.grid(row=1, column=1)
        self.radius_y.grid(row=1, column=2)
        self.freq_x.grid(row=2, column=1)
        self.freq_y.grid(row=2, column=2)
        draw_button = tk.Button(self, text="Отрисовка", command=self.draw_lissajous)
        draw_button.grid(row=3, column=0, columnspan=2)
        clear_button = tk.Button(self, text="Очистить", command=self.clear_board)
        clear_button.grid(row=3, column=2)
        random_button = tk.Button(self, text="Рандом", command=self.random_lissajous)
        random_button.grid(row=3, column=3)

    # Отрисовка кривой Лиссажу
    def draw_lissajous(self):
        x0 = int(self.center_x.get())
        y0 = int(self.center_y.get())
        r_x = int(self.radius_x.get())
        r_y = int(self.radius_y.get())
        o_x = int(self.freq_x.get())
        o_y = int(self.freq_y.get())
        Algorithms.parameter_lissajous_drawing(self.board, (x0, y0),
                                               r_x, r_y, o_x, o_y)
        self.board.paint()

    # Очистка панели рисования
    def clear_board(self):
        self.board.clear_board()

    # Генерация кривой Лиссажу по случайным параметрам
    def random_lissajous(self):
        x0 = random.randint(100, 300)
        y0 = random.randint(100, 300)
        r_x = random.randint(50, 150)
        r_y = random.randint(50, 150)
        o_x = random.randint(1, 20)
        o_y = random.randint(1, 20)
        self.center_x.delete(0, tk.END)
        self.center_y.delete(0, tk.END)
        self.radius_x.delete(0, tk.END)
        self.radius_y.delete(0, tk.END)
        self.freq_x.delete(0, tk.END)
        self.freq_y.delete(0, tk.END)
        self.center_x.insert(0, str(x0))
        self.center_y.insert(0, str(y0))
        self.radius_x.insert(0, str(r_x))
        self.radius_y.insert(0, str(r_y))
        self.freq_x.insert(0, str(o_x))
        self.freq_y.insert(0, str(o_y))
        self.draw_lissajous()

# Панель для ввода параметров закраски фигур
class FugureFillControlPanel(tk.Frame):
    def __init__(self, board, master, algorithm='modified'):
        super().__init__(master)
        self.board = board

        # координаты точки начала закраски
        self.start_x = tk.Entry(self, width=3)
        self.start_y = tk.Entry(self, width=3)

        self.create_widgets()

    # Создание меток и кнопок для панели управления
    def create_widgets(self):
        tk.Label(self, text="Начальная точка:").grid(row=0, column=0)
        self.start_x.grid(row=0, column=1)
        self.start_y.grid(row=0, column=2)
        draw_button = tk.Button(self, text="Отрисовка", command=self.fill)
        draw_button.grid(row=1, column=0, columnspan=2)
        clear_button = tk.Button(self, text="Очистить", command=self.clear_board)
        clear_button.grid(row=1, column=2)

    # Закраска фигур модицицированным рекурсивным алгоритмом
    def fill(self):
        x0 = int(self.start_x.get())
        y0 = int(self.start_y.get())
        Algorithms.modified_recurant_fill(self.board, x0, y0)
        self.board.paint()

    # Очистка панели рисования
    def clear_board(self):
        self.board.clear_board()

class Algorithms:
    @staticmethod
    def natural_line_drawing(board, p0, p1):
        # Рисование линии с использованием естественного алгоритма
        x0, y0 = p0
        x1, y1 = p1
        if x0 == x1:  # Вертикальная линия
            for y in range(min(y0, y1), max(y0, y1) + 1):
                board.draw_point(x0, y)
        else:
            a = (y1 - y0) / (x1 - x0)  # угловой коэффициент
            b = y0 - a * x0  # свободный член
            if abs(a) <= 1:  # Использование итерации по x
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    y = int(round(a * x + b))
                    board.draw_point(x, y)
            else:  # Использование итерации по y
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    x = int(round((y - b) / a))
                    board.draw_point(x, y)

    @staticmethod
    def natural_circle_drawing(board, center, radius):
        # Рисование окружности с использованием естественного алгоритма
        x_c, y_c = center
        for x in range(-radius, radius + 1):
            y = int((radius**2 - x**2)**0.5)
            board.draw_point(x_c + x, y_c + y)  # Верхняя половина
            board.draw_point(x_c + x, y_c - y)  # Нижняя половина

    @staticmethod
    def parameter_lissajous_drawing(board, center, r_x, r_y, freq_x, freq_y):
        # Рисование кривой Лиссажу
        x_c, y_c = center
        for t in range(0, 360):
            x = int(r_x * math.sin(freq_x * t * (math.pi / 180)))
            y = int(r_y * math.sin(freq_y * t * (math.pi / 180)))
            board.draw_point(x_c + x, y_c + y)

    @staticmethod
    def modified_recurant_fill(board, x0, y0):
        # Заливка области с использованием модифицированного рекурсивного алгоритма
        stack = [(x0, y0)]  # Добавляем в стек "затравку"
        while stack:
            x, y = stack.pop()
            if 0 <= x < 550 and 0 <= y < 430:  # Проверка границ
                board.draw_point(x, y)
                # Добавление соседних точек в стек
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))

if __name__ == "__main__":
    Main()