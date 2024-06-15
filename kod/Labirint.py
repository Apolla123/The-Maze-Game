from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from random import choice


# Класс "Cell" представляет каждую ячейку лабиринта.
class Cell:
    def __init__(self, x, y, thickness):
        # Они содержат информацию:
        # о её положении(x, y)
        self.x, self.y = x, y
        # толщина стен
        self.thickness = thickness
        # стенах(верхняя, нижняя, левая и правая)
        self.walls = {'up': True, 'right': True, 'down': True, 'left': True}
        # состоянии(посещена или нет)
        self.visited = False

    # рисует ячейку на painter
    def draw(self, painter, tile):
        # Вычисляет координаты и толщину ячейки в пикселях.
        x, y = self.x * tile, self.y * tile
        # устанавливает цвет
        pen = QPen(Qt.green, self.thickness)
        painter.setPen(pen)
        # Затем, в зависимости от наличия стены в каждом направлении, рисует линии.
        if self.walls['up']:
            painter.drawLine(x, y, x + tile, y)
        if self.walls['right']:
            painter.drawLine(x + tile, y, x + tile, y + tile)
        if self.walls['down']:
            painter.drawLine(x + tile, y + tile, x, y + tile)
        if self.walls['left']:
            painter.drawLine(x, y + tile, x, y)

    # проверяет, является ли ячейка с координатами (x, y) допустимой ячейкой.
    def check_cell(self, x, y, cols, rows, grid_cells):
        find_index = lambda x, y: x + y * cols
        # Если координаты выходят за пределы границ лабиринта, возвращает False.
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    # проверяет соседние ячейки.
    def check_neighbors(self, cols, rows, grid_cells):
        neighbors = []
        # проверяет ячейки в четырех направлениях
        top = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        right = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        left = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)
        # Ищет соседние ячейки, которые еще не были посещены, и добавляет их в список соседей.
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        # Возвращает случайно выбранную непосещенную соседнюю ячейку или False, если таких ячеек нет.
        return choice(neighbors) if neighbors else False


# Рисуем лабиринт
class MazeWidget(QWidget):
    def __init__(self, cols, rows, tile_size):
        super().__init__()
        # количество столбцов
        self.cols = cols
        # количество строк
        self.rows = rows
        self.tile_size = tile_size
        # размер ячейки
        self.thickness = 4
        # Создаём список, содержащий объекты класса Cell для каждой ячейки лабиринта.
        self.grid_cells = [Cell(col, row, self.thickness) for row in range(self.rows) for col in range(self.cols)]
        # Вызываем метод generate_maze().
        self.generate_maze()

    # генерация лабиринта с использованием рекурсивного алгоритма обратного отслеживания
    # Recursive Backtracking
    def generate_maze(self):
        # Выбираем в качестве текущей ячейки первую ячейку.
        current_cell = self.grid_cells[0]
        # создается пустой список для хранения посещенных ячеек
        array = []
        # для отслеживания количества разрушенных стен
        break_count = 1
        # Затем, пока не все ячейки посещены
        while break_count != len(self.grid_cells):
            # отмечает текущую ячейку как посещенную
            current_cell.visited = True
            # проверяет соседние ячейки
            next_cell = current_cell.check_neighbors(self.cols, self.rows, self.grid_cells)
            # выбирает следующую ячейку для перемещения.
            if next_cell:
                # помечается как посещенная
                next_cell.visited = True
                break_count += 1
                # добавляется в список array
                array.append(current_cell)
                # удаляются стены между текущей и следующей ячейками
                self.remove_walls(current_cell, next_cell)
                # текущая ячейка обновляется на следующую ячейку.
                current_cell = next_cell
            # Если не найдена ни одна допустимая соседняя ячейка,
            # а в array есть ячейки, выполняется обратный поиск путем установки
            # current_cell в самую последнюю добавленную ячейку массива.
            elif array:
                current_cell = array.pop()

    # удаляет стены между текущей и следующей ячейками на основе их координат.
    def remove_walls(self, current, next):
        dx = current.x - next.x
        # Если смещение по x равно 1
        if dx == 1:
            # удаляет правую стену текущей ячейки
            current.walls['left'] = False
            # и левую стену следующей ячейки
            next.walls['right'] = False
        # Если смещение по x равно -1
        elif dx == -1:
            # удаляет левую стену текущей ячейки
            current.walls['right'] = False
            # и правую стену следующей ячейки.
            next.walls['left'] = False
        dy = current.y - next.y
        # Если смещение по y равно 1
        if dy == 1:
            # удаляет верхнюю стену текущей ячейки
            current.walls['up'] = False
            # и нижнюю стену следующей ячейки
            next.walls['down'] = False
        # Если смещение по y равно -1
        elif dy == -1:
            # даляет нижнюю стену текущей ячейки
            current.walls['down'] = False
            # и верхнюю стену следующей ячейки.
            next.walls['up'] = False

    # рисование ячеек сетки
    def paintEvent(self, event):
        painter = QPainter(self)
        # устанавливается режим сглаживания
        painter.setRenderHint(QPainter.Antialiasing)
        for cell in self.grid_cells:
            cell.draw(painter, self.tile_size)