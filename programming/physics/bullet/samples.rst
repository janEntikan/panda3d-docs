.. _bullet_samples:

Bullet Samples
==============

Learning the Bullet module is best done by looking at working samples. A bunch
of tutorials can be downloaded from the following link. The samples include
all models and textures.

https://www.panda3d.org/download/noversion/bullet-samples.zip

More samples contributed by various users follow below here:

Stack of cubes falling on top of each other:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. only:: python

   .. code-block:: python

      import direct.directbase.DirectStart
      from panda3d.core import Vec3
      from panda3d.bullet import BulletWorld
      from panda3d.bullet import BulletPlaneShape
      from panda3d.bullet import BulletRigidBodyNode
      from panda3d.bullet import BulletBoxShape

      base.cam.set_pos(10, -30, 20)
      base.cam.look_at(0, 0, 5)

      # World
      world = BulletWorld()
      world.set_gravity(Vec3(0, 0, -9.81))

      # Plane
      shape = BulletPlaneShape(Vec3(0, 0, 1), 1)
      node = BulletRigidBodyNode('Ground')
      node.add_shape(shape)
      np = render.attach_new_node(node)
      np.set_pos(0, 0, -2)
      world.attach_rigid_body(node)

      # Boxes
      model = loader.load_model('models/box.egg')
      model.set_pos(-0.5, -0.5, -0.5)
      model.flatten_light()
      shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
      for i in range(10):
          node = BulletRigidBodyNode('Box')
          node.set_mass(1.0)
          node.add_shape(shape)
          np = render.attach_new_node(node)
          np.set_pos(0, 0, 2+i*2)
          world.attach_rigid_body(node)
          model.copy_to(np)

      # Update
      def update(task):
        dt = base.clock.dt
        world.do_physics(dt)
        return task.cont

      task_mgr.add(update, 'update')
      base.run()
