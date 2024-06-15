from PyQt5.QtWidgets import QMainWindow, QLineEdit
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont
import sqlite3


class LevelWindow(QMainWindow):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.main = root
        self.initUI()

    # Настройка интерфейся
    def initUI(self):
        self.setWindowTitle('Levels')
        self.setGeometry(400, 400, 800, 500)

        self.set_background()
        self.create_line_edit_widgets()
        self.update_top_players()

    def set_background(self):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("image/MyGameRating.png")))
        self.setPalette(palette)

    def create_line_edit_widgets(self):
        font = QFont()
        # Устанавливаем размер шрифта
        font.setPointSize(20)

        positions = [(215, 195), (215, 270), (215, 350)]
        self.line_edit_widgets = []

        for position in positions:
            line_edit = QLineEdit(self)
            line_edit.setGeometry(215, 195, 350, 30)
            line_edit.setFont(font)
            line_edit.setReadOnly(True)
            line_edit.setStyleSheet("border: none; background-color: transparent; color: #848074;")
            line_edit.move(*position)
            self.line_edit_widgets.append(line_edit)

    # Делаем топ-3
    def update_top_players(self):
        conn = sqlite3.connect('sqlitebase/MyGame_base.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT Login, Time FROM Players WHERE Time > 0 ORDER BY Time LIMIT 3")
        top_players = cursor.fetchall()

        for i, player in enumerate(top_players):
            login, time = player
            self.line_edit_widgets[i].setText(f"{login} - {time} sec")

        conn.close()

    def closeEvent(self, event):
        self.main.show()
        self.close()