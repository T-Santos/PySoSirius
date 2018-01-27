# standard

# installed

# my
from .sirius_playing import SiriusCurrentlyPlaying

class SiriusChannel(object):

	"""docstring for Channel"""
	def __init__(
			self,
			channel,
			id,
			name,
			url,
			category= None,
			genre = None,
			description = None,
			*args,
			**kwargs):
		# PY3 super().__init__(*args,**kwargs)
		super(SiriusChannel,self).__init__()
		
		self.channel = channel
		self.name = name
		self.url = url
		self.id = id

		self.category = category
		self.genre = genre
		self.description = description

		self.currently_playing = None

	def PrintMe(self):

		print('Channel:' + str(self.channel))
		print('\t' + 'ID: ' + str(self.id))
		print('\t' + 'Name: ' + str(self.name))
		print('\t' + 'URL: ' + str(self.url))
		print('\t' + 'Category: ' + str(self.category))
		print('\t' + 'Genre: ' + str(self.genre))
		print('\t' + 'Description: ' + str(self.description))

	def get_currently_playing(self):

		if not self.currently_playing:
			self.currently_playing = SiriusCurrentlyPlaying(self.id)
		else:
			self.currently_playing.update()

		return self.currently_playing
		


