
# Standard packages/modules
from collections import namedtuple

# installed packages/modules

# my pagkages/modules
from .defaults import *

class PySoSirius(object):

	channel_data_wrapper = namedtuple(
							'wrap_channel_data',
							['channel','id','name','url','category','genre','description']
							)

	@classmethod
	def wrap_channel_data(cls,channel_data):

		return cls.channel_data_wrapper(*channel_data)

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

		from .database.manager import SiriusManager
		from .sirius_channel import SiriusChannel

		channels = []
		db_manager = SiriusManager()

		# TODO this For could probably be a lambda or map
		# some sort of one liner
		channel_rows = db_manager.get_channel_rows()
		for channel_row in channel_rows:

			channels.append(SiriusChannel(*channel_row))

		return channels


	def get_channel(self,**kwargs):

		from database.manager import SiriusManager
		from sirius_channel import SiriusChannel

		db_manager = SiriusManager()

		channel_row = db_manager.get_channel_row(**kwargs)
		
		return SiriusChannel(*channel_row)
