
# Standard packages/modules
import requests
from collections import namedtuple

# installed packages/modules
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# my pagkages/modules

class SiriusScraper(object):

	"""docstring for Scraper"""
	
	# TODO: Maybe have named tuple to manage the channeldata fromt he table
	ROOT_URL = 'http://www.siriusxm.com/'
	URL_FOR_COOKIE = ROOT_URL
	URI_ALL_CHANNELS = 'http://www.siriusxm.com/channellineup/'
	CHANNEL_TABLE_ID = 'packageChannelsTable'

	CHANNEL_INTERNAL_ID_VAR = 'SXM.ChannelContentID = '

	SIRIUS_CHANNEL_NUMBER_MAP = {714: ('Indie1.0','Indie 1.0')}

	@classmethod
	def get_channel_id(cls,url):

		page = requests.get(url).text
		soup = BeautifulSoup(page,'html.parser')

		scripts = soup.findAll('script')
		for script in scripts:
			scriptString = script.string
			if scriptString:
				found = scriptString.find(cls.CHANNEL_INTERNAL_ID_VAR)
				if found > -1:
					start = found + len(cls.CHANNEL_INTERNAL_ID_VAR)
					end = scriptString.find(";",start)
					return scriptString[start:end][1:-1]
		return None

	def __init__(self):
		super(SiriusScraper, self).__init__()

		# TODO: might want to use PhantomJs
		self.browser = webdriver.Firefox()

		# open browser to bogus url for website
		self.browser.get(type(self).URL_FOR_COOKIE)

		# set the platform choice cookie on bogus page
		cookie = {'name' : "sxm_platform", 'value' : 'sirius'}
		self.browser.add_cookie(cookie)
		cookie = {'name' : "sxm_radio", 'value' : 'YMM|2012|Nissan|Sentra'}
		self.browser.add_cookie(cookie)
		
		# now nav to the all channels page for scraping
		self.browser.get(type(self).URI_ALL_CHANNELS)

		self._channel_table = self.browser.find_element_by_id(type(self).CHANNEL_TABLE_ID)

	def get_channel_data(
		self,
		channel = None,
		channel_name = None):

		if (not channel and
			not channel_name):
			raise ValueError('One of channel,channel_name is required.')

		if channel:
			source = self._get_channel_page_source(
				channel_id_type = 'channelnum',
				channel_id = channel)
		elif channel_name:
			source = self._get_channel_page_source(
				channel_id_type = 'channelname',
				channel_id = channel_name)
			
		# TODO: Raise exception
		if source:
			return self._get_channel_data_from_page_source(source)
		else:
			return None

	def get_channels_data(self):

		# temp unsorted list of Channel object instances
		channels_data = []

		for row in self._channel_table.find_elements_by_tag_name('tr'):

			cell_values = self._get_channel_data_from_page_source(row)

			if cell_values:
				channels_data.append(cell_values)

		# need to cast to int otherwise we get order like 1,10,2,20,3 
		# instead of 1,2,3,10,20
		return sorted(channels_data, key=lambda c: int(c[0]))

	def _get_channel_page_source(
		self,
		channel_id_type,
		channel_id):

		# TODO: Maube catch exception selenium.common.exceptions.NoSuchElementException
		# if the item doesnt exist and raise my own

		if channel_id_type == 'channelnum':
			return self._channel_table.find_element_by_xpath(
				'//span[@class="channelnum" and contains(text(), "{0}")]'.format(
					str(channel_id))).find_element_by_xpath('../../..')
		elif channel_id_type == 'channelname':

			channel_name_cells = self._channel_table.find_elements_by_class_name('channelname')

			if channel_name_cells:

				for channel_name_cell in channel_name_cells:

					try:
						link = channel_name_cell.find_element_by_link_text(
							channel_id).find_element_by_xpath(
								'../..')

						return link
					except NoSuchElementException:
						pass
		return None

	def _get_channel_data_from_page_source(self,page_source):

		channel_data = None
		cells = page_source.find_elements_by_tag_name('td')

		if cells:
			# TODO: make sure we make use of the named tuple here instead
			cell_channel_number = 0
			cell_channel_name = 1
			cell_channel_category = 2
			cell_channel_genre = 3
			cell_channel_desc = 4

			channel_number = int(cells[cell_channel_number].text.encode('ascii','ignore'))
			channel_name = cells[cell_channel_name].text.encode('ascii','ignore')

			# known SiriusXM Channel URL bugs
			# ensure number and name is correct
			if (channel_number in type(self).SIRIUS_CHANNEL_NUMBER_MAP
				and channel_name == type(self).SIRIUS_CHANNEL_NUMBER_MAP[channel_number][1]):
				url = type(self).ROOT_URL+type(self).SIRIUS_CHANNEL_NUMBER_MAP[channel_number][0]
			else:
				url = cells[cell_channel_number].find_element_by_tag_name('a').get_attribute('href')

			channel_data = (channel_number,
				 			type(self).get_channel_id(url),
							channel_name,
							url,
							cells[cell_channel_category].text.encode('ascii','ignore'),
							cells[cell_channel_genre].text.encode('ascii','ignore'),
							cells[cell_channel_desc].text.encode('ascii','ignore'))

		return channel_data