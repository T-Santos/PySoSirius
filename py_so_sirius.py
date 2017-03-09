#import sqlite3

# Standard packages/modules

# installed packages/modules

# my pagkages/modules
from defaults import *
#from sirius_channel import SiriusChannel

class PySoSirius(object):

	"""docstring for PSS"""
	def __init__(self,*args,**kwargs):
		# PY3 super().__init__(*args,**kwargs)
		super(PySoSirius,self).__init__(*args,**kwargs)

		self.channels = []

		if 'database' in kwargs.keys():
			self.database = kwargs['database']
		else:
			self.database = DATABASE
		
		if 'genres' in kwargs.keys():
			self.genres = kwargs['genres']
		else:
			self.genres = LIMIT_TO_GENRES

		if 'categories' in kwargs.keys():
			self.categories = kwargs['categories']
		else:
			self.categories = LIMIT_TO_CATEGORIES

		if 'channels' in kwargs.keys():
			self.channels = kwarg['channels']
		else:
			self.channels = LIMIT_TO_CHANNELS
	'''
		# Handle DB level init stuff
		if self.database:
			self.db_connex = sqlite3.connect(self.database)
			self.db_conn_cursor = self.db_connex.cursor()
		# TODO: Need to have a DB Init to build local tables
		# for shit

	def __del__(self,**kwargs):
		super().__del__(kwargs)

		if self.database:
			self.db_conn_cursor.close()
	'''
	
	def get_channels(self):

		# This will hit the db to get all rows in the table
		# and create a SeriusChannel object and return the 
		# sorted list of SeriusChannel object instances

		return []

	def get_channel(
		self,
		channel = None,
		channel_name = None,
		channel_id = None):
		
		# This will return one SeriusChannel instance

		return None
