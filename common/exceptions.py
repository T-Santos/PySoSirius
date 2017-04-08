'''
	Handle any exceptions made in PySoSirius
'''

class PySoSiriusError(Exception):
	'''
		base class for all PySoSirius errors
	'''
	pass

class AttributeNotFoundError(PySoSiriusError):
	'''
		raised when there is a key error when a key in the 
		currently playing data store doesnt exist
	'''
	pass