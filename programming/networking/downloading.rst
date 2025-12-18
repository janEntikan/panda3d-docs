.. _downloading-a-file:

Downloading a File
==================

To download a file while the game is running without blocking the connections
one has to use :class:`.HTTPClient` and :class:`.HTTPChannel` objects. This will
allow the file to be downloaded in the background using the download_task task.

.. code-block:: python

   self.http = HTTPClient()
   self.channel = self.http.make_channel(True)
   self.channel.begin_get_document(DocumentSpec('http://my.url/'))
   self.rf = Ramfile()
   self.channel.download_to_ram(self.rf)
   task_mgr.add(self.download_task, 'download')

   def download_task(self, task):
       if self.channel.run():
           # Still waiting for file to finish downloading.
           return task.cont
       if not self.channel.is_download_complete():
           print("Error downloading file.")
           return task.done
       data = self.rf.get_data()
       print("got data:")
       print(data)
       return task.done

You can also download to file

.. code-block:: python

   channel.download_to_file(Filename(file_name))

The file channel can be queried for further information while the game is
running to get the current download state.

.. code-block:: python

   mb_downloaded = self.channel.get_bytes_downloaded() / 1024 / 1024
   percent_downloaded = 100. * self.channel.get_bytes_downloaded() / channel.get_file_size()
