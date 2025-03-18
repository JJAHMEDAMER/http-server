import socket


class TCPServer:
    def __init__(self, host="127.0.0.1", port=5000):
        self.addr = (host, port)
        self.buffer_size = 8

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.addr)
            s.listen(1)
            print(f"Server running on {self.addr[0]}:{self.addr[1]}")

            while True:
                conn, addr = s.accept()
                print(f"Connection from {addr}")

                data = conn.recv(1024 * self.buffer_size)
                if not data:
                    break

                res = self.handle_request(data.decode())

                print(res)

                conn.sendall(res.encode())
                conn.close()

    def handle_request(self, data: str) -> str:
        status_line = "HTTP/1.1 200 OK\r\n"

        headers_arr = [
            "Content-Type: text",
        ]

        headers = ""
        for header in headers_arr:
            headers += header + "\r\n"

        headers_end = "\r\n"

        body = "Hello from the server \n" + data

        res = f"{status_line}{headers}{headers_end}{body}"
        return res


if __name__ == "__main__":
    server = TCPServer()
    server.start()
