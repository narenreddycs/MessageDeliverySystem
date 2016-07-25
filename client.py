'''
Client sends messages to the server -

Client:
Enter Command: <1> for List the connected clients, <2> to relay message to selected clients
'''

from thread import *
import threading
import socket, sys
from message import *

server_ip = '127.0.0.1'
server_port = 8080
buffer_size = 1024

class RecvThread(threading.Thread):
	def __init__(self, s):
		threading.Thread.__init__(self)
		self.loop = True
		self.s = s
		self.s.settimeout(1.0)
		
	def run(self):
		while(self.loop):
			try:
				msg = self.s.recv(buffer_size)
				if(len(msg)>0):
					print("\n*[*] Received Message: %s" % msg)
				else:
					break
			except socket.timeout:
				continue
			except socket.error as ex:
				print('Recv Error: ', ex)
				self.exit()
				
	def exit(self):
		print('Exiting Recv Thread..')
		self.loop = False
		
def send_to_server(msg):
	s.send(msg)

class InputThread(threading.Thread):
	def __init__(self, threads):
		threading.Thread.__init__(self)
		self.loop = True
		self.threads = threads
		
	def run(self):
		try:
			while(self.loop):
				response = int(raw_input("\nEnter any command: "))
				if(response == -1):
					print('Exiting...')
					for thread in self.threads:
						thread.exit()
					self.loop = False
				elif(response == Message.ListMCode):
					send_to_server(str(response))
				elif(response == Message.RelayMCode):
					response1 = raw_input("\nEnter the relay message: ")
					response2 = raw_input('\nENter the Client ID\'s separated by ",": ')
					send_to_server(RelayMessage(response1, response2).to_str())
				else:
					print('Unexpected Input ', response)
		except Exception as ex:
			print(ex)
			for thread in self.threads:
				thread.exit()
try:
	print("Connecting to Server...\n")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((server_ip, server_port))
	rt = RecvThread(s)
	it = InputThread([rt])
	rt.start()
	it.start()
	rt.join()
except socket.error, (value, message):
	print(message)
s.close()	
