import os,socket,sys
import tqdm
import pickle
from GM import * 
M = 100

res = ['False', 'True']
REJECTED = '0'
ACCEPTED = '1'
key = {'pub': (1255268899298437, 227546358779650), 'priv': (19535381, 64256177)}

def enc(st):	
	encr = []
	for i in st:
		d = encrypt(i, key['pub'])[0]
		encr.append(d)
	print(encr)
	return encr
	

b_ = '1'*M

BUFFER_SIZE = 1024

host = 'localhost'
port = 6688


if __name__ == "__main__":

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BUFFER_SIZE)

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
	# cipher = '010000010000'
	f = open('cipher.txt', 'r+')
	
	cipher = [line.rstrip('\n') for line in f.readlines()]
	cipher = [int(line) for line in cipher]
	print('cipher ',cipher)
	f.close()

	def inverse(Y):
		inverseY = ''
		for i in Y:
			if i == '0':
				inverseY = inverseY + '1'
			else:
				inverseY = inverseY + '0'
		return inverseY

	def center_search_attack(B):
		inverseB = inverse(B)
		D = ''
		for i in range(M):
			D = inverseB[:i+1] + B[i+1:]
			ct = enc(D)
			# print("cipher ", ct)
			data = str(ct)
			s.sendall(bytes(data ,encoding='UTF-8'))
			result = s.recv(1).decode()
			
			# print('ct ', ct)
			if result == REJECTED:
				break
		A = ['' for i in range(M)]
		for i in range(M):
			ct = D[:i] + inverse(D[i]) + D[i+1:]
			ct = enc(ct)
			# print("cipher2 ", ct)
			data = str(ct)
			s.sendall(bytes(data ,encoding='UTF-8'))
			result = s.recv(1).decode()
			# print('i ', i, ' res ' , res[int(result)])
			if result == REJECTED:
				A[i] = D[i]
			else:
				A[i] = inverse(D[i])
		print("Recovered result", A)


	def hill_climbing_attack(c):
		
		while 1:
			trial = ['0' for i in range(M)]
			for k in range(M-1, -1, -1):
				lamda = c[:k+1]

				for j in range(M-k-1):
					zero = enc('0')[0]
					print('zero ', zero)
					lamda.append(zero)
					
				print('send lamda ', lamda)
				data = str(lamda)
				# lamda = [str(dt) for dt in lamda]
				# data=pickle.dumps(lamda)
				# print(sys.getsizeof(data))
				s.sendall(bytes(data, encoding='UTF-8'))
				result = s.recv(1).decode()
				if result == REJECTED:
					print("REJECTED")
					break
				else:
					print('ACCEPTED')
				if k == 0:
					trial = ''.join(trial)
					print(" run CENTER SEARCH ATTACK")
					return center_search_attack(trial)
					# s.close()
					# break
			print('_______end for________ k = ', k)
			# # t = input('pause :>')
			z = k+1
			trial[z] = '1'
			print('z = ', z, " current bi : ", trial)
			if z >= 1:
				for k in range(z):
					print('k = ', k)
					lamda = c[:k]
					zero = enc('0')[0]
					lamda.append(zero)
					for j in range(k+1,z+1):
						lamda.append(c[j])
					for j in range(M-z-1):
						# zero = enc('0')[0]
						lamda.append(zero)
					print('send lamda2 ', lamda)
					data = str(lamda)
					s.sendall(bytes(data, encoding='UTF-8'))
					result = s.recv(1).decode()
					if result == REJECTED:
						trial[k] = '1'
						print('REJECTED', trial)
					else:
						print('ACCEPTED')

				print('_______end for2________')
			print("trial ", trial,  "   z = ", z)
			zero = enc('0')[0]
			for k in range(z+1, M):
				print('\nk = ', k)
				lamda = c[:z]
				print('lam ', lamda)
				for j in range(k-z):
					lamda.append(zero)
				lamda.append(c[k])
				for j in range(M-k-1):
					lamda.append(zero)
				
				# lamda = '001000000000'
				print('send lamda3 ', lamda)
				data = str(lamda)
				s.send(bytes(data, encoding='UTF-8'))
				
				result = s.recv(1).decode()
				if result == ACCEPTED:
					trial[k] = '1'
					print('ACCEPTED')
				else:
					print("REJECTED")
			print('--check while--')
			break
		print('Recovered bi ', trial)
		s.close()




	hill_climbing_attack(cipher)