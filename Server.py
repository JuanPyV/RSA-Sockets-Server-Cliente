from socket import *
from threading import Thread

client_sock = []  # almacena los sockets de los clientes
client_addresses = {}  # almacena {key: client socket, values: client address}
public_key = []  # almacena las llaves publicas


def accept_incoming_connections():

    client, client_address = SERVER.accept()
    client_sock.append(client)
    print("%s:%s se conecto." % client_address)
    public_key.append(client.recv(BUFFER_SIZE))
    client_addresses[client] = client_address


def handle_client1(client_sock, client_addresses):

    client_sock[0].send(public_key[1])

    while True:
        msg0 = client_sock[0].recv(BUFFER_SIZE)
        client_sock[1].send(msg0)
        print(" Client 1: %s" % msg0.decode('utf8'))


def handle_client2(client_sock, client_addresses):

    client_sock[1].send(public_key[0])

    while True:
        msg1 = client_sock[1].recv(BUFFER_SIZE)
        client_sock[0].send(msg1)
        print(" Client 2: %s" % msg1.decode('utf8'))


# ----SOCKET Part----
HOST = "127.0.0.1"
PORT = 1234
BUFFER_SIZE = 1024
ADDRESS = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

SERVER.listen(2)
print('Server IP: ', HOST)
print("Esperando conexion...")
accept_incoming_connections()
accept_incoming_connections()

Thread(target=handle_client1, args=(client_sock, client_addresses)).start()
Thread(target=handle_client2, args=(client_sock, client_addresses)).start()
SERVER.close()
