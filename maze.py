import random
import time
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Drawing Window")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def get_canvas(self):
        return self.__canvas

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False
        self.redraw()
        self.__root.quit()


class Cell:
    def __init__(self, x1, y1, x2, y2, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True, win=None):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.visited = False  # Добавляем флаг для отслеживания посещенности
        self.win = win

    def draw(self, canvas):
        if canvas is None:
            return  # Если canvas равен None, не рисуем ничего

        # Рисуем стены ячейки на холсте или рисуем с фоновым цветом, если стен нет
        if self.has_left_wall:
            canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="black", width=2)
        else:
            canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="#d9d9d9", width=2)

        if self.has_right_wall:
            canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="black", width=2)
        else:
            canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="#d9d9d9", width=2)

        if self.has_top_wall:
            canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="black", width=2)
        else:
            canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="#d9d9d9", width=2)

        if self.has_bottom_wall:
            canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="black", width=2)
        else:
            canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="#d9d9d9", width=2)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        self._cells = []
        self._create_cells()

    def _create_cells(self):
        # Инициализируем список ячеек (каждая строка — это отдельный список для ячеек)
        self._cells = [[] for _ in range(self.num_rows)]

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                # Корректно вычисляем координаты для ячеек
                x1 = self.x1 + j * self.cell_size_x
                y1 = self.y1 + i * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y

                # Создаем объект Cell с вычисленными координатами
                cell = Cell(x1, y1, x2, y2, win=self.win)
                
                # Добавляем ячейку в соответствующий список
                self._cells[i].append(cell)

                # Вызываем метод для рисования ячейки
                self._draw_cell(i, j, cell)
                self._animate()  # Анимация

    def _draw_cell(self, i, j, cell):
        # Рассчитываем положение x/y на основе индексов и размеров
        x1 = self.x1 + j * self.cell_size_x
        y1 = self.y1 + i * self.cell_size_y
        x2 = x1 + self.cell_size_x
        y2 = y1 + self.cell_size_y

        # Создаем ячейку
        cell._x1 = x1
        cell._y1 = y1
        cell._x2 = x2
        cell._y2 = y2

        # Рисуем ячейку
        cell.draw(self.win.get_canvas() if self.win else None)
        
        # Анимация (если требуется)
        self._animate()

    def _animate(self):
        if self.win:
            self.win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        # Вход в лабиринт - первая ячейка (верхняя левая)
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False  # Убираем верхнюю стену
        entrance_cell.has_left_wall = False  # Убираем левую стену
        self._draw_cell(0, 0, entrance_cell)

        # Выход из лабиринта - последняя ячейка (нижняя правая)
        exit_cell = self._cells[self.num_rows - 1][self.num_cols - 1]
        exit_cell.has_bottom_wall = False  # Убираем нижнюю стену
        exit_cell.has_right_wall = False  # Убираем правую стену
        self._draw_cell(self.num_rows - 1, self.num_cols - 1, exit_cell)

    def _break_walls_r(self, i, j):
        # Помечаем текущую ячейку как посещенную
        self._cells[i][j].visited = True
        
        # Получаем возможные направления для обхода (север, юг, восток, запад)
        directions = []
        if i > 0 and not self._cells[i-1][j].visited:  # Север
            directions.append('north')
        if i < self.num_rows - 1 and not self._cells[i+1][j].visited:  # Юг
            directions.append('south')
        if j > 0 and not self._cells[i][j-1].visited:  # Запад
            directions.append('west')
        if j < self.num_cols - 1 and not self._cells[i][j+1].visited:  # Восток
            directions.append('east')
        
        # Если нет направлений, выходим
        if not directions:
            self._draw_cell(i, j, self._cells[i][j])  # Нарисовать текущую ячейку
            return

        # Иначе выбираем случайное направление
        direction = random.choice(directions)

        # Ломаем стены в выбранном направлении
        if direction == 'north':
            self._cells[i][j].has_top_wall = False
            self._cells[i-1][j].has_bottom_wall = False
            self._break_walls_r(i-1, j)
        elif direction == 'south':
            self._cells[i][j].has_bottom_wall = False
            self._cells[i+1][j].has_top_wall = False
            self._break_walls_r(i+1, j)
        elif direction == 'west':
            self._cells[i][j].has_left_wall = False
            self._cells[i][j-1].has_right_wall = False
            self._break_walls_r(i, j-1)
        elif direction == 'east':
            self._cells[i][j].has_right_wall = False
            self._cells[i][j+1].has_left_wall = False
            self._break_walls_r(i, j+1)
        
        # Рисуем текущую ячейку
        self._draw_cell(i, j, self._cells[i][j])

    def _reset_cells_visited(self):
        # Проходим по всем ячейкам лабиринта и сбрасываем visited в False
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def solve(self):
        # Начинаем решение с первой ячейки (вход)
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        # Помечаем текущую ячейку как посещенную
        self._cells[i][j].visited = True

        # Анимация
        self._animate()

        # Если мы достигли конца (выход)
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True
        
        # Для каждого направления (вверх, вниз, влево, вправо)
        directions = []
        if i > 0 and not self._cells[i-1][j].visited and not self._cells[i][j].has_top_wall:
            directions.append('north')
        if i < self.num_rows - 1 and not self._cells[i+1][j].visited and not self._cells[i][j].has_bottom_wall:
            directions.append('south')
        if j > 0 and not self._cells[i][j-1].visited and not self._cells[i][j].has_left_wall:
            directions.append('west')
        if j < self.num_cols - 1 and not self._cells[i][j+1].visited and not self._cells[i][j].has_right_wall:
            directions.append('east')

        # Если направление ведет к решению, рекурсивно идем дальше
        for direction in directions:
            if direction == 'north' and self._solve_r(i-1, j):
                return True
            elif direction == 'south' and self._solve_r(i+1, j):
                return True
            elif direction == 'west' and self._solve_r(i, j-1):
                return True
            elif direction == 'east' and self._solve_r(i, j+1):
                return True

        # Если ни одно направление не сработало, возвращаем False
        return False
