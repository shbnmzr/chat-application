# Import modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 # Port 0 - 655235 can be used if not already in use
LISTENER_LIMIT = 5 # Maximum number of clients
active_clients = [] # Stores currently connected users


# Listens to a client
def listen_for_msg(client, sender_username):
    while True:
        response = client.recv(2048).decode('utf-8')
        if response != '':
            final_msg = sender_username + '~' + response
            broadcast_msg(final_msg)
        else:
            print(f'{sender_username} sent an empty message!!!!')


def unicast_msg(client, msg):
    client.sendall(msg.encode('utf-8'))


# Broadcast message to all clients currently connected to the server
def broadcast_msg(msg):
    for user in active_clients:
        unicast_msg(user[1], msg)


# Handle Clients
def client_handler(client: socket):
    # Server listens for client message containing username
    while True:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            broadcast_msg(f'SERVER ~ {username} has arrived!')
            break
        else:
            print('Username cannot be empty')

    threading.Thread(target=listen_for_msg, args=(client, username, )).start()


# Main Function
def main():
    # Creating socket object
    # AF_INET -> IPv4 will be used
    # SOCK_STREAM -> TCP Protocol will be used
    # SOCK_DGRAM -> UDP Protocol will be used
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Providing server with HOST and PORT
        server.bind((HOST, PORT))
        print('Successfully bound server!')
    except:
        print(f'Unable to bind to {HOST + str(PORT)}')

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # Keep listening to clients' connections
    while True:
        client, address = server.accept()
        print(f'Successfully connected to client {address[0]}{address[1]}')

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()