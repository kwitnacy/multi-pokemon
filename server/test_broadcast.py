from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import socket as s
import threading
import os
import json
import time 

from users import users


HOST = s.gethostbyname(s.gethostname())
PORT = 1337
PORT_BROAD = 2000
PORT_GET_LOC = 2001

print('SERVER ADDR: ' + HOST + ':' + str(PORT))

FREE_PORTS = [i for i in range(1338, 1501, 1)]

ONLINE_USERS = {}

RUNNING = True

socket_recv = s.socket(s.AF_INET, s.SOCK_DGRAM)
socket_recv.bind((HOST, PORT))

socket_broad = s.socket(s.AF_INET, s.SOCK_DGRAM)
socket_broad.bind((HOST, PORT_BROAD))

socket_get_loc = s.socket(s.AF_INET, s.SOCK_DGRAM)
socket_get_loc.bind((HOST, PORT_GET_LOC))


### Utilities --- begin

def log(data: str = ''):
	with open('log', 'a') as log:
		log.write(time.strftime('[%h %d %H:%M:%S') + '] ' + data + '\n')


def print_data(data, addr):
	print('[' + addr[0] + ':' + str(addr[1]) + '] send -> ' + str(data))


def close_all_that_shit():
	# TODO:
	# TODO: close all connections
	# TODO: close sockets
	# TODO: save new users to somewhere
	pass


def session(data, addr, free_port):
	session_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
	session_socket.bind((HOST, free_port))
	
	# server private key
	private_key = ec.generate_private_key(ec.SECP384R1, default_backend())
	
	# server public key
	public_key = private_key.public_key()	
	
	# server public key bytes
	public_key_bytes = public_key.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	
	# server sends public key bytes to client
	session_socket.sendto(public_key_bytes, addr)
	
	# server gets public key from client (bytes -> obj)
	client_public_key = serialization.load_pem_public_key(data, backend=default_backend())
	
	shared_key = private_key.exchange(ec.ECDH(), client_public_key)

	derived_key = HKDF(
	    algorithm=hashes.SHA256(),
	    length=32,
	    salt=None,
	    info=b'handshake data',
	    backend=default_backend()
	).derive(shared_key)
	
	aesgcm = AESGCM(derived_key)
	
	transmision_running = True
	while transmision_running:
		# request
		data, addr = session_socket.recvfrom(1024)

		mess = aesgcm.decrypt(data[:12], data[12:], None)
		
		nounce = os.urandom(12)
		
		d = str(mess[2:])
		
		res_code = 0x40

		# login
		if mess[0] == 0x01:
			j = json.loads(d[2:-1].replace("'", "\""))
			if users[j['user_name']]['passwd_hash'] == j['passwd_hash']:
				log('Login from: ' + str(addr[0]) + ':' + str(addr[1]) + ', username: ' + j['user_name'] + ': success :)')
				ONLINE_USERS[j['user_name']] = users[j['user_name']]
				ONLINE_USERS[j['user_name']]['ip_addr'] = (addr[0], addr[1])
				ONLINE_USERS[j['user_name']]['aes_engine'] = AESGCM(derived_key)
				res_code = 0x80
			else:
				log('Login from: ' + str(addr[0]) + ':' + str(addr[1]) + ', username: ' + j['user_name'] + ': error :( ')
				res_code = 0x40
		# logout
		elif mess[0] == 0x02:
			j = json.loads(d[2:-1].replace("'", "\""))
			log('Logout from: ' + str(addr[0]) + ':' + str(addr[1]) + ', username: ' + j['user_name'])
			users[j['user_name']] = ONLINE_USERS[j['user_name']]
			users[j['user_name']]['ip_addr'] = None
			del(ONLINE_USERS[j['user_name']])
		# sign up
		elif mess[0] == 0x03:
			j = json.loads(d[2:-1].replace("'", "\""))
			if j['user_name'] in users:
				log('Sign-in from: ' + str(addr[0]) + ':' + str(addr[1]) + ', username: ' + j['user_name'] + ': name taken, account was not created')
				res_code = 0x40

			else:
				log('Sign-in from: ' + str(addr[0]) + ':' + str(addr[1]) + ', username: ' + j['user_name'] + ': account was created')
				users[j['user_name']] = j
				users[j['user_name']]["ip_addr"] = None
				users[j['user_name']]["loc"] = None
				users[j['user_name']]["friends"] = []
				res_code = 0x80
		# add contact
		elif mess[0] == 0x04:
			pass
		# Edit contact
		elif mess[0] == 0x08:
			pass
		# Delete contact
		elif mess[0] == 0x0C:
			pass
		# End transmission
		elif mess[0] == 0x20:
			transmision_running = False
		
		mess = bytearray(mess)
		mess[0] |= res_code

		ct = aesgcm.encrypt(nounce, bytes(mess), None)

		# response
		session_socket.sendto(nounce + ct, addr)

	session_socket.close()
	FREE_PORTS.append(free_port)
	FREE_PORTS.sort()


### Utilities --- end


def recv(socket):
	global RUNNING

	if socket is None:
		return 1
	
	socket.settimeout(10)
	while RUNNING:
		try:
			data, addr = socket.recvfrom(1024)
			threading.Thread(target=session, args=(data, addr, FREE_PORTS.pop(), )).start()
		except s.timeout:
			pass
	
	print('exited recv thread.')


def server_console():
	global RUNNING
	commands = ['ousers  	-> prints online users', 
				'users 		-> print all users', 
				'quit/close	-> fucks everything up', 
				'help 		-> help'
				]
	
	while RUNNING:
		command = input('>>>')
		if command == 'ousers':
			print(ONLINE_USERS)
		elif command == 'users':
			print(users)
		elif command == 'quit' or command == 'close':
			close_all_that_shit()
			RUNNING = False
			break
		elif command == 'help':
			for x in commands:
				print(x)
		else:
			print('wrong command')
			for x in commands:
				print(x)
	
	print('exited console thread.')


def broadcast(socket):
	global RUNNING

	while RUNNING:
		data = {name: ONLINE_USERS[name]['loc'] for name in ONLINE_USERS.keys()}
		addresses = {name: (ONLINE_USERS[name]['ip_addr'], ONLINE_USERS[name]['aes_engine']) for name in ONLINE_USERS.keys()}
		to_send = bytes(json.dumps(data), 'utf-8')

		for (addr, aes_engine) in addresses.values():
			nounce = os.urandom(12)
			socket.sendto(nounce + aes_engine.encrypt(nounce, to_send, None), (addr[0], int(addr[1]) + 1))
		
		time.sleep(0.05)
	
	print('exited broadcast thread.')


def get_loc(socket):
	global RUNNING

	socket.settimeout(10)

	while RUNNING:
		try:
			data, addr = socket.recvfrom(4096)
			data = data.decode('utf-8').split('|')
			ONLINE_USERS[data[0]]['loc'] = data[1]
		except s.timeout:
			pass
	print('exited get loc thread.')


threading.Thread(target=recv, args=(socket_recv, )).start()
threading.Thread(target=server_console, args=()).start()
threading.Thread(target=broadcast, args=(socket_broad, )).start()
threading.Thread(target=get_loc, args=(socket_get_loc, )).start()

