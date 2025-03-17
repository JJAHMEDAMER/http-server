import socket
from urllib.parse import urlparse


def ports():
    URLS = [
        "http://www.python.org",
        "https://www.mybank.com",
        "ftp://prep.ai.mit.edu",
        "gopher://gopher.micro.umn.edu",
        "smtp://mail.example.com",
        "imap://mail.example.com",
        "imaps://mail.example.com",
        "pop3://pop.example.com",
        "pop3s://pop.example.com",
    ]

    common_ports = []
    for url in URLS:
        parsed_url = urlparse(url)
        port = socket.getservbyname(parsed_url.scheme)
        common_ports.append(port)
        print("{:>6} : {}".format(parsed_url.scheme, port))

    for port in common_ports:
        print(f"Port: {port:>3} -> Service: {socket.getservbyport(port)}")


if __name__ == "__main__":
    ports()
