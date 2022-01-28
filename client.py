import os,socket,sys
import tqdm
M = 10
N = M
res = ['False', 'True']
REJECTED = '0'
ACCEPTED = '1'
def enc(st):
	return st


b_ = '1'*M

BUFFER_SIZE = 512 

host = 'localhost'
port = 6688

if __name__ == "__main__":

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
	# cipher = '010000010000'
	cipher = '0111001000'

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
		for i in range(N):
			D = inverseB[:i+1] + B[i+1:]
			ct = enc(D)
			s.sendall(bytes(ct ,encoding='UTF-8'))
			result = s.recv(1).decode()
			
			print('ct ', ct)
			if result == REJECTED:
				break
		A = ['' for i in range(N)]
		for i in range(N):
			ct = D[:i] + inverse(D[i]) + D[i+1:]
			s.sendall(bytes(ct ,encoding='UTF-8'))
			result = s.recv(1).decode()
			print('i ', i, ' res ' , res[int(result)])
			if result == REJECTED:
				A[i] = D[i]
			else:
				A[i] = inverse(D[i])
		print(A)


	def hill_climbing_attack(c):
		
		while 1:
			trial = ['0'for i in range(M)]
			for k in range(M-1, -1, -1):
				print('check k ', k)
				lamda = c[:k+1]
				for j in range(M-k-1):
					lamda = lamda + enc('0')
				print('send lamda ', lamda)
				s.sendall(bytes(lamda,encoding='UTF-8'))
				
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
					
					lamda = lamda + enc('0') + c[k+1:z+1] + enc('0')*(M-z-1)

					print('send lamda2 ', lamda)
					s.sendall(bytes(lamda, encoding='UTF-8'))
					result = s.recv(1).decode()
					if result == REJECTED:
						trial[k] = '1'
						print('REJECTED', trial)
					else:
						print('ACCEPTED')

				print('_______end for2________')
			print("trial ", trial,  "   z = ", z)
			for k in range(z+1, M):
				print('\nk = ', k)
				lamda = c[:z]
				
				print('lam ', lamda)
				
				lamda = lamda + enc('0')*(k-z) +c[k]+enc('0')*(M-k-1)
				
				# lamda = '001000000000'
				print('send lamda3 ', lamda)
				s.send(bytes(lamda, encoding='UTF-8'))
				
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