from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QFont
from kod import StartLabirint
import sqlite3


class RegisterWindow(QMainWindow):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.main = root
        self.initUI()

    # Настройка интерфейся
    def initUI(self):
        self.setWindowTitle('Register')
        self.setGeometry(400, 400, 800, 500)

        self.login = self.create_line("Напишите Логин", 85, 220)
        self.password = self.create_line("Напишите Пароль", 85, 300)
        self.password1 = self.create_line("Повторите Пароль", 85, 375)

        # Кнопка для начала регистрации
        button = self.create_button("Нажми меня", 600, 250)
        button.clicked.connect(self.register)

        self.set_background()

    def create_button(self, text, x, y):
        button = QPushButton(text, self)
        button.setGeometry(x, y, 100, 150)
        button.setStyleSheet("border: none; background-color: transparent; color: #848074;")

        return button

    def create_line(self, text, x, y):
        font = QFont()
        # Устанавливаем размер шрифта
        font.setPointSize(16)

        line = QLineEdit(self)
        line.setPlaceholderText(text)
        line.setGeometry(x, y, 500, 50)
        line.setFont(font)
        line.setStyleSheet("border: none; background-color: transparent; color: #848074;")

        return line

    def set_background(self):
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("image/MyGameRegister.png")))
        self.setPalette(palette)

    def register(self):
        login = str(self.login.text())
        password = str(self.password.text())
        password1 = str(self.password1.text())

        # Подключение к базе данных
        conn = sqlite3.connect('sqlitebase/MyGame_base.sqlite')
        cursor = conn.cursor()

        # Проверка наличия логина в базе данных
        cursor.execute("SELECT login FROM Players WHERE login=?", (login,))
        result = cursor.fetchone()

        try:
            # Если логина нет, добавляем его в базу данных
            if login != '':
                if result is None:
                    if password == password1:
                        if password is not None:
                            cursor.execute("INSERT INTO Players (login, password, time) VALUES (?, ?, 0)", (login, password))
                            conn.commit()
                            QMessageBox.information(self, "Успешно!", "Логин и пароль успешно добавлены в базу данных")
                            self.start(login)
                        else:
                            QMessageBox.information(self, "Ошибка!", "Введите что-то в строку пароль!")
                    else:
                        QMessageBox.information(self, "Ошибка!", "Пароли на совпадают")
                else:
                    QMessageBox.information(self, "Ошибка!", "Такой логин уже существует")
            else:
                QMessageBox.information(self, "Ошибка!", "Поле с Логином не должно быть пустым")
        except sqlite3.Error:
            QMessageBox.information(self, "Ошибка!", "Что-то не так! Попробуйте снова!")

        # Закрытие соединения с базой данных
        conn.close()

    # начать игру
    def start(self, login):
        self.window_play = StartLabirint.StartWindow(str(login))
        self.window_play.show()
        self.hide()

    def closeEvent(self, event):
        self.main.show()
        self.close()