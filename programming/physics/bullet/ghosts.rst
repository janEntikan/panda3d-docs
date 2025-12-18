.. _ghosts:

Bullet Ghosts
=============

Ghost objects are intangible objects. They do collide with other objects, but
they won't create any collision response (forces etc.) from such collisions.
Ghost objects keep track of all objects they collide with, and it is possible to
query them for all objects they currently overlap with.

Ghost objects therefore can be used to implement a sensor, which detects the
presence of any (or a particular) object within the sensor's shape. For example
an automatic door which should open if the player is in front of the door, or an
area which triggers some event if the player moves through the area.

.. only:: python

   Example for how to set up a ghost object:

   .. code-block:: python

      from panda3d.bullet import BulletGhostNode
      from panda3d.bullet import BulletBoxShape

      shape = BulletBoxShape(Vec3(1, 1, 1))

      ghost = BulletGhostNode('Ghost')
      ghost.add_shape(shape)
      ghost_np = render.attach_new_node(ghost)
      ghost_np.set_pos(0, 0, 0)
      ghost_np.set_collide_mask(BitMask32(0x0f))

      world.attach_ghost(ghost)

   Example for how to get overlapping objects:

   .. code-block:: python

      def check_ghost(self, task):
          ghost = ghost_np.node()
          print(ghost.get_num_overlapping_nodes())
          for node in ghost.get_overlapping_nodes():
              print(node)

          return task.cont

      task_mgr.add(check_ghost, 'check_ghost')
