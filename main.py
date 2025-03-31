import time
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        # Создаем корневое окно
        self.__root = Tk()
        
        # Устанавливаем заголовок окна
        self.__root.title("Drawing Window")
        
        # Создаем холст для рисования
        self.__canvas = Canvas(self.__root, width=width, height=height)
        
        # Упаковываем холст
        self.__canvas.pack(fill=BOTH, expand=True)
        
        # Изначально окно не работает
        self.__running = False
        
        # Добавляем обработчик закрытия окна
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    # Метод для получения доступа к холсту
    def get_canvas(self):
        return self.__canvas

    # Метод перерисовки
    def redraw(self):
        # Перерисовываем окно
        self.__root.update_idletasks()
        self.__root.update()

    # Метод ожидания закрытия окна
    def wait_for_close(self):
        # Устанавливаем окно как работающее
        self.__running = True
        
        # Повторно перерисовываем окно, пока оно работает
        while self.__running:
            self.redraw()

    # Метод закрытия окна
    def close(self):
        # Устанавливаем состояние окна как завершенное
        self.__running = False
        self.redraw()  # Перерисовываем один последний раз перед закрытием
        self.__root.quit()  # Закрываем приложение


class Cell:
    def __init__(self, x1, y1, x2, y2, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        # Координаты ячейки
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        # Стены ячейки
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall

    def draw(self, canvas):
        # Рисуем стены ячейки на холсте
        if self.has_left_wall:
            canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="black", width=2)
        if self.has_right_wall:
            canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="black", width=2)
        if self.has_top_wall:
            canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="black", width=2)
        if self.has_bottom_wall:
            canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="black", width=2)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        # Параметры лабиринта
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

        # Список для хранения ячеек лабиринта
        self._cells = []
        
        # Создаем ячейки
        self._create_cells()

    def _create_cells(self):
        # Заполняем список ячейками
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                x1 = self.x1 + j * self.cell_size_x
                y1 = self.y1 + i * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y
                cell = Cell(x1, y1, x2, y2)  # Ячейка с полными стенами по умолчанию
                row.append(cell)
                # Нарисовать ячейку
                self._draw_cell(i, j, cell)
            self._cells.append(row)

    def _draw_cell(self, i, j, cell):
        # Рисуем ячейку на холсте
        cell.draw(self.win.get_canvas())
        # Анимация обновления
        self._animate()

    def _animate(self):
        # Анимация — обновляем окно и делаем задержку
        self.win.redraw()
        time.sleep(0.05)


# Основная функция
def main():
    win = Window(800, 600)  # Создаем окно размером 800x600
    # Создаем лабиринт
    maze = Maze(x1=50, y1=50, num_rows=10, num_cols=10, cell_size_x=40, cell_size_y=40, win=win)

    win.wait_for_close()  # Ожидаем закрытия окна


if __name__ == "__main__":
    main()
