import asyncio
import socket
import threading
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


# /////////////////////////////////////////////////////////////////////////////
# {functions}
def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))


def receive_message():
    while True:
        print(client.recv(2048).decode(FORMAT))


# /////////////////////////////////////////////////////////////////////////////


# wait for another client to connect
while client.recv(2048).decode(FORMAT) == 'wait':
    print('Dear client, Please wait')
    time.sleep(10)

# make a thread for receive messages continuously
thread = threading.Thread(target=receive_message)
thread.start()

# for sending message
while True:
    send(input('enter message: '))
