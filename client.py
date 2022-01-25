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