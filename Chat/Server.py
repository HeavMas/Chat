import threading
import socket
import DataBase
from datetime import datetime
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 55013))
sock.listen(15)
name = list()
clients = list()
nicks = list()
LIST_OF_USERS = list()
#ДОДЕЛАТЬ СПИСОК ВСЕХ УЧАСТНИКОВ ЧАТА
def connection(cl_sock):
    while True:
        inc_message = cl_sock.recv(1024)
        date = datetime.now().strftime('%Y-%M-%d %H:%M:%S')
        for i in clients:
            i.send(f"LIST OF USER: {LIST_OF_USERS}".encode())
            i.send(f"{date} {inc_message.decode()}".encode())
def authorisation(conn):
    txt = conn.recv(1024).decode()
    print(txt)
    while True:
        if txt == '1':
            reg_list = list()
            #conn.send('Введите логин'.encode())
            log = conn.recv(1024).decode()
            reg_list.append(log)
            #conn.send('Введите пароль'.encode())
            pas = conn.recv(1024).decode()
            reg_list.append(pas)
            #conn.send('Введите имя, которое будет отображаться в чате'.encode())
            name = conn.recv(1024).decode()
            reg_list.append(name)
            LIST_OF_USERS.append(log)
            DataBase.reg_usr(log, pas, name)
            resp = DataBase.find_usr(reg_list[0], reg_list[1])
            #если датабэйс вернула успех отправляем пользователю успех
            nicks.append(name)
            if resp is True:
                print("успех")
                conn.send("Вы успешно зарегестрировались".encode())
                break
        elif txt == '2':
            while True:
                log_list = list()
                #conn.send('Введите ваш логин'.encode())
                log = conn.recv(1024).decode()
                #conn.send('Введите ваш пароль'.encode())
                log_list.append(log)
                pas = conn.recv(1024).decode()
                log_list.append(pas)
                LIST_OF_USERS.append(log)
                resp = DataBase.find_usr(log_list[0], log_list[1])
                if resp is True:
                    print(1)
                    text = 'Вы успешно авторизировались, нажмите на enter чтобы продолжить'
                    conn.send(text.encode())
                    clients.append(conn)
                    th = threading.Thread(target=connection, args=(conn, ),daemon=True).start()
                    break
                elif resp is False:
                    text = 'Неверный пароль\n'
                    conn.send(text.encode())
                elif resp == "WL":
                    text = 'Пользователя не существует\n'
                    conn.send(text.encode())
            break
        else:
            conn.send("Вы ввели неверные данные\n".encode())
def acception():
    while True:
        conn, addr = sock.accept()
        if conn:
            print(f"Client {addr} connected")
            auth = threading.Thread(target=authorisation, args=(conn,))
            auth.start()
            auth.join()
            chat = threading.Thread(target=connection, args=(conn,), daemon=True)
            chat.start()

acception()