import socket
import threading
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QTextBrowser
from time import sleep
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 55013))
Name = ''
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat App")
        self.setGeometry(200, 200, 400, 200)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.login_label = QLabel("Login:")
        self.login_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Log in")
        self.login_button.clicked.connect(self.register)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.login)

        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.username_label)
        hbox1.addWidget(self.username_input)
        vbox.addLayout(hbox1)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.password_label)
        hbox2.addWidget(self.password_input)
        vbox.addLayout(hbox2)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.login_label)
        hbox3.addWidget(self.login_input)
        vbox.addLayout(hbox3)
        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.login_button)
        hbox4.addWidget(self.register_button)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)

    def login(self):
        # implement login functionality here
        sock.send("1".encode())
        login = self.login_input.text()
        password = self.password_input.text()
        sock.send(login.encode())
        sleep(1)
        sock.send(password.encode())
        sock.send(self.username_input.text().encode())
        succes = sock.recv(1024).decode()
        print(succes)
        if succes == ("Вы успешно зарегестрировались"):
            self.close()
            self.chat_window = ChatWindow()
            self.chat_window.show()

    def register(self):
        global Name
        # implement registration functionality here
        username = self.username_input.text()
        password = self.password_input.text()
        login = self.login_input.text()
        sock.send("2".encode())
        sock.send(login.encode())
        sleep(1)
        Name = username
        sock.send(password.encode())
        succes = sock.recv(1024).decode()
        if succes == "Вы успешно авторизировались, нажмите на enter чтобы продолжить":
            self.close()
            self.chat_window = ChatWindow()
            self.chat_window.show()



class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat App")
        self.setGeometry(200, 200, 600, 400)

        self.list_users = QtWidgets.QLabel()
        self.chat_box = QTextBrowser()
        self.chat_box.setReadOnly(True)

        self.message_input = QLineEdit()

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        vbox = QVBoxLayout()
        vbox.addWidget(self.chat_box)
        hbox = QHBoxLayout()
        hbox.addWidget(self.message_input)
        hbox.addWidget(self.send_button)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        th = threading.Thread(target=self.reciever,daemon=True).start()
    def reciever(self):
        while True:
            self.message = sock.recv(1024).decode()
            print(self.message)
            self.chat_box.append(self.message)
    def send_message(self):
        global Name
        # implement send message functionality here
        self.smessage = self.message_input.text()
        sock.send((Name + ': ' + self.smessage).encode())
    #ДОДЕЛАТЬ ИМЯ ПОЛЬЗОВАТЕЛЯ

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

