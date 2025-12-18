.. _related-object-manager:

Related Object Manager
======================

The Related Object Manager is a handy class that can be utilized to wait for the
creation of multiple DOs. You simply pass the IDs of the objects you want to
wait for as a list and a callback method. This callback method is called when
all objects have been created successfully.
This manager is readily available in repository-based classes like the
Client Repository.


.. code-block:: python

   # Use the client repositories manager
   cr.related_object_mgr.request_objects(
       [
        player_do_id,
        level_do_id,
        some_other_object_do_id
       ],
       all_callback = self.all_objects_manifested)

   def all_objects_manifested(self, all_objects):
       # all_objects now contains the DOs for the player, level
       # and some_other_object
