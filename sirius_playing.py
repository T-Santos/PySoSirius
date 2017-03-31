# standard/installed
import requests
from functools import reduce
from operator import getitem
from datetime import datetime, timedelta
from time import time


class SiriusCurrentlyPlaying(object):

	JSON_URI_PREFIX = 'http://www.siriusxm.com/metadata/pdt/en-us/json/channels/'
	JSON_MSG_SUCCESS_CODES = [100,200]

	JSON_ROOT_MSG_DATA_KEYS = {
								'messages':['channelMetadataResponse','messages'],
								'song':['channelMetadataResponse','metaData','currentEvent'],
		}

	JSON_MSG_DATA_KEYS = {
							'album':['song','album','name'],
							'artist':['artists','name'],
							'code':['code'],
							'song':['song','name'],
	}

	def __init__(self,channel_id):
		super(SiriusCurrentlyPlaying,self).__init__()

		self.id = channel_id
		self.__last_updated = None
		self.data = self.__get_currently_playing()

	def __get_currently_playing(self):

		# TODO make sure this is the correct way to get UTC time
		timenow = (datetime.utcnow() - timedelta(minutes=1)).strftime('%m-%d-%H:%M:00')
		urlSuffix = '/timestamp/'+timenow
		url = type(self).JSON_URI_PREFIX + self.id + urlSuffix

		self.last_updated = time()
		return requests.get(url).json()

	def update(self):

		# dont want to overload XM's servers, only ping every minute
		# they tend to update currently playing on their site as well.
 		if not ((time() - self.last_updated) < 60):
			self.data = self.__get_currently_playing()

	@property
	def artist_name(self):
		keys = type(self).JSON_ROOT_MSG_DATA_KEYS['song'] + type(self).JSON_MSG_DATA_KEYS['artist']
		return self.currently_playing_item(keys)

	@property
	def song_name(self):
		keys = type(self).JSON_ROOT_MSG_DATA_KEYS['song'] + type(self).JSON_MSG_DATA_KEYS['song']
		return self.currently_playing_item(keys)
	
	@property
	def album(self):
		keys = type(self).JSON_ROOT_MSG_DATA_KEYS['song'] + type(self).JSON_MSG_DATA_KEYS['album']
		return self.currently_playing_item(keys)

	# TODO: change this to __getitem__ or overload/subclass it somehow
	# or catch the key exception and raise my own
	def currently_playing_item(self,keys):

		# TODO: some items have issues on their return values
		# DR DRE: albumn 2001 song: forgot about dre has issues since its an int 2001
		# other international channels have issues with unicode values
		msg_code_keys = type(self).JSON_ROOT_MSG_DATA_KEYS['messages'] + type(self).JSON_MSG_DATA_KEYS['code']

		message = reduce(getitem,msg_code_keys,self.data) 

		if message in type(self).JSON_MSG_SUCCESS_CODES:
			return reduce(getitem,keys,self.data)
		else:
			print(message)
			return None