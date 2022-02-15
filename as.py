import sys,os,socket
import re
import pickle
import random
import numpy as np
from GM import * 
threshold = 3
SIZE = 2048
M = 100
template = []
raw_template = ''
res = ['False', 'True']
key = {'pub': (1255268899298437, 227546358779650), 'priv': (19535381, 64256177)}

N = key['pub'][0]

n_changes = 0
raw_template = [0]
#random first version of template
raw_template[0] = np.random.choice(['0', '1'], size=M)

def enc(st):
	return encrypt(st, key['pub'])

def generate_template():
	global template, raw_template, n_changes

	temp = ''.join(raw_template[n_changes])
	encrypted_temp = []
	for i in range(M):
		c_i = enc(temp[i])[0]
		encrypted_temp.append(c_i)

	# encrypted_temp = enc(temp)
	f=open('cipher.txt', 'w+')
	for i in encrypted_temp:
		f.write(str(i) +'\n')
	f.close()
	template.append(encrypted_temp)
	print("TEMPLATE: ", temp, "\nencrypt -> ", encrypted_temp)

generate_template()


def authenticate(fresh_bio, id):
	hw = 0
	hd = [0 for i in range(M)]
	for i in range(M):
		print(fresh_bio[i])
		print(template[id][i])
		#compare to the lastest version of template
		print(len(template))
		print(n_changes)
		hd[i] = (fresh_bio[i]*template[n_changes][i])%N

	for j in range(M):
		hd[j] = decrypt([hd[j]], key['priv'])
	hw = sum(hd)

	if hw < threshold:
		return 1
	else:
		return 0



def update_template():
	global raw_template, n_changes, encrypted_temp

	#from last template, adjust k bits (k<threshold)
	new_template = raw_template[n_changes] 
	for i in range(threshold):
		k = randint(0, M-1)
		print("k =  ", k)
		if new_template[k] == '0':
			new_template[k] = '1'
		else:
			new_template[k] = '0'
	print('new template ', new_template)
	raw_template.append(new_template)

	temp = ''.join(new_template)
	encrypted_temp = []
	for i in range(M):
		c_i = enc(temp[i])[0]
		encrypted_temp.append(c_i)

	template.append(encrypted_temp)

	n_changes +=1



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
n_trial = 0
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
	
	n_trial +=1
	if n_trial == 100:
		update_template()


	print('\nserver response:>', res[response])
	client_socket.send(bytes(str(response),encoding='UTF-8'))
	# else:
	# 	while 1:
	# 		chat = input('server :>')
			# if not chat: break
	# 		client_socket.sendall(bytes(chat+'\n',encoding='UTF-8'))
print("Raw value template' versions " )
for raw in raw_template:
	print(raw)
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
	