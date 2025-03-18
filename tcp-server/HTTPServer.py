from TCPServer import TCPServer


class HttpServer(TCPServer):
    status = {"code": 200, "message": "OK"}
    version = "HTTP/1.1"
    path = ""
    method = ""
    req_headers = {}
    res_headers = {}

    def parse_request_line(self, data: str):
        method, path, version = data.split(" ")
        self.path = path
        self.method = method
        self.version = version  # Remove the "\r\n" at the end

    def parse_headers(self, headers: str) -> dict:
        self.req_headers = {}
        headers = headers.split("\r\n")
        for header in headers:
            key, value = header.split(": ")
            self.req_headers[key] = value

    def handle_request(self, data: str) -> str:
        self.parse_request_line(data[: data.index("\r\n")])
        self.req_headers = self.parse_headers(data[data.index("\r\n") + 1 : data.index("\r\n\r\n")])
        req_body = data[data.index("\r\n\r\n") + 4 :]  # 4 is the length of "\r\n\r\n"

        body = ""
        if self.method == "GET":
            body = self.GET(self.path)
        elif self.method == "POST":
            body = self.POST(self.path, req_body)

        return self.construct_response(body)

    def GET(self, path: str) -> str:
        self.res_headers["Content-Type"] = "text/html"
        return f"<h1>GET request for {path}</h1>"

    def POST(self, path: str, body: str) -> str:
        self.res_headers["Content-Type"] = "json"
        return f"""
        {{
            "message": "POST request for {path}",
            "body": {body}
        }}
        """

    def construct_response(self, data: str) -> str:
        res_headers = ""
        for key, value in self.res_headers.items():
            res_headers += f"{key}: {value}\r\n"

        # fmt: off
        return (
            f"{self.version} {self.status['code']} {self.status['message']}\r\n"
            f"{res_headers}"
            f"\r\n"
            f"{data}"
        )
        # fmt: ons


if __name__ == "__main__":
    server = HttpServer()
    server.start()
