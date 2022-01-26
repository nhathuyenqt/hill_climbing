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
# pid = os.fork()

# if (pid):

	# while 1:
	# 	line = s.recv(BUFFER_SIZE)
	# 	print ('server tells :> ', str(line,encoding='UTF-8'))
	# 	if not line:
	# 		break
# else:
c = enc(b_)
bi = ''
while 1:
	bi = '0'*M
	for k in range(M):
		print('check k ', k)
		lamda = c[:k]

		for j in range(M-k):
			lamda = lamda + enc('0')
		print('send lamda ', lamda)
		s.sendall(bytes(lamda,encoding='UTF-8'))
		
		result = s.recv(1).decode()
		if result == REJECTED:
			print("REJECTED")
			break
		else:
			print('ACCEPTED')
		if k == M-1:
			print(" run CENTER SEARCH ATTACK")
			# s.close()
			# break
	print('_______end for________ k = ', k)
	# # t = input('pause :>')
	z = k
	bi = bi[:z] + '1' + bi[z+1:]	#bi[z] = '1'
	if z >= 1:
		for k in range(z-1):
			if k>0:
				lamda = c[:k-1]
			else:
				lamda = ''
			lamda = lamda + enc('0') + c[k+1:z+1] + enc('0')*(M-z-1)

			print('send lamda2 ', lamda)
			s.sendall(bytes(lamda, encoding='UTF-8'))
			result = s.recv(1).decode()
			if result == ACCEPTED:
				print('ACCEPTED')
				bi = bi[:k] + '1' + bi[k+1:]	#bi[k] = '1'
			else:
				print('REJECTED')
		print('_______end for2________')
	print("bi ", bi,  "   z = ", z)
	for k in range(z+1, M):
		print('\nk = ', k)
		if z>0:
			lamda = c[:z-1]
		else:
			lamda = ''
		print('lam ', lamda)
		
		lamda = lamda + enc('0')*(k-z) +c[k]+enc('0')*(M-k-1)
		
		# lamda = '001000000000'
		print('send lamda3 ', lamda)
		s.send(bytes(lamda, encoding='UTF-8'))
		
		result = s.recv(1).decode()
		if result == REJECTED:
			bi = bi[:k] + '1' + bi[k+1:]	#bi[k] = '1'
			print("REJECTED")
		else:
			print('ACCEPTED')
	print('--check while--')
	break
print('bi ', bi)
s.close()