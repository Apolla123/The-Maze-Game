from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from kod import StartInvite, Level
import sys


class MyGame(QWidget):
    def __init__(self):
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса
        self.initUI()

    # Настройка интерфейся
    def initUI(self):
        self.setGeometry(400, 400, 800, 500)
        self.setWindowTitle('MyGame Starting')

        self.create_start_button()
        self.create_levels_button()
        self.set_background()

    # Кнопка старта
    def create_start_button(self):
        self.btn_start = self.create_button('Начать Играть', 150, 220)
        self.btn_start.clicked.connect(self.start_register)

    # Кнопка посмотреть пройденые уровни
    def create_levels_button(self):
        self.btn_levels = self.create_button('Рейтинг По Времени', 150, 330)
        self.btn_levels.clicked.connect(self.level)

    # Создаём кнопки
    def create_button(self, text, x, y):
        button = QPushButton(text, self)
        button.setGeometry(x, y, 500, 100)
        button.setStyleSheet("color: #848074; background-color: #a8a7a1; font-size: 40px; font-weight: bold;"
                             "border-radius: 20px; border: 5px solid #93918b;")
        return button

    def set_background(self):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("image/Mygame.png")))
        self.setPalette(palette)

    # Окно с началом регистрации/входа
    def start_register(self):
        self.window_register = StartInvite.StartRegisterWindow(self)
        self.window_register.show()
        self.hide()

    # Окно с топ 3 по рейтингу
    def level(self):
        self.window_levels = Level.LevelWindow(self)
        self.window_levels.show()
        self.hide()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# запуск
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyGame()
    widget.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())