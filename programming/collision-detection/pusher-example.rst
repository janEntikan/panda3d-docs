.. _pusher-example:

Pusher Example
==============

.. only:: python

   Here is a short example that shows two small spheres using a
   ``CollisionHandlerPusher``:

   .. code-block:: python

      from direct.showbase.ShowBase import ShowBase
      from panda3d.core import CollisionTraverser, CollisionHandlerPusher
      from panda3d.core import CollisionNode, CollisionSphere
      from panda3d.core import Point3

      # Initialize the scene.
      ShowBase()

      # Initialize the collision traverser.
      base.c_trav = CollisionTraverser()

      # Initialize the Pusher collision handler.
      pusher = CollisionHandlerPusher()

      # Load a model.
      smiley = loader.load_model('smiley')
      # Reparent the model to the camera so we can move it.
      smiley.reparent_to(camera)
      # Set the initial position of the model in the scene.
      smiley.set_pos(0, 25.5, 0.5)

      # Create a collision node for this object.
      c_node = CollisionNode('smiley')
      # Attach a collision sphere solid to the collision node.
      c_node.add_solid(CollisionSphere(0, 0, 0, 1.1))
      # Attach the collision node to the object's model.
      smiley_c = smiley.attach_new_node(c_node)
      # Set the object's collision node to render as visible.
      smiley_c.show()

      # Load another model.
      frowney = loader.load_model('frowney')
      # Reparent the model to render.
      frowney.reparent_to(render)
      # Set the position of the model in the scene.
      frowney.set_pos(5, 25, 0)

      # Create a collision node for this object.
      c_node = CollisionNode('frowney')
      # Attach a collision sphere solid to the collision node.
      c_node.add_solid(CollisionSphere(0, 0, 0, 1.1))
      # Attach the collision node to the object's model.
      frowney_c = frowney.attach_new_node(c_node)
      # Set the object's collision node to render as visible.
      frowney_c.show()

      # Add the Pusher collision handler to the collision traverser.
      base.c_trav.add_collider(frowney_c, pusher)
      # Add the 'frowney' collision node to the Pusher collision handler.
      pusher.add_collider(frowney_c, frowney, base.drive.node())

      # Have the 'smiley' sphere moving to help show what is happening.
      frowney.pos_interval(5, Point3(5, 25, 0), start_pos=Point3(-5, 25, 0), fluid=1).loop()

      # Run the scene. Move around with the mouse to see how the moving sphere changes
      # course to avoid the one attached to the camera.
      run()

.. only:: cpp

