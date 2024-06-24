import socket
import threading
import sys

directory = "/tmp"

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    lines = request.splitlines()
    if lines:
        request_line = lines[0]
        parts = request_line.split()
        if len(parts) > 1:
            url_path = parts[1]
            print(f"{url_path=}")
            headers = {}
            for line in lines[1:]:
                if line:
                    header_name, header_value = line.split(":", 1)
                    headers[header_name.strip()] = header_value.strip()
            if url_path == '/':
                response = "HTTP/1.1 200 OK\r\n\r\n"
            elif url_path.startswith("/echo/"):
                echo_str = url_path[len("/echo/"):]
                response_body = echo_str
                content_length = len(response_body)
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {content_length}\r\n\r\n"
                    f"{response_body}"
                )
            elif url_path == "/user-agent":
                user_agent = headers.get("User-Agent", "Unknown")
                response_body = user_agent
                content_length = len(response_body)
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    f"Content-Type: text/plain\r\n"
                    f"Content-Length: {content_length}\r\n\r\n"
                    f"{response_body}"
                )
            elif url_path.startswith("/files"):
                directory = sys.argv[2]
                filename = url_path[7:]
                print(directory, filename)
                try:
                    with open(f"/{directory}/{filename}", "r") as f:
                        body = f.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
                except Exception as e:
                    response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"

    client_socket.sendall(response.encode())

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))

        client_handler.start()
        #test

if __name__ == "__main__":
    main()
