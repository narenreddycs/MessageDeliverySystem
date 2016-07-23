import socket, sys
		 
server_ip = '127.0.0.1'
server_port = 8080
buffer_size = 1024
 
try:
	print("Connecting to Server...\n")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((server_ip, server_port))
	
	while(1):
		msg = s.recv(buffer_size)
		if(len(msg)>0):
			print("*[*] Received Message: %s" % msg)
		else:
			break
	s.close()
except socket.error, (value, message):
	s.close()
	sys.exit(1)
except KeyboardInterrupt:
	s.close()
	sys.exit(1)