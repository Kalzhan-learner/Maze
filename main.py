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

class Point:
    def __init__(self, x, y):
        self.x = x  # Координата x
        self.y = y  # Координата y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1  # Первая точка
        self.point2 = point2  # Вторая точка

    def draw(self, canvas, fill_color):
        # Метод рисования линии на холсте
        canvas.create_line(
            self.point1.x, self.point1.y, 
            self.point2.x, self.point2.y, 
            fill=fill_color, width=2
        )

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

    def draw_move(self, to_cell, canvas, undo=False):
        # Вычисляем центры текущей ячейки и целевой ячейки
        center_x1 = (self._x1 + self._x2) / 2
        center_y1 = (self._y1 + self._y2) / 2
        center_x2 = (to_cell._x1 + to_cell._x2) / 2
        center_y2 = (to_cell._y1 + to_cell._y2) / 2
        
        # Если undo не задано, линия будет красной
        line_color = "red" if not undo else "gray"
        
        # Рисуем линию от центра текущей ячейки к центру целевой ячейки
        line = Line(Point(center_x1, center_y1), Point(center_x2, center_y2))
        line.draw(canvas, line_color)

# Основная функция
def main():
    win = Window(800, 600)  # Создаем окно размером 800x600
    # Получаем холст через новый метод get_canvas()
    canvas = win.get_canvas()

    # Создаем несколько ячеек с разными стенками
    cell1 = Cell(50, 50, 150, 150)  # Ячейка с полными стенами
    cell2 = Cell(150, 50, 250, 150, has_left_wall=False)  # Ячейка без левой стены
    cell3 = Cell(50, 150, 150, 250, has_top_wall=False)  # Ячейка без верхней стены
    cell4 = Cell(150, 150, 250, 250, has_bottom_wall=False)  # Ячейка без нижней стены

    # Рисуем ячейки на холсте
    cell1.draw(canvas)
    cell2.draw(canvas)
    cell3.draw(canvas)
    cell4.draw(canvas)

    # Прорисовываем путь между ячейками
    cell1.draw_move(cell2, canvas)  # Путь от cell1 до cell2 (красная линия)
    cell2.draw_move(cell3, canvas)  # Путь от cell2 до cell3 (красная линия)
    cell3.draw_move(cell4, canvas, undo=True)  # Путь от cell3 до cell4 (серый, для undo)

    win.wait_for_close()  # Ожидаем закрытия окна

if __name__ == "__main__":
    main()
