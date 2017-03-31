PySoSirius
=======================

An API to extract Sirius XM channel data

----

Package Contents

- PySoSirius - Main driver used to get channels stored in a local SQLite database.
- SiriusManager - Used to interface with local SQLite database.
- SiriusScraper - Used to scrape SiriusXM's website for channel data.
- SiriusChannel - Used to interact with a specific channel.
- SiriusCurrentlyPlaying - Used to wrap currently playing data polled from SiriusXM.

**Get all locally stored channels**

.. code-block:: python

   from pysosirius import PySoSirius

   sirius = PySoSirius()
   sirius.get_channels()

**Get one locally stored channel**

.. code-block:: python

   from pysosirius import PySoSirius

   sirius = PySoSirius()
   sirius.get_channel(channel=56)

**Get Currently Playing and print interesting info**

.. code-block:: python

   from pysosirius import PySoSirius

   sirius = PySoSirius()
   channel = sirius.get_channel(channel=56)
   channel.get_currently_playing()

   print('artist: ' + channel.currently_playing.artist_name)
   print('song:   ' + channel.currently_playing.song_name)
   print('album: ' + channel.currently_playing.album)

**Scrape and store only music channels**

.. code-block:: python

   from pysosirius import PySoSirius
   from pysosirius.web.utilities import SiriusScraper  
   from pysosirius.sirius_channel import SiriusChannel
   from pysosirius.database.manager import SiriusManager

   db_manager = SiriusManager()
   scraper = SiriusScraper()
   channels = scraper.get_channels_data()

   for channel in channels:
       channel_data = PySoSirius.wrap_channel_data(channel)
       if channel_data.category == 'Music':
          db_manager.set_channel_row(channel_data)

   db_manager.save()
