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

    def draw_line(self, line, fill_color):
        # Вызываем метод draw() объекта Line для рисования линии
        line.draw(self.__canvas, fill_color)

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

# Основная функция
def main():
    win = Window(800, 600)  # Создаем окно размером 800x600
    # Создаем несколько точек
    p1 = Point(100, 100)
    p2 = Point(200, 200)
    p3 = Point(300, 100)
    p4 = Point(400, 200)

    # Создаем несколько линий
    line1 = Line(p1, p2)
    line2 = Line(p2, p3)
    line3 = Line(p3, p4)

    # Рисуем линии с различными цветами
    win.draw_line(line1, "black")
    win.draw_line(line2, "red")
    win.draw_line(line3, "blue")
    win.wait_for_close()  # Ожидаем закрытия окна

if __name__ == "__main__":
    main()
