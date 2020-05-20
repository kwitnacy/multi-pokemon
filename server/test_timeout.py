import socket as s


sock = s.socket(s.AF_INET, s.SOCK_DGRAM)

sock.bind(('127.0.0.1', 10001))

sock.settimeout(1)

try:
    data = sock.recv(4096)
except s.timeout:
    print('hej')
