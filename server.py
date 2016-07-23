import socket,sys
from thread import *
import uuid
import message as M

max_conn = 100
buffer_size = 8192
server_port = 8080

def get_id():
	return uuid.uuid1()
	
clients = []

class ClientStub:
	def __init__(self, conn, addr, id):
		self.conn = conn
		self.addr = addr
		self.id = id
		print('Client Connected- Addr %s; ID %s',(str(addr), str(self.id)))
		start_new_thread(self.recv, ())
		self.conn.send(M.IdentityMessage(self.id).to_str())
		
	def recv(self):
		while(1):
			try:
				reply = self.conn.recv(buffer_size)
				if(len(reply)>0):
					print "*[*] Message Received: %s" % reply
				else:
					print "*[*] Cliend Disconnected - %s" % str(id)
					self.conn.close()
					clients.remove(self)
					break
			except KeyboardInterrupt:
				self.conn.close()
				sys.exit(1)
				#print "\n[*] Server Shutting Down ..."
	def send(msg):
		conn.send(msg)
		
def start():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('', server_port))
		s.listen(max_conn)
		print "[*] Initializing Sockets... Done"
		print "[*] Sockets Binded Successfully ..."
		print("[*] Server Started Successfully [%d]]\n" % server_port)
	except Exception, e:
		print "[*] Unable to initialize Socket"
		sys.exit(2)
		
	while(1):
		try:
			conn, addr = s.accept()
			client = ClientStub(conn, addr, get_id())
			clients.append(client)
		except KeyboardInterrupt:
			s.close()
			print "\n[*] Server Shutting Down ..."
			sys.exit(1)
	s.close()
				
start()