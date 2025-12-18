.. _client-repositories:

Client Repositories
===================

Similar to the server repositories, client repositories are there to handle the
lower-level connection code to the server. As seen earlier in the
:ref:`ai-repositories` chapter, client repositories doesn’t necessarily have to
be on end-user machines but can also be used on servers. A basic client
repository implementation may look as follows or should at least implement the
following set of functions to work properly.

.. code-block:: python

   from direct.distributed.ClientRepository import ClientRepository
   from panda3d.core import URLSpec, ConfigVariableInt, ConfigVariableString
   from DGameObject import DGameObject

   class GameClientRepository(ClientRepository):

       def __init__(self):
           dc_file_names = ['direct.dc', 'your_own_dc_file.dc']

           # a distributed object of our game.
           self.distributed_object = None
           self.ai_d_game_obect = None

           ClientRepository.__init__(
               self,
               dc_file_names = dc_file_names,
               threaded_net = True)

           # Set the same port as configured on the server to be able to connect
           # to it
           tcp_port = ConfigVariableInt('server-port', 4400).get_value()

           # Set the IP or hostname of the server we want to connect to
           hostname = ConfigVariableString('server-host', '127.0.0.1').get_value()

           # Build the URL from the server hostname and port. If your server
           # uses another protocol then http you should change it accordingly.
           # Make sure to pass the connect_method to the ClientRepository.__init__
           # call too.  Available connection methods are:
           # self.CM_HTTP, self.CM_NET and self.CM_NATIVE
           self.url = URLSpec('http://{}:{}'.format(hostname, tcp_port))

           # Attempt a connection to the server
           self.connect([self.url],
                        success_callback = self.connect_success,
                        failure_callback = self.connect_failure)

       def lost_connection(self):
           """ This should be overridden by a derived class to handle an
           unexpectedly lost connection to the gameserver. """
           # Handle the disconnection from the server.  This can be a reconnect,
           # simply exiting the application or anything else.
           exit()

       def connect_failure(self, status_code, status_string):
           """ Something went wrong """
           exit()

       def connect_success(self):
           """ Successfully connected.  But we still can't really do
           anything until we've got the do_id range. """

           # Make sure we have interest in the by the AIRepository defined
           # TimeManager zone, so we always see it even if we switch to
           # another zone.
           self.set_interest_zones([1])

           # We must wait for the TimeManager to be fully created and
           # synced before we can enter another zone and wait for the
           # game object.  The unique_name is important that we get the
           # correct, our sync message from the TimeManager and not
           # accidentally a message from another client
           self.accept_once(self.unique_name('got_time_sync'), self.sync_ready)

       def sync_ready(self):
           """ Now we've got the TimeManager manifested, and we're in
           sync with the server time.  Now we can enter the world.  Check
           to see if we've received our do_id_base yet. """

           # This method checks whether we actually have a valid do_id range
           # to create distributed objects yet
           if self.have_create_authority():
               # we already have one
               self.got_create_ready()
           else:
               # Not yet, keep waiting a bit longer.
               self.accept(self.unique_name('create_ready'), self.got_create_ready)

       def got_create_ready(self):
           """ Ready to enter the world.  Expand our interest to include
           any other zones """

           # This method checks whether we actually have a valid do_id range
           # to create distributed objects yet
           if not self.have_create_authority():
               # Not ready yet.
               return

           # we are ready now, so ignore further create_ready events
           self.ignore(self.unique_name('create_ready'))

           # Now the client is ready to create DOs and send and receive data
           # to and from the server

First of all, we need to initialize the :class:`.ClientRepository`. This will
handle the connection code to the server. We pass it our dc files as well as the
threaded_net parameter which will have the same effect as described in the server
repositories.

.. code-block:: python

   ClientRepository.__init__(
       self,
       dc_file_names = dc_file_names,
       threaded_net = True)

Having the client repository ready, we can try to connect to the desired server
with the :meth:`.ConnectionRepository.connect` call available from the CR.
Dependent on the outcome, one of the functions given to the call will be used.

.. code-block:: python

   self.connect([self.url],
                success_callback = self.connect_success,
                failure_callback = self.connect_failure)

In the connect_success method we have to make sure that the client is interested
in the correct zones in which a time manager has been instantiated. How the time
manager is set up and what it is used for will be shown in a later section.
For now we just expect it to exist in zone 1 on the AI Server.

As soon as the client is synced, the :class:`.TimeManager` will send a
got_time_sync event. It is recommended to show some kind of waiting screen to the
user at this point until the client is fully connected to the server.

In the sync_ready and got_create_ready methods you’ll see the
:meth:`.ClientRepository.haveCreateAuthority` function called. This is a check
to see if we are already able to create DOs and give them a correct
:term:`doId`. You can create DOs earlier already, but they may have invalid
:term:`doIds <doId>` then.

At the end of the got_create_ready method you can fully use the client and create
whatever DOs you may need and add other client related logic.

At this stage, you may also want to set interest in different zones for the
client to see objects created by the server and other clients which are placed
in those specific zones. You can do this by calling the
:meth:`.ClientRepository.setInterestZones()` method which you simply pass a
number of zone_ids that this client should see.

ShowBase Client Repository
--------------------------

After setting up your main client repository, you should add it to your ShowBase
instance in a variable called ``cr``, as in the following example:

.. code-block:: python

   base.cr = MyMainClientRepository()
