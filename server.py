import threading
import socket


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

client_sockets = set()

def load_users():
    users = {}
    try:
        with open("users.txt", "r") as f:
            for line in f:
                login, password = line.strip().split(":")
                users[login] = password
    except FileNotFoundError:
        print("Ошибка: файл не найден")
    return users

def auth(login, password):
    users = load_users()
    return users.get(login) == password

def send_m(message):
    for client in list(client_sockets):
        try:
            client.send(message)
        except OSError:
            client_sockets.remove(client)

def listening(client, client_address):
    with client:
        data = client.recv(1024).decode('utf-8')
        login, password = data.split("|")
        if auth(login, password):
            client.send("AUTH_SUCCESS".encode('utf-8'))
            print(f"{login} успешно авторизован")
        else:
            client.send("AUTH_BAD".encode('utf-8'))
            client.close()
            print(f"{login} не авторизован")
            return
        while True:
            try:
                message = client.recv(1024)
                send_m(message)
            except:
                client_sockets.remove(client)
                client.close()
                print(f"[-] {client_address} отключился")
                send_m(f"{client_address} отключился".encode('utf-8'))
                break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen()
    print(f"Адрес сервера {SERVER_HOST}:{SERVER_PORT}")
    while True:
        client_socket, client_address = s.accept()
        print(f"[+] {client_address} подключился")
        client_sockets.add(client_socket)
        t = threading.Thread(target=listening, args=(client_socket, client_address))
        t.start()