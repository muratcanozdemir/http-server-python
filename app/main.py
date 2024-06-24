# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')
        lines = request.splitlines()
        if lines:
            request_line = lines[0]
            parts = request_line.split()
            if len(parts) > 1:
                url_path = parts[1]
                if url_path == '/':
                    response = "HTTP/1.1 200 OK\r\n\r\n"
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n"

        client_socket.sendall(response.encode())

if __name__ == "__main__":
    main()
