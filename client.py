import os,socket,sys
import tqdm
M = 12
REJECTED = '0'
ACCEPTED = '1'
def enc(st):
	return st




b_ = '1'*M


BUFFER_SIZE = 512 

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

# if (pid):

	# while 1:
	# 	line = s.recv(BUFFER_SIZE)
	# 	print ('server tells :> ', str(line,encoding='UTF-8'))
	# 	if not line:
	# 		break
# else:
c = enc(b_)
while 1:
	bi = '0'*M
	for k in range(M):
		lamda = c[:k]
		for j in range(M-k):
			lamda = lamda + enc('0')
		print('lamda ', lamda)
		s.sendall(bytes(lamda,encoding='UTF-8'))
		
		result = s.recv(1).decode()
		print("  -> ", result)
		if result == REJECTED:
			print("REJECTED")
			break
		if k == M-1:
			print(" run CENTER SEARCH ATTACK")
			# s.close()
			# break
	print('________________ k = ', k)
	t = input('pause :>')
	z = k
	bi = bi[:z] + '1' + bi[z+1:]	#bi[z] = '1'
	if z >= 1:
		for k in range(1, z-1):
			lamda = c[z-1]
			for j in range(M-k):
				lamda = lamda + enc('0')
			print('lamda2 ', lamda)
			s.sendall(bytes(lamda, encoding='UTF-8'))
			result = s.recv(1).decode()
			if result == ACCEPTED:
				bi = bi[:k] + '1' + bi[k+1:]	#bi[k] = '1'

	for k in range(z+1, M):
		lamda = c[:z]
		for j in range(z, k):
			lamda = lamda + enc('0')
		lamda = lamda + c[k]
		for j in range(M-k):
			lamda = lamda + enc('0')
		print('lamda3 ', lamda)
		s.sendall(bytes(lamda,encoding='UTF-8'))
		
		result = s.recv(1).decode()
		if result == REJECTED:
			bi = bi[:k] + '1' + bi[k+1:]	#bi[k] = '1'
s.close()