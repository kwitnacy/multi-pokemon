from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import socket as s
import threading
import os
import json
import time

from users import users
from DBhelper import DBHelperclass
import queries
import DBclases


class Server():
    def __init__(self):
        # self.HOST = s.gethostbyname(s.gethostname())
        self.HOST = '127.0.0.1'
        self.PORT_MAIN = 1337
        self.PORT_GET_LOC = 1401
        self.PORT_SEND_LOC = 1402
        self.FREE_PORTS = [i for i in range(1338, 1401, 1)]
        self.ONLINE_USERS = {}
        self.RUNNING = True
        self.TIMEOUT = 10

        print('SERVER ADDR: ' + self.HOST + ':' + str(self.PORT_MAIN))

        self.sock_main = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.sock_main.bind((self.HOST, self.PORT_MAIN))

        self.sock_send_loc = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.sock_send_loc.bind((self.HOST, self.PORT_SEND_LOC))

        self.sock_get_loc = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.sock_get_loc.bind((self.HOST, self.PORT_GET_LOC))

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.pad = padding.OAEP(mgf=padding.MGF1(hashes.SHA1()), algorithm=hashes.SHA1(), label=None)

        self.thread_main = threading.Thread(target=self.recv_connection, args=())
        self.thread_send_loc = threading.Thread(target=self.send_loc, args=())
        self.thread_get_loc = threading.Thread(target=self.get_loc, args=())
        self.thread_console = threading.Thread(target=self.console, args=())

        self.dbhelper = DBHelperclass()
        self.dbhelper.execute("CREATE DATABASE IF NOT EXISTS pokemon")
        self.dbhelper.change_db("pokemon")

        temp_users = self.dbhelper.fetch("SELECT * FROM Users")
        self.users = { x['user_name']: x for x in temp_users}
        self.log('STARTED Server')

    def start(self):
        self.thread_main.start()
        self.thread_send_loc.start()
        self.thread_get_loc.start()
        self.thread_console.start()


    def close_all(self):
        # TODO:
        # TODO: close all connections
        # TODO: close sockets
        q = queries.Query()
        for row in self.users.values():
            if row['user_ID'] == 0:
                q.insert_no_ID(DBclases.User(row['user_ID'], row['user_name'], row['passwd_hash'], None, None))
        pass


    def log(self, data: str = ''):
        with open('log.pz', 'a') as log_file:
            log_file.write(time.strftime('[%h %d %H:%M:%S') + '] ' + data + '\n')


    def log_send_loc(self, data: str = ''):
        with open('log_send_loc.pz', 'a') as log_file:
            log_file.write(time.strftime('[%h %d %H:%M:%S') + '] ' + data + '\n')


    def send_loc(self):
        while self.RUNNING:
            data = {self.ONLINE_USERS[name]['user_name']: self.ONLINE_USERS[name]['loc'] for name in self.ONLINE_USERS.keys()}
            
            addresses = {name: (self.ONLINE_USERS[name]['ip_addr'], self.ONLINE_USERS[name]['rsa_engine']) for name in self.ONLINE_USERS.keys()}
    
            if data:
                self.log_send_loc(str(data))
    
            to_send = bytes(json.dumps(data), 'utf-8')

            for (addr, rsa_engine) in addresses.values():
                self.sock_send_loc.sendto(rsa_engine.encrypt(to_send, self.pad), (addr[0], 1502))
            
            time.sleep(0.001)


    def get_loc(self):
        self.sock_get_loc.settimeout(self.TIMEOUT)

        while self.RUNNING:
            try:
                data, addr = self.sock_get_loc.recvfrom(4096)
                token = data[:32].decode('utf-8')
                mess = data[33:]
                
                loc = self.private_key.decrypt(mess, self.pad).decode('utf-8')
                self.ONLINE_USERS[token]['loc'] = loc
            except s.timeout:
                pass
        print('exited get loc thread.')
    

    def log_in(self, j, cpk, client_addr):
        # find in database
        try:
            if self.users[j['user_name']]['passwd_hash'] == j['passwd_hash']:
                # user row found
                # get data to variable j/users
                token = os.urandom(16).hex()
                self.log('Login from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + j['user_name'] + ': success :)')
                self.ONLINE_USERS[token] = self.users[j['user_name']]
                self.ONLINE_USERS[token]['ip_addr'] = (client_addr[0], client_addr[1])
                self.ONLINE_USERS[token]['rsa_engine'] = cpk
                self.ONLINE_USERS[token]['token'] = token
                
                return {
                    "status": "OK",
                    "mess": "logged in",
                    "token": token
                }
            else:
                self.log('Login from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + j['user_name'] + ': error :( ')
        except KeyError:
            return {
                "status": "Erorr",
                "mess": "No user"
            }
        
    def log_out(self, j, cpk, client_addr):
        # delete to self.ONLINE_USERS = {}
        # save data to database
        try:
            token = j['token']
        except KeyError:
            return {
                "status": "Error",
                "mess": "No token"
            }
            
        if token in self.ONLINE_USERS:
            self.log('Logout from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + self.ONLINE_USERS[token]['user_name'] + ': succes :)')
            del self.ONLINE_USERS[token]

            return {
                "status": "OK",
                "mess": "logged out"
            }
        else:
            self.log('Logout from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + self.ONLINE_USERS[token]['user_name'] + ': User not logged in :(')
            return {
                "status": "OK",
                "mess": "User not logged in or doesn't exists"
            }


    def sign_in(self, j, cpk, client_addr):
        try:
            if j['user_name'] in self.users:
                self.log('Sign-in from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + j['user_name']
                    + ': name taken, account was not created')

                return {
                    "status": "Error",
                    "mess": "name taken"
                }
            else:
                self.users[j['user_name']] = j
                self.users[j['user_name']]['ip_addr'] = None
                self.users[j['user_name']]['loc'] = None
                self.users[j['user_name']]['user_ID'] = 0
                
                self.log('Sign-in from: ' + str(client_addr[0]) + ':' + str(client_addr[1]) + ', username: ' + j['user_name']
                        + ': accont was created (passwd_hash: ' + j['passwd_hash'] + ')')
                        
                return {
                    "status": "OK",
                    "mess": "singed in"
                }
        except:
            return{
                "status": "Error",
                "mess": "Wrong json"
            }


    # TODO
    def fight(self):
        # get data with who you want to fight
        # check if player is online
        # send to the attacker ip of the attacked player with fight token and seed
        return{
            "status": "Error",
            "mess": "Not implemented yet"
        }


    # TODO
    def fight_result(self):
        # get fight result
        return{
            "status": "Error",
            "mess": "Not implemented yet"
        }


    def session(self, data, addr, free_port):
        session_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        session_socket.bind((self.HOST, free_port))

        # send public key to client
        session_socket.sendto(self.public_key, addr)

        # client public key
        client_pub_key = serialization.load_pem_public_key(data, default_backend())

        # request
        data, addr = session_socket.recvfrom(1024)
        
        data = self.private_key.decrypt(data, self.pad)
        
        d = data.decode('utf-8')[1:]

        j = json.loads(d.replace("'", "\""))
        
        response = {
            'status': 'ERROR',
            'mess': 'wrong byte'
        }

        if data[0] == 0x01:
            response = self.log_in(j, client_pub_key, addr)

        elif data[0] == 0x02:
            response = self.log_out(j, client_pub_key, addr)

        elif data[0] == 0x03:
            response = self.sign_in(j, client_pub_key, addr)
            
        elif data[0] == 0x04:
            response = self.fight()
        
        ct = client_pub_key.encrypt(json.dumps(response).encode('utf-8'), self.pad)

        session_socket.sendto(ct, addr)

        session_socket.close()
        self.FREE_PORTS.append(free_port)
        self.FREE_PORTS.sort()



    def recv_connection(self):
        self.sock_main.settimeout(self.TIMEOUT)

        while self.RUNNING:
            try:
                data, addr = self.sock_main.recvfrom(4096)
                threading.Thread(target=self.session, args=(data, addr, self.FREE_PORTS.pop(), )).start()
            except s.timeout:
                pass

        print('exited recv thread.')


    def console(self):
        commands = ['ousers  	-> prints online users', 
                    'users 		-> print all users', 
                    'quit/close	-> fucks everything up', 
                    'help 		-> help'
                    ]
        
        while self.RUNNING:
            command = input('>>>')
            if command == 'ousers':
                print(self.ONLINE_USERS)
            elif command == 'users':
                print(self.users)
            elif command == 'quit' or command == 'close':
                self.close_all()
                self.RUNNING = False
                break
            elif command == 'help':
                for x in commands:
                    print(x)
            else:
                print('wrong command')
                for x in commands:
                    print(x)
        
        print('exited console thread.')


if __name__ == "__main__":
    server = Server()
    server.start()
