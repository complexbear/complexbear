''' Interface classes for talking to complexbear database
'''
import logging
import MySQLdb
from datetime import datetime

logger = logging.getLogger(__name__)

def connect():
	conn = MySQLdb.connect(user='matt',db='complexbear',host='plug')
	cursor = conn.cursor()
	logger.info('DB connected')
	return cursor
	

# Static initialization
cursor = None
	
class Label(object):
	def __init__(self, id, name):
		self.id = id
		self.name = name
		
	def __str__(self):
		return '(ID:%s, Name:%s)' %(self.id,self.name)
	
	def __repr__(self):
		return self.__str__()
	
	@classmethod		
	def create(cls, name):
		if not Label.exists(name):
			sql = 'INSERT INTO labels (name) VALUES (%s)' 
			cursor.execute(sql, (name,))			
		return Label.getId(name)
	
	@classmethod
	def getId(cls, name):
		sql = 'SELECT id FROM labels WHERE name = %s'
		rsp = cursor.execute(sql, (name,))
		if rsp == 0:
			return None
		return cursor.fetchone()[0]
	
	@classmethod
	def getName(cls, id):
		sql = 'SELECT name FROM labels WHERE id = %s'
		rsp = cursor.execute(sql, (id,))
		if rsp == 0:
			return None
		return cursor.fetchone()[0]
	
	@classmethod
	def all(cls):
		sql = 'SELECT * FROM labels'
		rsp = cursor.execute(sql)
		if rsp == 0: return []
		labels = cursor.fetchall()
		return [Label(i,n) for i,n in labels]
	
	@classmethod
	def exists(cls, name):
		sql = 'SELECT COUNT(*) FROM labels WHERE name = %s' 
		rsp = cursor.execute(sql, (name,))
		return rsp != 0 and cursor.fetchone()[0] != 0
	
	
class PostLabels(object):
	def __init__(self, postId):
		self.id = postId
		self.labels = []
		self._load()
		
	def __str__(self):
		return '(%s %s)' %(self.id,self.labels)
	
	def __repr__(self):
		return self.__str__()
		
	def _load(self):
		self.labels = []
		sql = 'SELECT labelId FROM postLabels WHERE postId = %s' 
		rsp = cursor.execute(sql, (self.id))
		if rsp != 0:
			labelIds = cursor.fetchall()
			self.labels = list(zip(*labelIds)[0])
		
	def add(self, name):
		# Does the label already exist?
		labelId = Label.getId(name)
		if not labelId:
			labelId = Label.create(name)
		sql = 'INSERT INTO postLabels (postId, labelId) VALUES (%s, %s)'
		rsp = cursor.execute(sql, (self.id, labelId))
		if rsp != 0:
			self.labels.append(name)
			
	def __iter__(self):
		for l in self.labels:
			yield l
			
	
class Post(object):
	def __init__(self, id, msg, user, timestamp):
		self.id = id
		self.labels = PostLabels(id)
		self.msg = msg
		self.user = user
		self.timestamp = timestamp
		if not User.exists(user): raise Exception('user %s does not exist' %user)		

	def __str__(self):
		return 'Post(id=%s, user=%s, created=%s' %(self.id,self.user,self.timestamp)

	def __repr__(self):
		return self.__str__()
	
	@classmethod
	def create(cls, msg, user):
		# Create a post
		if not User.exists(user): raise Exception('user %s does not exist' %user)
		sql = 'INSERT INTO posts (msg,user,timestamp) VALUES (%s,%s,%s)'
		rsp = cursor.execute(sql, (msg,user,datetime.now()))
		if rsp == 0: raise Exception('failed to create post for user %s' %user)
		sql = 'SELECT id,msg,user,timestamp FROM posts WHERE id=MAX(id)'
		rsp = cursor.execute(sql)
		return Post(*cursor.fetchone()[0])
		

	@classmethod
	def get(cls, id):
		sql = 'SELECT msg,user,timestamp FROM posts WHERE id = %s'
		rsp = cursor.execute(sql, (id,))
		if rsp == 0: return None
		return Post(*cursor.fetchone()[0])
	
	@classmethod
	def all(cls):
		sql = 'SELECT id,msg,user,timestamp FROM posts'
		rsp = cursor.execute(sql)
		if rsp == 0: return []
		return [Post(*x) for x in cursor.fetchall()]
	
	
class User(object):
	def __init__(self,name,ro):
		self.name = name
		self.ro = ro
		
	def __str__(self):
		return '(Name:%s, ReadOnly:%s)' %(self.name, self.ro)
	
	def __repr__(self):
		return self.__str__()
	
	@classmethod
	def create(cls, name, ro=True):
		ro = 1 if ro else 0
		sql = 'INSERT INTO users (name, readOnly) VALUES (%s, %s)'
		rsp = cursor.execute(sql, (name,ro))
		if rsp == 0: raise Exception('Failed to create User: %s, %s' %(name,ro))
		return User(name, ro)
		
	@classmethod
	def get(cls, name=None):
		if name is None: return Users.all()
		sql = 'SELECT * FROM users WHERE name = %s' %name
		rsp = cursor.execute(sql)
		if rsp == 0: return None
		return User(*cursor.fetchone()[0])
	
	@classmethod
	def exists(cls, name):
		sql = 'SELECT COUNT(*) FROM users WHERE name = %s'
		rsp = cursor.execute(sql, (name,))
		return rsp != 0 and cursor.fetchone()[0] != 0
	
	@classmethod
	def all(cls):
		sql = 'SELECT * FROM users'
		rsp = cursor.execute(sql)
		if rsp == 0: return []
		users = cursor.fetchall()
		return [User(name,ro) for name,ro in users]
