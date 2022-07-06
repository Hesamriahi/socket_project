import socket
import threading
import time
import requests

# ip = requests.get('https://api.ipify.org').text
# print(ip)

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
# SERVER = '192.168.1.10'
# SERVER = ip
# SERVER = "0.0.0.0"
print(f'server is {SERVER}')
ADDR = (SERVER, PORT)
print(f'ADDR is {ADDR}')
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
# /////////////////////////////////////////////////////////////////////////////

# for ipv4 with tcp protocol &&& for ipv6 with udp protocol
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

server.bind(ADDR)
connections = []


# /////////////////////////////////////////////////////////////////////////////
# {functions}

# Specifies the opposite connection
def opposite_side(conn):
    if conn == connections[0]:
        return connections[1]
    if conn == connections[1]:
        return connections[0]


def send_message_to_client(conn, msg):
    print(f'&*&*&*&* [SEND MESSAGE] {msg} to {conn}&*')
    conn.send(msg.encode(FORMAT))


# send 'start' to clients
def start_conversation(here_connections):
    for conn in here_connections:
        send_message_to_client(conn, 'start')
        thread = threading.Thread(target=handle_client, args=(conn,))
        thread.start()
        print(f'[CONNECTION STARTED] to {conn}')


# it recieve message from one client and send it for opposite client
def handle_client(conn):
    print(f'[new connection] SOMEONE connected.')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[SAID] {msg}")
            other_side = opposite_side(conn)
            send_message_to_client(other_side, msg)

    conn.close()


# /////////////////////////////////////////////////////////////////////////////
# connect with clients and wait until 2 clients connect, then connect them together
def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {server}')
    while True:
        conn, addr = server.accept()
        connections.append(conn)
        if len(connections) == 1:
            send_message_to_client(conn, 'wait')
        if len(connections) == 2:
            start_conversation(connections)

        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')


# /////////////////////////////////////////////////////////////////////////////


print('[STARTING] server is starting...')
start()
