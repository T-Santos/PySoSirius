from setuptools import setup, find_packages

setup(
	name='pysosirius',
	version='0.0.9',
	description='Unofficial Sirius XM API',
	url='https://github.com/T-Santos/PySoSirius',
	author='Tyler Santos',
	author_email='1tsantos7+pysosirius@Gmail.com',
	license='MIT',
	packages=['pysosirius','pysosirius.database','pysosirius.web','pysosirius.common'],
	# Project uses BeautifulSoup, requests and selenium to
	# parse webpages for new info not stored in the local db
	install_requires=['bs4','requests','selenium'],
	package_data={
	    'pysosirius.database': ['PySoSirius.db'],
	},
	keywords="Sirius SiriusXM XM Music",	
	classifiers=[
		# How mature is this project? Common values are
		'Development Status :: 1 - Planning',

		# Indicate who your project is intended for
		'Intended Audience :: Developers',

		# Pick your license as you wish (should match "license" above)
		 'License :: OSI Approved :: MIT License',

		# Specify the Python versions you support here. In particular, ensure
		# that you indicate whether you support Python 2, Python 3 or both.
		'Programming Language :: Python :: 2.7'
	],
	zip_safe=True)