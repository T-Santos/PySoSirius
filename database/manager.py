# Standard
import sqlite3

# installed

# mine

class SiriusManager(object):

	DATABASE_PATH = './pysosirius/database/'
	DATABASE_FILENAME = 'PySoSirius.db'

	"""docstring for SiriusManager"""
	def __init__(self):
		super(SiriusManager, self).__init__()

		self.database_path = type(self).DATABASE_PATH + type(self).DATABASE_FILENAME
		self.connection = sqlite3.connect(self.database_path)
		self.cursor = self.connection.cursor()

		self._create_channel_table()

		def __del__(self):

			self.connection.close()
	
	def _create_channel_table(self):

		# Create table
		try:
			self.cursor.execute(
				'''CREATE TABLE channels
					(channel INTEGER PRIMARY KEY NOT NULL,
					 id TEXT NOT NULL,
					 name TEXT NOT NULL,
					 url TEXT NOT NULL,
					 category TEXT NOT NULL,
					 genre TEXT NOT NULL,
					 description TEXT)''')
		except sqlite3.OperationalError:
			pass	

	def get_channel_rows(self):

		# TODO: look into yield or iterator of sorts
		self.cursor.execute('SELECT * FROM channels')
		return self.cursor.fetchall()
		
	def get_channel_row(
			self,
			channel = None,
			id = None,
			name = None,
			url = None):

		if (not channel and
			not id and
			not name):
			raise ValueError('One of channel, id, name, url is required.')

		if channel:
			self.cursor.execute('SELECT * FROM channels WHERE channel=?',(channel,))
		elif id:
			self.cursor.execute('SELECT * FROM channels WHERE id=?',(id,))
		elif name:
			self.cursor.execute('SELECT * FROM channels WHERE name=?',(name,))
		elif url:
			self.cursor.execute('SELECT * FROM channels WHERE url=?',(url,))

		return self.cursor.fetchone()

	def set_channel_row(self,data):

		# TODO: Raise own exception 
		try:
			self.cursor.execute('INSERT INTO channels VALUES (?,?,?,?,?,?,?)',data)
		except sqlite3.IntegrityError:
			pass

	def save(self):
		self.connection.commit()

	def update_database(self):

		# given a list of channels, see if the rows for those 
		# channels need to be updated or added to the db
		pass
