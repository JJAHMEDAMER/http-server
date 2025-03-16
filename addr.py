import socket


def addr():
    print(socket.gethostname())  # Print the hostname of the machine

    ## DNS lookup
    print("google.com: ", socket.gethostbyname("google.com"))  # Print the IP address of google.com
    print("this machine: ", socket.gethostbyname(socket.gethostname()))  # Print the IP address of the machine

    HOSTS = ["apu", "pymotw.com", "www.python.org", "nosuchname"]

    for host in HOSTS:
        print(host)
        try:
            name, aliases, addresses = socket.gethostbyname_ex(host)  # use hostname to get hostname info

            ipAddr = socket.gethostbyname(host)
            name, aliases, addresses = socket.gethostbyaddr(ipAddr)  # use Ip address to get hostname info

            print("  Hostname:", name)  # the actual hostname (DNS A record or DNS AAAA record)
            print("   Aliases:", aliases)  # the domain name (DNS CNAME record)
            print(" Addresses:", addresses)  # IP addresses
        except socket.error as msg:
            print("ERROR:", msg)
        print()


if __name__ == "__main__":
    addr()
