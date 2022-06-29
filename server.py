import socket
import threading
import time
import requests

ip = requests.get('https://api.ipify.org').text
print(ip)

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = ip
# SERVER = "0.0.0.0"
print(SERVER)
ADDR = (SERVER, PORT)
print(ADDR)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f'[new connection] {addr} connected.')

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f'[{addr}] {msg}')
            conn.send('Msg recieved'.encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {server}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'[active connections] {threading.active_count() - 1}')


print('[STARTING] server is starting...')
start()
