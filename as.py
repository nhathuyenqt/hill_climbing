import sys,os,socket
import re
import numpy as np

threshold = 3
SIZE = 10
n = 10
template = ['','']
res = ['False', 'True']
def authenticate(fresh_bio, id):

	count = 0;
	b = template[id]
	print(template)
	print(b)
	print(fresh_bio)
	print('len fresh ', len(fresh_bio))
	if  len(fresh_bio) < SIZE:
		print(fresh_bio)
	print('len b     ', len(b))

	for i in range(n):
		if b[i] != fresh_bio[i]:

			count = count + 1
	print('count', count)
	if count < threshold:
		return 1
	else:
		return 0


def generate_template():
	global template
	template[0] = np.random.choice(['0', '1'], size=(SIZE))
	# template[0] = '0001000010'
	# test = ['1' '0' '1' '0' '1' '0' '0' '1' '1' '0']
	# template[0] = "".join(test)
	# it = "".join(template[0])
	# template[0] = ['1' '1' '1' '0' '1' '0' '1' '0' '0' '0' '1' '0']
	print("TEMPLATE: ", ''.join(template[0]))

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
	received = client_socket.recv(SIZE).decode()
	print('\nclient :>', received)
	if not received:
		break
	response = authenticate(received, 0)

	print('\nserver response:>', res[response])
	client_socket.sendall(bytes(str(response),encoding='UTF-8'))
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
	