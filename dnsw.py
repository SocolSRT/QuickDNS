import socket
import struct
import time
import select
DNS_SERVERS = ['9.9.9.9', '1.1.1.1', '94.140.14.14', '77.88.8.8', '208.67.222.222', '8.8.8.8']
DNS_TIMEOUT = 0.1
WHITELIST = ['192.168.1.1', '192.168.1.2']
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 53))
def handle_request(data, client):
    if client[0] not in WHITELIST:
        return
    request = data
    domain = request[-1]
    forward_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    forward_socket.settimeout(DNS_TIMEOUT)
    for dns_server in DNS_SERVERS:
        forward_socket.sendto(request, (dns_server, 53))
        try:
            r, w, x = select.select([forward_socket], [], [], 1)
            if forward_socket in r:
                response, address = forward_socket.recvfrom(1024)
                server_socket.sendto(response, client)
                return
        except socket.timeout:
            continue
    response = struct.pack("!H", 0) + struct.pack("!H", 0) + struct.pack("!H", 3) + struct.pack("!H", 0) + struct.pack("!H", 1) + struct.pack("!H", 0) + struct.pack("!H", 0) + struct.pack("!H", 0) + struct.pack("!H", 0) + struct.pack("!H", 0)
    server_socket.sendto(response, client)
while True:
    data, client = server_socket.recvfrom(1024)
    handle_request(data, client)
