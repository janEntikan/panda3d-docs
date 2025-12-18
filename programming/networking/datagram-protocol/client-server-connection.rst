.. _client-server-connection:

Client-Server Connection
========================

The first step in network communication is to establish the client-server
connection. This entails two sets of operations: one for the server side
(which listens for incoming connections), and one for the client side (which
establishes a connection to the server). Both of these processes are described
below.

Preparing the server for connection
-----------------------------------

An average Panda program acting as a server will need to create four classes:

-  A :class:`.QueuedConnectionManager`, which handles the low-level connection
   processes, establishes connections, and handles unexpected network
   termination

-  A :class:`.QueuedConnectionListener`, which waits for clients to request a
   connection

-  A :class:`.QueuedConnectionReader`, which buffers incoming data from an
   active connection

-  A :class:`.ConnectionWriter`, which allows PyDatagrams to be transmitted out
   along an active connection

The first step is to instantiate these four classes.

.. code-block:: python

   from panda3d.core import QueuedConnectionManager
   from panda3d.core import QueuedConnectionListener
   from panda3d.core import QueuedConnectionReader
   from panda3d.core import ConnectionWriter

   c_manager = QueuedConnectionManager()
   c_listener = QueuedConnectionListener(c_manager, 0)
   c_reader = QueuedConnectionReader(c_manager, 0)
   c_writer = ConnectionWriter(c_manager, 0)

   active_connections = [] # We'll want to keep track of these later

This method of instantiation prepares the classes in single-thread mode, which
that realtime communication requires them to be polled periodically.

To accept client connections, the server opens a special "rendezvous" socket at
a specific port address. This port address must be known by both the client and
the server. Additionally, a backlog is specified; this is the number of incoming
connection requests that the connection will track before it starts rejecting
connection attempts. The responsibility for managing the rendezvous socket is
passed to the QueuedConnectionListener, and a task is spawned to periodically
poll the listener.

.. code-block:: python

   port_address = 9099 #No-other TCP/IP services are using this port
   backlog = 1000 #If we ignore 1,000 connection attempts, something is wrong!
   tcp_socket = c_manager.open_tcp_server_rendezvous(port_address,backlog)

   c_listener.add_connection(tcp_socket)

Since the network handlers we instantiated are polled, we'll create some tasks
to do the polling.

.. code-block:: python

   task_mgr.add(tsk_listener_polling, "Poll the connection listener", -39)
   task_mgr.add(tsk_reader_polling, "Poll the connection reader", -40)

When a connection comes in, the tsk_listener_polling function below handles the
incoming connection and hands it to the QueuedConnectionReader. The connection
is now established.

.. code-block:: python

   from panda3d.core import PointerToConnection
   from panda3d.core import NetAddress

   def tsk_listener_polling(taskdata):
       if c_listener.new_connection_available():

           rendezvous = PointerToConnection()
           net_address = NetAddress()
           new_connection = PointerToConnection()

           if c_listener.get_new_connection(rendezvous,net_address,new_connection):
               new_connection = new_connection.p()
               active_connections.append(new_connection) # Remember connection
               c_reader.add_connection(new_connection)     # Begin reading connection
       return Task.cont

Once a connection has been opened, the QueuedConnectionReader may begin
processing incoming packets. This is similar to the flow of the listener's task,
but it is up to the server code to handle the incoming data.

.. code-block:: python

   from panda3d.core import NetDatagram

   def tsk_reader_polling(taskdata):
       if c_reader.data_available():
           datagram = NetDatagram()  # catch the incoming data in this instance
           # Check the return value; if we were threaded, someone else could have
           # snagged this data before we did
           if c_reader.get_data(datagram):
               my_process_data_function(datagram)
       return Task.cont

Note that the QueuedConnectionReader retrieves data from all clients connected
to the server. The NetDatagram can be queried using NetDatagram.get_connection to
determine which client sent the message.

If the server wishes to send data to the client, it can use the ConnectionWriter
to transmit back along the connection.

.. code-block:: python

   # broadcast a message to all clients
   my_py_datagram = my_new_py_datagram()  # build a datagram to send
   for a_client in active_connections:
       c_writer.send(my_py_datagram,a_client)

Finally, the server may terminate a connection by removing it from the
QueuedConnectionReader's responsibility. It may also deactivate its listener so
that no more connections are received.

.. code-block:: python

   # terminate connection to all clients

   for a_client in active_connections:
       c_reader.remove_connection(a_client)
   active_connections = []

   # close down our listener
   c_manager.close_connection(tcp_socket)

Connecting with a client
------------------------

The process the client undertakes to connect to a server is extremely similar to
the process the server undertakes to receive connections. Like the server, a
client instantiates a QueuedConnectionManager, QueuedConnectionReader, and
ConnectionWriter. However, there are some differences in the process. In
general, a client has no need to open a rendezvous socket or create a
QueuedConnectionListener, since it will be doing the connecting itself. Instead,
the client connects to a specific server by specifying the server's IP address
and the correct socket ID.

.. code-block:: python

   port_address = 9099  # same for client and server

   # A valid server URL. You can also use a DNS name
   # if the server has one, such as "localhost" or "panda3d.org"
   ip_address = "192.168.0.50"

   # How long, in milliseconds, until we give up trying to reach the server?
   timeout = 3000  # 3 seconds

   my_connection = c_manager.open_tcp_client_connection(ip_address, port_address, timeout)
   if my_connection:
       c_reader.add_connection(my_connection)  # receive messages from server

When the client has finished communicating with the server, it can close the
connection.

.. code-block:: python

   c_manager.close_connection(my_connection)
