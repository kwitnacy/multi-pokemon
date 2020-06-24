from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import socket

private_key = rsa.generate_private_key(
	public_exponent=65537,
	key_size=2048,
	backend=default_backend()
)
public_key = private_key.public_key().public_bytes(
	encoding=serialization.Encoding.PEM,
	format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# print(public_key)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('127.0.0.1', 5000))

data, addr = s.recvfrom(4096)

# print(data)

received_pub_key = serialization.load_pem_public_key(data, default_backend())


print(public_key.decode('utf-8'))

s.sendto(public_key, addr)

mess = received_pub_key.encrypt(
	b'hej',
	padding.OAEP(
        mgf=padding.MGF1(hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None,
	)
)

s.sendto(mess, addr)


data = s.recv(4096)

print(private_key.decrypt(
	data,
	padding.OAEP(
        mgf=padding.MGF1(hashes.SHA1()),
        algorithm=hashes.SHA1(),
        label=None,
		)	 
	)
)


