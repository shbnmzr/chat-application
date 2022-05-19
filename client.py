# Import Modules
import socket
import threading
import server


def send_msg(client):
    while True:
        msg = input('Enter message: ')
        if msg != '':
            client.sendall(msg.encode('utf-8'))
        else:
            print('Message cannot be empty!')


def listen_for_msg(client):
    while True:
        msg = client.recv(2048).decode('utf-8')
        if msg != '':
            username = msg.split('~')[0]
            content = msg.split('~')[1]

            print(f'{username}:\n {content}')
        else:
            print('Message cannot be empty!')


def communicate_with_server(client: socket):
    username = input('Enter username: ')
    if username != '':
        client.sendall(username.encode('utf-8'))
    else:
        print('Username cannot be empty. Exiting!')
        exit(0)

    threading.Thread(target=listen_for_msg, args=(client, )).start()
    send_msg(client)

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server previously created
    try:
        client.connect((server.HOST, server.PORT))
        print('Successfully connected!')
    except:
        print('Server refused connection!')

    communicate_with_server(client)


if __name__=='__main__':
    main()