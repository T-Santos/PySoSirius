# standard/installed
import requests
from requests.exceptions import ConnectionError, Timeout
import sys

from functools import reduce
from operator import getitem
from datetime import datetime, timedelta
from time import time

# local modules/packages
from .common.exceptions import AttributeNotFoundError 


class SiriusCurrentlyPlaying(object):

    JSON_URI_PREFIX = 'http://www.siriusxm.com/metadata/pdt/en-us/json/channels/'
    JSON_MSG_SUCCESS_CODES = [100,200]

    JSON_ROOT_MSG_DATA_KEYS = {
                                'messages':['channelMetadataResponse','messages'],
                                'song':['channelMetadataResponse','metaData','currentEvent'],
                                'status':['channelMetadataResponse']
                                }

    JSON_MSG_DATA_KEYS = {
                            'album':['song','album','name'],
                            'artist':['artists','name'],
                            'code':['code'],
                            'song':['song','name'],
                            'start':['startTime']
                            }

    @classmethod
    def get_attribute(cls,keys,data):

        try: 
            value = reduce(getitem,keys,data)
            return value
        except KeyError as error:
            message = "Key: " + error.message + " does not exist."
            raise AttributeNotFoundError(message)
        except:
            message = sys.exc_info()[0].__name__ + "  " + sys.exc_info()[1].message
            raise AttributeNotFoundError(message)

    def __init__(self,channel_id):
        super(SiriusCurrentlyPlaying,self).__init__()

        self.id = channel_id
        self.__last_updated = None
        self.data = self.__get_currently_playing()

    def __get_currently_playing(self):
        
        self.last_updated = time()
        try:
            response = requests.get(self._get_url()).json()
        except (ConnectionError,Timeout,ValueError):
            response = {}
        return response

    def _get_url(self):

        timenow = datetime.utcnow().strftime('%m-%d-%H:%M:00')
        urlSuffix = '/timestamp/'+timenow
        url = type(self).JSON_URI_PREFIX + self.id + urlSuffix
        return url

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
    
    @property
    def start(self):
        keys = type(self).JSON_ROOT_MSG_DATA_KEYS['song'] + type(self).JSON_MSG_DATA_KEYS['start']
        return self.currently_playing_item(keys)
    
    @property
    def status(self):
        keys = type(self).JSON_ROOT_MSG_DATA_KEYS['status'] + ['status']
        return self.currently_playing_item(keys)

    def currently_playing_item(self,keys):

        msg_code_keys = type(self).JSON_ROOT_MSG_DATA_KEYS['messages'] + type(self).JSON_MSG_DATA_KEYS['code']

        message = type(self).get_attribute(msg_code_keys,self.data) 

        if message in type(self).JSON_MSG_SUCCESS_CODES:
            return type(self).get_attribute(keys,self.data)
        else:
            return None
