import socket


class TCPServer:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(1)
            print(f"Server running on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                print(f"Connection from {addr}")

                data = conn.recv(1024 * 2)
                print(data)
                if not data:
                    break

                # fmt: off
                res = (
                    "HTTP/1.1 200 OK\r\n"
                    "\r\n"
                ) + data.decode()
                # fmt: on

                print(res)
                conn.sendall(res.encode())
                conn.close()


if __name__ == "__main__":
    server = TCPServer()
    server.start()
