import unittest
from maze import Maze, Cell

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win=None)  # Передаем None для окна
        self.assertEqual(len(m1._cells), num_rows)
        self.assertEqual(len(m1._cells[0]), num_cols)

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win=None)  # Передаем None для окна
        
        # До вызова метода _break_entrance_and_exit:
        entrance_cell = m1._cells[0][0]
        exit_cell = m1._cells[num_rows - 1][num_cols - 1]
        
        self.assertTrue(entrance_cell.has_left_wall)
        self.assertTrue(entrance_cell.has_top_wall)
        self.assertTrue(exit_cell.has_right_wall)
        self.assertTrue(exit_cell.has_bottom_wall)
        
        m1._break_entrance_and_exit()

        # После вызова метода _break_entrance_and_exit:
        entrance_cell = m1._cells[0][0]
        exit_cell = m1._cells[num_rows - 1][num_cols - 1]
        
        self.assertFalse(entrance_cell.has_left_wall)
        self.assertFalse(entrance_cell.has_top_wall)
        self.assertFalse(exit_cell.has_right_wall)
        self.assertFalse(exit_cell.has_bottom_wall)

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win=None)  # Передаем None для окна
        
        # Делаем несколько обходов, чтобы пометить ячейки как посещенные
        m1._break_walls_r(0, 0)
        m1._break_walls_r(1, 0)
        m1._break_walls_r(2, 0)

        # Проверяем, что visited для некоторых ячеек стало True
        self.assertTrue(m1._cells[0][0].visited)
        self.assertTrue(m1._cells[1][0].visited)
        self.assertTrue(m1._cells[2][0].visited)

        # Сбрасываем visited
        m1._reset_cells_visited()

        # Проверяем, что все visited стали False
        self.assertFalse(m1._cells[0][0].visited)
        self.assertFalse(m1._cells[1][0].visited)
        self.assertFalse(m1._cells[2][0].visited)
        for row in m1._cells:
            for cell in row:
                self.assertFalse(cell.visited)  # Проверка, что все ячейки сброшены

if __name__ == "__main__":
    unittest.main()
