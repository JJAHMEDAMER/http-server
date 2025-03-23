import json
from TCPServer import TCPServer


class HttpServer(TCPServer):
    status = {"code": 200, "message": "OK"}
    req_line = {"version": "HTTP/1.1", "path": "", "method": ""}
    req = {
        "headers": {},
        "body": "",
    }
    res = {
        "headers": {},
        "body": "",
    }

    def parse_req_line(self, req_line: str):
        method, path, version = req_line.split(" ")
        self.req_line["path"] = path
        self.req_line["method"] = method
        self.req_line["version"] = version

    def parse_req_headers(self, headers: str) -> dict:
        self.req_headers = {}
        headers = headers.split("\r\n")
        for header in headers:
            key, value = header.split(": ")
            self.req_headers[key] = value

    def parse_req_body(self, body: str):
        if self.req["headers"]["Content-Type"] == "application/json":
            self.req["body"] = json.loads(body)
        else:
            self.req["body"] = body

    def parse_request(self, data: str):
        self.parse_req_line(data[: data.index("\r\n")])
        self.parse_req_headers(data[data.index("\r\n") + 1 : data.index("\r\n\r\n")])
        self.parse_req_body(data[data.index("\r\n\r\n") + 4 :])

    def handle_request(self, data: str) -> str:
        self.parse_request(data)
        if self.req_line["method"].upper() == "GET":
            self.res["body"] = self.GET(self.req_line["path"])
        elif self.req_line["method"].upper() == "POST":
            self.res["body"] = self.POST(self.req_line["path"], self.req["body"])
        else:
            self.res["body"] = ""
            self.status["code"] = 405
            self.status["message"] = "Method Not Allowed"

        return self.construct_response()

    def GET(self, path: str) -> str:
        self.res["headers"]["Content-Type"] = "text/html"
        return f"<h1>GET request for {path}</h1>"

    def POST(self, path: str, body: str) -> str:
        self.res["headers"]["Content-Type"] = "json"
        return f"""
        {{
            "message": "POST request for {path}",
            "body": {body}
        }}
        """

    def construct_response(self) -> str:
        header_str = ""
        for key, value in self.res["headers"].items():
            header_str += f"{key}: {value}\r\n"

        # fmt: off
        return (
            f"{self.req_line["version"]} {self.status['code']} {self.status['message']}\r\n"
            f"{header_str}"
            f"\r\n"
            f"{self.res["body"]}"
        )
        # fmt: ons


if __name__ == "__main__":
    server = HttpServer()
    server.start()
