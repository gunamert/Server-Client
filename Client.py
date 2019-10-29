import socket


def client_func():
    host = '10.2.25.193'  # as both code is running on same pc
    port = 5002  # socket server port number

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = raw_input("Enter Query: ""(exit)"" for close connection\n")  # take input

    while True:
        if (message == "exit"):
            client_socket.send(message.encode())  # send message
            closeResponse = client_socket.recv(4096).decode()  # receive response
            if (closeResponse == "ok"):
                break

        client_socket.send(message.encode())  # send message
        data = client_socket.recv(4096).decode()  # receive response
        if (data == "error"):
            print('Wrong Query...')
        else:
            print('Query Result : \n' + data)  # show in terminal

        message = raw_input("\n\nEnter Query: \n")  # again take input

    client_socket.close()  # close the connection


def main():
    client_func()


if __name__ == '__main__':
    main()
