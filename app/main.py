import socket
import threading
import sys
import os


def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        lines = request.splitlines()
        if lines:
            request_line = lines[0]
            parts = request_line.split()
            if len(parts) > 1:
                method = parts[0]
                url_path = parts[1]
                print(" ".join(f"{method=}", f"{url_path =}"))

                headers = {}
                i = 1
                while i < len(lines) and lines[i]:
                    if ':' in lines[i]:
                        header_name, header_value = lines[i].split(":", 1)
                        headers[header_name.strip()] = header_value.strip()
                    i += 1
                
                if method == "GET":
                    if url_path == '/':
                        response = "HTTP/1.1 200 OK\r\n\r\n".encode()
                    elif url_path.startswith("/echo/"):
                        echo_str = url_path[len("/echo/"):]
                        response_body = echo_str
                        content_length = len(response_body)
                        response = (
                            "HTTP/1.1 200 OK\r\n"
                            f"Content-Type: text/plain\r\n"
                            f"Content-Length: {content_length}\r\n\r\n"
                            f"{response_body}".encode()
                        )
                    elif url_path == "/user-agent":
                        user_agent = headers.get("User-Agent", "Unknown")
                        response_body = user_agent
                        content_length = len(response_body)
                        response = (
                            "HTTP/1.1 200 OK\r\n"
                            f"Content-Type: text/plain\r\n"
                            f"Content-Length: {content_length}\r\n\r\n"
                            f"{response_body}".encode()
                        )
                    elif url_path.startswith("/files/"):
                        filename = url_path[len("/files/"):]
                        file_path = os.path.join(directory_path, filename)
                        print(f"Trying to serve file: {file_path}")

                        try:
                            with open(file_path, "rb") as f:
                                body = f.read()
                            content_length = len(body)
                            response = (
                                "HTTP/1.1 200 OK\r\n"
                                "Content-Type: application/octet-stream\r\n"
                                f"Content-Length: {content_length}\r\n\r\n"
                            ).encode() + body
                        except Exception as e:
                            print(f"Error serving file: {e}")
                            response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
                elif method == "POST":
                    if url_path.startswith("/files/"):
                        filename = url_path[len("/files/"):]
                        file_path = os.path.join(directory_path, filename)
                        content_length = int(headers.get("Content-Length", 0))
                        
                        # Read the request body
                        body = client_socket.recv(content_length).decode('utf-8')

                        try:
                            with open(file_path, "wb") as f:
                                f.write(body)
                            response = "HTTP/1.1 201 Created\r\n\r\n".encode()
                        except Exception as e:
                            print(f"Error writing file: {e}")
                            response = "HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()
                    else:
                        response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

        client_socket.sendall(response)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def main():
    print("Logs from your program will appear here!")
    
    global directory_path
    if len(sys.argv) > 1 and sys.argv[1] == "--directory" and len(sys.argv) > 2:
        directory_path = sys.argv[2]
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))

        client_handler.start()
        #test

if __name__ == "__main__":
    main()
