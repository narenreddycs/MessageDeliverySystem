#from enum import Enum

#Message Formats:
#0:<id>
#1:<id1>,<id2>,<id3>
#2:<msg>|<id1>,<id2>

COMMAND_SEPARATOR = ':'
LIST_SEPARATOR = ','
MSG_SEPARATOR = '|'
	
class Message(object):

	def __init__(self, mId):
		self.mId = mId
		
	def to_str(self):
		return '%s%s%s'%(self.mId, COMMAND_SEPARATOR, self.payload())
		
	#To Be Implemented by Child Classes...
	def payload(self):
		return ''
	
class IdentityMessage(Message):
	def __init__(self, id):
		self.id = id
		super(IdentityMessage, self).__init__(0)
		
	def payload(self):
		return self.id
		
class ListMessage(Message):
	def __init__(self, id_list):
		self.list = id_list
		super(ListMessage, self).__init__(1)
	
	def payload(self):
		return LIST_SEPARATOR.join(self.list)

class RelayMessage(Message):
	def __init__(self, msg, list):
		self.msg = msg
		self.list = list
		super(RelayMessage, self).__init__(2)
		
	def payload(self):
		return MSG_SEPARATOR.join([self.msg, LIST_SEPARATOR.join(self.list)])