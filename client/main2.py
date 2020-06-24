from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import atexit
import os
import time
import socket 
import threading

frame = {
	'login': 0x01,
	'logout': 0x02,
	'signup': 0x03,
	'add contact': 0x04,
	'edit contact': 0x08,
	'delete contact': 0x0C,
	'END_TRANS': 0x20
}

SERVER_ADDR_MAIN = '192.168.0.20'
SERVER_PORT_MAIN = 1337

USER_NAME = 'rojberqwe'
PASSWD = '123QWERTY'
EMAIL = 'kwitn@put.poznna.pl'

HOST = socket.gethostbyname(socket.gethostname())
PORT = 4200

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

# s_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s_broadcast.bind((HOST, PORT + 1))

# s_loc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s_loc.bind((HOST, PORT + 2))


def broadcast_fun():
	global MAIN_AES_ENGINE
	while True:
		data = s_broadcast.recv(4096) 
		print(MAIN_AES_ENGINE.decrypt(data[:12], data[12:], None))
	
	print('hej1')


def send_loc():
	val_x, val_y = 1000, 1000
	
	while True:
		data_ = USER_NAME + '|(' + str(val_x) + ',' + str(val_y) + ')'
		s_loc.sendto(bytes(data_, 'utf-8'), (HOST, 2001))	
		val_x -= 1
		val_y -= 1
		time.sleep(0.05)


def crypto_stuff(sock):
	global SERVER_ADDR_MAIN, SERVER_PORT_MAIN
	private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
	public_key = private_key.public_key()
	public_key_bytes = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

	s.sendto(public_key_bytes, (SERVER_ADDR_MAIN, SERVER_PORT_MAIN))
		
	data, SERVER_ADDR = s.recvfrom(4096)
	print(data)
	server_public_key = serialization.load_pem_public_key(data, backend=default_backend())
	shared_key = private_key.exchange(ec.ECDH(), server_public_key)
	derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data', backend=default_backend()).derive(shared_key)

	return AESGCM(derived_key), SERVER_ADDR

# sign up, begin
sign_up_data = {
	'user_name' : USER_NAME,
	'passwd_hash' : PASSWD,
	'email_hash' : EMAIL
}
mess = bytearray()
mess.append(frame['signup'])
mess.append(0x00)
mess.extend(map(ord, str(sign_up_data)))

aes_engine, SERVER_ADDR = crypto_stuff(s)
nonce = os.urandom(12)

ct = aes_engine.encrypt(nonce, bytes(mess), None)

s.sendto(nonce + ct, SERVER_ADDR)

data = s.recv(1024)

print(aes_engine.decrypt(data[:12], data[12:], None))

mess = bytearray()
mess.append(frame['END_TRANS'])
mess.append(0x00)
nonce = os.urandom(12)

ct = aes_engine.encrypt(nonce, bytes(mess), None)

s.sendto(nonce + ct, SERVER_ADDR)

data = s.recv(1024)

print(aes_engine.decrypt(data[:12], data[12:], None))

MAIN_AES_ENGINE = aes_engine
# sign up, end


# login, begin:
log_in_data = {
	'user_name' : USER_NAME,
	'passwd_hash' : PASSWD,
	'email_hash' : EMAIL
}

mess = bytearray()
mess.append(frame['login'])
mess.append(0x00)
mess.extend(map(ord, str(log_in_data)))

aes_engine, SERVER_ADDR = crypto_stuff(s)
nonce = os.urandom(12)

ct = aes_engine.encrypt(nonce, bytes(mess), None)

s.sendto(nonce + ct, SERVER_ADDR)

data = s.recv(1024)

print(aes_engine.decrypt(data[:12], data[12:], None))

mess = bytearray()
mess.append(frame['END_TRANS'])
mess.append(0x00)
nonce = os.urandom(12)

ct = aes_engine.encrypt(nonce, bytes(mess), None)

s.sendto(nonce + ct, SERVER_ADDR)

data = s.recv(1024)

print(aes_engine.decrypt(data[:12], data[12:], None))

MAIN_AES_ENGINE = aes_engine
# login, end:


# logout, begin:
log_out_data = {
	'user_name' : USER_NAME,
	'passwd_hash' : PASSWD,
	'email_hash' : EMAIL
}

mess = bytearray()
mess.append(frame['logout'])
mess.append(0x00)
mess.extend(map(ord, str(log_out_data)))

aes_engine, SERVER_ADDR = crypto_stuff(s)
nonce = os.urandom(12)

ct = aes_engine.encrypt(nonce, bytes(mess), None)

s.sendto(nonce + ct, SERVER_ADDR)

data = s.recv(1024)

print(aes_engine.decrypt(data[:12], data[12:], None))

mess = bytearray()
mess.append(frame['END_TRANS'])
mess.append(0x00)
nonce = os.urandom(12)

ct = aes_engine.encrypt(nonce, bytes(mess), None)

s.sendto(nonce + ct, SERVER_ADDR)

data = s.recv(1024)

print(aes_engine.decrypt(data[:12], data[12:], None))
# logout, end:

