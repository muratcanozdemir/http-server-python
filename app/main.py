import socket
import threading
import sys
import os

def handle_client(client_socket):
    try:
        request_data = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            request_data += data

        print("Complete request received:")
        print(request_data.decode('utf-8', errors='replace'))

        headers = {}
        body = b''

        # Decode and split request into lines
        try:
            request_text = request_data.decode('utf-8')
        except UnicodeDecodeError:
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            client_socket.close()
            return

        lines = request_text.split("\r\n")

        if lines:
            request_line = lines[0]
            parts = request_line.split()
            if len(parts) >= 2:
                method = parts[0]
                url_path = parts[1]
                print(f"method='{method}', url_path='{url_path}'")

                # Read headers
                i = 1
                while i < len(lines) and lines[i]:
                    if ':' in lines[i]:
                        header_name, header_value = lines[i].split(":", 1)
                        headers[header_name.strip()] = header_value.strip()
                    i += 1

                print("Headers received:")
                for header, value in headers.items():
                    print(f"{header}: {value}")

                # Read the body based on Content-Length header
                if "Content-Length" in headers:
                    content_length = int(headers["Content-Length"])
                    body_start = request_text.find("\r\n\r\n") + 4
                    body = request_data[body_start:body_start+content_length]
                    
                    # If body is not fully read, continue reading from the socket
                    while len(body) < content_length:
                        body += client_socket.recv(content_length - len(body))
                    
                    print(f"Body received: {body.decode('utf-8', errors='replace')}")

                if method == "POST":
                    if url_path.startswith("/files/"):
                        filename = url_path[len("/files/"):]
                        file_path = os.path.join(directory_path, filename)

                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        print(f"Creating file: {file_path}")

                        try:
                            with open(file_path, "wb") as f:
                                f.write(body)
                                response = b"HTTP/1.1 201 Created\r\n\r\n"
                        except Exception as e:
                            print(f"Error writing file: {e}")
                            response = b"HTTP/1.1 500 Internal Server Error\r\n\r\n"
                    else:
                        response = b"HTTP/1.1 404 Not Found\r\n\r\n"
                else:
                    response = b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            else:
                response = b"HTTP/1.1 400 Bad Request\r\n\r\n"
        else:
            response = b"HTTP/1.1 400 Bad Request\r\n\r\n"

        # Send response back to client
        print("Sending response:")
        print(response.decode('utf-8', errors='replace'))
        client_socket.sendall(response)
        client_socket.shutdown(socket.SHUT_WR)
        client_socket.close()
    except Exception as e:
        print(f"Error handling client: {e}")
        try:
            client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        except Exception as e:
            print(f"Failed to send error response: {e}")
    finally:
        client_socket.close()

def main():
    print("Logs from your program will appear here!")

    global directory_path
    if len(sys.argv) > 1 and sys.argv[1] == "--directory" and len(sys.argv) > 2:
        directory_path = sys.argv[2]

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening on port 4221")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
