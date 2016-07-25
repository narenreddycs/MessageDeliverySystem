import socket,sys
import threading
from thread import *
import uuid
import message as M

max_conn = 250
buffer_size = 8192
server_port = 8080

def get_id():
	return uuid.uuid1()
	
clients = []

class RecvThread(threading.Thread):

	def __init__(self,conn, handler):
		threading.Thread.__init__(self)
		self.conn = conn
		self.conn.settimeout(1.0)
		self.handler = handler
		self.loop = True
		
	def run(self):
		while(self.loop):
			try:
				reply = self.conn.recv(buffer_size)
				if(len(reply)>0):
					self.handler.on_recv(reply)
				else:
					print "*[*] Client Disconnected - %s"
					self.handler.stop()
					break
			except socket.timeout:
				continue
			except socket.error, (value, message):
				print('Socket Error: ', message)
				handler.stop()
			except KeyboardInterrupt:
				handler.stop()
				
	def stop(self):
		self.loop = False

class ClientStub:
	def __init__(self, conn, addr, id):
		self.conn = conn
		self.addr = addr
		self.id = str(id)
		print('Client Connected- Addr %s; ID %s',(str(addr), str(self.id)))
		self.rt = RecvThread(conn, self)
		self.rt.start()
		self.conn.send(M.IdentityMessage(self.id).to_str())
		
	def stop(self):
		print('Removing Client: ', self.id)
		self.rt.stop
		self.conn.close()
		clients.remove(self)
		
	def on_recv(self,command):
		try:
			print "*[*] Message Received: %s" % command
			msg = command.split(M.COMMAND_SEPARATOR)
			code = int(msg[0])
			if(code == M.Message.ListMCode):
				list = []
				for client in clients:
					list.append(client.id)
				self.send(M.ListMessage(list).to_str())
			elif(code == M.Message.RelayMCode):
				msg = M.RelayMessage(msg[0], msg[1])
				clients_ = []
				for c in clients:
					if c.id in msg.list:
						clients_.append(c)
				for c in clients_:
					c.send(msg.to_str())
				
			else:
				print('Unexpected Input: ',msg)
		except Exception as ex:
			print('On+Recv: ', ex)
	def send(self,msg):
		try:
			self.conn.send(msg)
		except socket.error, (value, message):
			print('Socket Error: ',message)
			self.stop()
		
def start():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('', server_port))
		s.listen(max_conn)
		s.settimeout(1.0)
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
			print(len(clients))
		except socket.timeout:
			continue
		except KeyboardInterrupt:
			print "\n[*] Server Shutting Down ..."
			for c in clients:
				c.stop()
			sys.exit(1)
		except socket.error, (value, message):
			print "\n[*] Server Shutting Down ..."
			for c in clients:
				c.stop()
			break
	s.close()
				
start()