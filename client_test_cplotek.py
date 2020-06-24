import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

socket_recv.bind(('localhost', 5000))

server_address = ('localhost', 5555)
message = bytes('dziendobry', encoding='utf-8')

sent = sock.sendto(message, server_address)
print(sent)

