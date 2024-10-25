import socket
import threading
import sys


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

def listen_messages():
    while True:
        try:
            message = s.recv(1024).decode('utf-8')
            if not message:
                print("[!] Отключен от сервера")
                break
            print("[#]" + message)
        except ConnectionError:
            print("[!] Соединение потеряно")
            break
    sys.exit(0)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((SERVER_HOST, SERVER_PORT))
        print(f"[+] Подключен к {SERVER_HOST}:{SERVER_PORT}")

        login = input("Введите логин:")
        password = input("Введите пароль: ")
        data = f"{login}|{password}"
        s.send(data.encode('utf-8'))
        auth_response = s.recv(1024).decode('utf-8')
        if auth_response == "AUTH_SUCCESS":
            print("Вы авторизованы")
        else:
            print("Вы не авторизованы. Отключение...")
            sys.exit(1)

        t = threading.Thread(target=listen_messages)
        t.daemon = True
        t.start()

        print("Пишите ваше сообщение. Введите 'q' для выхода")
        while True:
            message = input()
            if message.lower() == "q":
                print("[!] Отключение...")
                s.close()
                break
            message = f"{login} | {message}"
            s.send(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("\n[!] Прервано пользователем")
    except ConnectionError:
        print("[!] Ошибка соединения")
    finally:
        s.close()
        print("[!] Клиент отключен")