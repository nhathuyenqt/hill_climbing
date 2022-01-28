import sys,os,socket
import tqdm
import re
import numpy as np
threshold = 10
SIZE = 512
n = 10
def authenticate(fresh_bio, id):
	count = 0;
	b = template[id]
	for i in range(len(b)):
		if b[i] != fresh_bio[i]:
			count += 1

	if count < threshold:
		return 0
	else:
		return 1


def generate_template:
	
	template[0] = np.random.choice([0, 1], size=(SIZE))
	

BUFFER_SIZE = 512


server_host = 'localhost'
server_port = 6688
# socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((server_host, server_port))
s.listen(socket.SOMAXCONN)
print(f"[*] Listening as {server_host}:{server_port}")

while 1:
	(client_socket, address) = s.accept()
	print(f"[+] {address} is connected.")
	client_socket.sendall(b'Bienvenu\n')
	pid = os.fork()
	if (pid) :
		while 1:
			print("Hello\n")
			received = client_socket.recv(BUFFER_SIZE).decode()
			print(received)
	else:
		while 1:
			chat = input('client :>')
			if not chat: break
			client_socket.sendall(bytes(chat+'\n',encoding='UTF-8'))

	client_socket.close()
		# while 1:
		# 	line = new_connection.recv(1000)
		# 	print ("<:", str(line,encoding='UTF-8'))
		# 	if not line: break
	# else:
	# 	while 1:
	# 		clavier = input(':>')
	# 		if not clavier: break
	# 		new_connection.sendall(bytes(clavier, encoding='UTF-8'))
	# new_connection.close()
#

import os,socket,sys
import tqdm

BUFFER_SIZE = 512 

filesize = os.path.getsize(filename)

host = 'localhost'
port = 6688
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)


try:
	print(f"[+] Connecting to {host}:{port}")
	s.connect((host, port))
except:
	print ("problem of connection")
	sys.exit(1)
pid = os.fork()

if (pid):
	while 1:
		line = s.recv(1000)
		print (str(line,encoding='UTF-8'))
		if not line:
			break
else:
	while 1:
		chat = input('client :>')
		if not chat: break
		s.sendall(bytes(chat+'\n',encoding='UTF-8'))

s.close()