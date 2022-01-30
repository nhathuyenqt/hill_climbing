import sys,os,socket
import re
import pickle
import numpy as np
from GM import * 
threshold = 3
SIZE = 1024
M = 10
template = ['','']
res = ['False', 'True']
key = {'pub': (1255268899298437, 227546358779650), 'priv': (19535381, 64256177)}

N = key['pub'][0]

def enc(st):
	return encrypt(st, key['pub'])

def authenticate(fresh_bio, id):
	hw = 0
	# for j in fresh_bio:
	# 	print(decrypt([j], key['priv']), end='')
	# print()
	# for j in template[id]:
	# 	print(decrypt([j], key['priv']), end='')
	# print()
	hd = [0 for i in range(M)]
	for i in range(M):
		hd[i] = (fresh_bio[i]*template[id][i])%N

	for j in range(M):
		hd[j] = decrypt([hd[j]], key['priv'])
	hw = sum(hd)

	# print("E(b) x E(b')", hw)
	# count = decrypt([hw[0]], key['priv'])
	# print('count ', count)

	# b = template[id]
	# print(template)
	# print(b)
	# print(fresh_bio)
	# print('len fresh ', len(fresh_bio))
	# if  len(fresh_bio) < n:
	# 	print(fresh_bio)
	# print('len b     ', len(b))

	# for i in range(n):
	# 	if b[i] != fresh_bio[i]:

	# 		count = count + 1
	# print('count', count)
	if hw < threshold:
		return 1
	else:
		return 0

def generate_template():
	global template
	template[0] = np.random.choice(['0', '1'], size=M)
	# template[0] = '0001000010'
	template[0] = ['1' '0' '1' '0' '1' '0' '0' '1' '1' '0']
	# template[0] = "".join(test)
	# it = "".join(template[0])
	# template[0] = ['1' '1' '1' '0' '1' '0' '1' '0' '0' '0' '1' '0']
	temp = ''.join(template[0])
	encrypted_temp = []
	for i in range(M):
		c_i = enc(temp[i])[0]
		encrypted_temp.append(c_i)

	# encrypted_temp = enc(temp)
	f=open('cipher.txt', 'w+')
	for i in encrypted_temp:
		f.write(str(i) +'\n')
	f.close()
	template[0] = encrypted_temp
	print("TEMPLATE: ", temp, "\nencrypt -> ", encrypted_temp)


generate_template()

server_host = 'localhost'
server_port = 6688
# socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((server_host, server_port))
s.listen(socket.SOMAXCONN)

# while 1:
(client_socket, address) = s.accept()
# pid = os.fork()
# if (pid) :
while 1:
	received = client_socket.recv(SIZE).decode('UTF-8')
	# data = pickle.loads(received)

	if not received:
		break
	data = received[:-1]
	data = data[1:]
	data = data.split(",")
	data = [int(st) for st in data]
	print('\nclient :>', data)

	response = authenticate(data, 0)
	print('\nserver response:>', res[response])
	client_socket.send(bytes(str(response),encoding='UTF-8'))
	# else:
	# 	while 1:
	# 		chat = input('server :>')
			# if not chat: break
	# 		client_socket.sendall(bytes(chat+'\n',encoding='UTF-8'))

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
	