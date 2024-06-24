# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept() # wait for client

    while True:
        client_socket, client_address = server_socket.accept()
        print(f{"Connection from {client_address}"})

        request = client_socket.recv(1024)
        print(f{"Received request: {request}"})

        response = "HTTP/1.1 200 OK\r\n\r\n"
        client_socket.sendall(response.encode())

        client_socket.close()


if __name__ == "__main__":
    main()
