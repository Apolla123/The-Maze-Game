from PyQt5.QtWidgets import QLabel, QMainWindow, QMessageBox, QPushButton
from PyQt5.QtCore import Qt, QTimer
from kod import Labirint
import sqlite3


class StartWindow(QMainWindow):
    def __init__(self, login):
        super().__init__()
        self.login = str(login)
        self.step_size, self.player_size = 30, 10
        self.cols, self.rows = 20, 20
        self.step = self.step_size

        self.initUI()

    # Настройка интерфейся
    def initUI(self):

        # Создаём лабиринт
        self.maze_widget = Labirint.MazeWidget(self.cols, self.rows, self.step_size)
        # устанавливает в качестве центрального виджета главного окна
        self.setCentralWidget(self.maze_widget)
        self.setWindowTitle("Maze Visualization")
        self.setGeometry(100, 100, self.cols * self.step_size, self.rows * self.step_size)

        # Создаём игрока
        self.player = QLabel(self)
        self.player.setGeometry(5, 5, self.step_size - 10, self.step_size - 10)
        self.player.setStyleSheet("background-color: blue; border-radius: 25px;")

        # Создаём кнопку для окончания игры
        self.button = QLabel(self)
        self.button.setGeometry((self.cols - 1) * self.step_size + 2, (self.rows - 1) * self.step_size + 2,
                                self.step_size - 5, self.step_size - 5)
        self.button.setStyleSheet("background-color: red;")

        # Создаём кнопку рестарта
        self.button_restart = QPushButton('Рестарт', self)
        self.button_restart.clicked.connect(self.restart)
        self.button_restart.hide()

        # Создаём таймер
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.setWindowTitle(f"Start - Time: 0 seconds")
        self.timer.timeout.connect(self.update_timer)
        self.time = 0

    def restart(self):
        self.button_restart.hide()
        self.step = self.step_size
        self.time = 0
        self.timer.start()
        self.player.move(5, 5)

    # Чтобы найти ячейку, на которой находится игрок
    def find_cell(self, x, y):
        cell_x = x // self.step_size
        cell_y = y // self.step_size
        return self.maze_widget.grid_cells[cell_y * self.cols + cell_x]

    def keyPressEvent(self, event):
        x_player = self.player.x()
        y_player = self.player.y()

        key_actions = {Qt.Key_W: (0, -self.step), Qt.Key_S: (0, self.step), Qt.Key_A: (-self.step, 0), Qt.Key_D: (self.step, 0)}

        if event.key() in key_actions:
            dx, dy = key_actions[event.key()]
            x_player += dx
            y_player += dy

        # ячейка на которой находится игрок
        player_cell = self.find_cell(self.player.x(), self.player.y())

        # проверяем куда хочет пойти игрок и есть ли там стена
        if event.key() == Qt.Key_W and not player_cell.walls['up']:
            self.player.move(x_player, y_player)

        if event.key() == Qt.Key_S and not player_cell.walls['down']:
            self.player.move(x_player, y_player)

        if event.key() == Qt.Key_A and not player_cell.walls['left']:
            self.player.move(x_player, y_player)

        if event.key() == Qt.Key_D and not player_cell.walls['right']:
            self.player.move(x_player, y_player)

        # Проверяем, если игрок дотронулся до красного квадрата
        if self.player.geometry().intersects(self.button.geometry()) and self.step != 0:
            QMessageBox.information(self, "Game Over", f"Time: {self.time} seconds")
            self.button_restart.show()
            self.timer.stop()
            self.step = 0

            # Подключение к базе данных
            conn = sqlite3.connect('sqlitebase/MyGame_base.sqlite')
            cursor = conn.cursor()

            cursor.execute("SELECT Time FROM Players WHERE Login = ?", (self.login,))
            current_time = cursor.fetchone()

            # текущее время
            new_time = self.time
            # Сравнение нового времени с текущим значением
            if int(new_time) < int(current_time[0]) or current_time[0] == 0:
                print(current_time[0])
                # Обновление значения столбца "Time" в базе данных
                cursor.execute("UPDATE Players SET Time = ? WHERE Login = ?", (new_time, self.login))
                conn.commit()

            # Закрытие соединения с базой данных
            conn.close()

    # обновляем таймер
    def update_timer(self):
        self.player.update()
        self.time += 1
        self.setWindowTitle(f"Start - Time: {self.time} seconds")