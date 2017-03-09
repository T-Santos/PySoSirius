# standard/installed
import requests
from functools import reduce
from operator import getitem
from datetime import datetime, timedelta


class SiriusCurrentlyPlaying(object):

	JSON_URI_PREFIX = 'http://www.siriusxm.com/metadata/pdt/en-us/json/channels/'

	JSON_MSG_CODE_KEYS = ['channelMetadataResponse','messages','code']
	JSON_MSG_SUCCESS_CODES = [100,200]

	JSON_ARTIST_NAME_KEYS = ['channelMetadataResponse','metaData','currentEvent','artists','name']
	JSON_SONG_NAME_KEYS = ['channelMetadataResponse','metaData','currentEvent','song','name']
	JSON_ALBUMN_KEYS = ['channelMetadataResponse','metaData','currentEvent','song','album','name']

	def __init__(self,channel_id):
		super(SiriusCurrentlyPlaying,self).__init__()


		self.data = self.__get_currently_playing(channel_id)

	def __get_currently_playing(self,channel_id):

		timenow = (datetime.utcnow() - timedelta(minutes=1)).strftime('%m-%d-%H:%M:00')
		urlSuffix = '/timestamp/'+timenow
		url = type(self).JSON_URI_PREFIX + channel_id + urlSuffix
		return requests.get(url).json()

	@property
	def artist_name(self):
		return self.currently_playing_item(type(self).JSON_ARTIST_NAME_KEYS)

	@property
	def song_name(self):
		return self.currently_playing_item(type(self).JSON_SONG_NAME_KEYS)
	
	@property
	def albumn(self):
		return self.currently_playing_item(type(self).JSON_ALBUMN_KEYS)

	# TODO: change this to __getitem__ or overload/subclass it somehow
	# or catch the key exception and raise my own
	def currently_playing_item(self,keys):

		# TODO: some items have issues on their return values
		# DR DRE: albumn 2001 song: forgot about dre has issues since its an int 2001
		# other international channels have issues with unicode values

		message = reduce(getitem,type(self).JSON_MSG_CODE_KEYS,self.data) 

		if message in type(self).JSON_MSG_SUCCESS_CODES:
			return reduce(getitem,keys,self.data)
		else:
			print(message)
			return None