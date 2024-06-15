from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont
from kod import RegisterPlayer, EntryPlayer


class StartRegisterWindow(QMainWindow):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.main = root
        self.initUI()

    # Настройка интерфейся
    def initUI(self):
        self.setGeometry(400, 400, 800, 500)
        self.setWindowTitle('Invite')

        self.create_entry_button()
        self.create_register_button()
        self.set_background()

    # Кнопка для входа
    def create_entry_button(self):
        self.entry_btn = self.create_button('Вход', 150, 100)
        self.entry_btn.clicked.connect(self.entry)

    # Кнопка для регистрации
    def create_register_button(self):
        self.register_btn = self.create_button('Регистрация', 150, 250)
        self.register_btn.clicked.connect(self.register)

    # Создаём кнопки
    def create_button(self, text, x, y):
        font = QFont()
        # Устанавливаем размер шрифта
        font.setPointSize(16)

        button = QPushButton(text, self)
        button.setGeometry(x, y, 500, 100)
        button.setFont(font)
        button.setStyleSheet("color: #848074; background-color: #a8a7a1; font-size: 40px; font-weight: bold;"
                             "border-radius: 20px; border: 5px solid #93918b;")
        return button

    def set_background(self):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("image/MyGameInvite.jpg")))
        self.setPalette(palette)

    # создаём окно входа
    def entry(self):
        self.window_levels = EntryPlayer.EntryWindow(self)
        self.window_levels.show()
        self.hide()

    # создаём окно регистрации
    def register(self):
        self.window_levels = RegisterPlayer.RegisterWindow(self)
        self.window_levels.show()
        self.hide()

    def closeEvent(self, event):
        self.main.show()
        self.close()