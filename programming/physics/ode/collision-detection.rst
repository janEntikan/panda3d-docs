.. _collision-detection-with-ode:

Collision Detection with ODE
============================

Collision Detection
-------------------

There are two types of collision detection: the kind that immediately makes the
objects bounce back on a collision, and the kind that instead of making the
objects bounce back immediately creates control joints instead. The latter is
the method the Open Dynamics Engine uses. Normally, you would use near callbacks
to make the control joints and have the objects bounce back. However, Panda3D
has an auto_collide feature that automatically does these things for you.

These are the steps needed to have your objects collide with each other:

-  Create an OdeSpace (explained below). Use ``set_auto_collide_world(world)`` to
   let the OdeSpace know in which world you want to collide things.
-  Create an OdeJointGroup() to hold the contact joints. Use
   ``space.set_auto_collide_joint_group`` to let the space know in which
   OdeJointGroup you would like to store the contact joints.
-  Configure the surface table for the world.
-  Create ODE collision geometry for your bodies, e.g. OdeBoxGeom, OdePlaneGeom,
   etc. Be sure to set collide and category :ref:`bitmasks <collision-bitmasks>`
   on it using the ``set_collide_bits`` and ``set_category_bits`` methods. Assign it
   to your body using ``geom.set_body(body)``.
-  In your simulation loop, call ``space.auto_collide()`` before you call
   ``world.quick_step``.
-  After using quick_step, you need to empty your OdeJointGroup using the
   ``empty()`` method.

Spaces
------

To be able to use collision detection, you will need to create an OdeSpace.
There are three different kinds of space types you have to choose from, any one
will work but each one is more optimized for a special kind of simulation.

-  OdeSimpleSpace. This is the most simple kind of space available. This does
   not perform any collision culling at all, that's why it is not preferred for
   a large number of objects. If you have a small amount of objects, however,
   you will most likely prefer an OdeSimpleSpace.
-  If you have more objects and a larger scene, you will want to use the
   OdeQuadTreeSpace. This uses a pre-allocated hierarchical grid-based AABB tree
   to quickly cull collision checks. It's exceptionally quick for large amounts
   of objects in landscape-shaped worlds.
-  Finally, there's the OdeHashSpace, which uses an internal data structure that
   records how each geom overlaps cells in one of several three dimensional
   grids. Each grid has cubical cells of side lengths 2**i, where i is an
   integer that ranges from a minimum to a maximum value. You can set this
   minimum and maximum value using the ``set_min_level`` and ``set_max_level``
   functions respectively, or you can use ``set_levels`` to set them all in one
   call.

Geometry
--------

Geometry are the collision solids that you place in a space. These collision
solids are separate from panda's own collision solids but there are similar
collision solid types. The general code for creating geometry is
``OdeGeom(space, [parameters])``, where space is the OdeSpace the geometry is
being placed in. Parameters are dependent on which geometry solid you choose.
The geometry types that you can choose from are:

===================== ============== =======================================================
Geometry              Shape          Initialization Parameters
===================== ============== =======================================================
OdeBoxGeom            Box            ``OdeBoxGeom(space, length, width, height)``
OdeCappedCylinderGeom Capsule        ``OdeCappedCylinderGeom(space, radius, length)``
OdeCylinderGeom       Cylinder       ``OdeCylinderGeom(space, radius, length)``
OdePlaneGeom          Infinite Plane ``OdePlaneGeom(space, Vec4(<vector of plane normal>))``
OdeRayGeom            Finite Ray     ``OdeRayGeom(space, ray_length)``
OdeSphereGeom         Sphere         ``OdeSphereGeom(space, radius)``
OdeTriMeshGeom        3D Mesh        ``OdeTriMeshGeom(space, OdeTriMeshData)``
===================== ============== =======================================================

To set the position and direction of an OdeRayGeom, you must call
``OdeRayGeom.set(Vec3(<position>), Vec3(<direction>))``. The length of the
direction vector is always set to the ray length specified during instantiation.

A trimesh geometry allows you to create collision geometry of an arbitrary shape
from a 3d model. However collision detection with a trimesh is the most
expensive and might be unreliable, for most applications you are better off
approximating the shape with another collision solid. To get the OdeTriMeshGeom
from a model requires two steps:

.. only:: python

   .. code-block:: python

      model_trimesh = OdeTriMeshData(model_node_path, True)
      model_geom = OdeTriMeshGeom(space, model_trimesh)

.. only:: cpp

   .. code-block:: cpp

      PT(OdeTriMeshData) model_trimesh = new OdeTriMeshData(model_node_path, true);
      OdeTriMeshGeom model_geom (space, model_trimesh);

If a geometry represents a physically dynamic object you can associate it with
the dynamic body using ``ode_geom.set_body(body)``. This will automatically
reposition the geometry with regard to the position of the related body in the
OdeWorld.

Surfaces
--------

Sufaces define the material a geometry is made of and the Surface Table defines
how materials react with each other setting the bounce, friction etc. To set up
the surface system, you must first initialize the surface table which is done
with ``ode_world.init_surface_table(number_of_surfaces)``

Once you have done that, you have to setup the parameters for collisions between
two surfaces using
``ode_world.set_surface_entry(surface_id1, surface_id2, mu, bounce, bounce_vel, soft_erp, soft_cfm, slip, dampen)``.
The surface identifiers start from 0 so if you initialized your surface table
with 3 surfaces, the surface IDs are 0, 1, 2.

These are what the rest of the parameters mean:

mu
   This is the `Coulomb friction coefficient <https://en.wikipedia.org/wiki/Coefficient_of_friction>`__.
   It means how much friction the contact has, a value of 0.0 means there will
   be no friction at all, while a value of ``OdeUtil.get_infinity()`` means the
   contact will never slip.
bounce
   This is how bouncy the surface is. A value of 0.0 means it is not bouncy, a
   value of 1.0 gives a very bouncy surface.
bounce_vel
   The minimum velocity a body must have before it bounces. If a body collides
   with a velocity lower than this value, it will not bounce off.
soft_erp
   The error reduction parameter of the contact normal. This is used to simulate
   soft surfaces.
soft_cfm
   The constraint force mixing parameter of the contact normal. This is used to
   simulate soft surfaces.
slip
   The coefficient for the force-dependent slip. This makes it possible for
   bodies to slide past each other.
dampen
   This is used to simulate a `damping <https://en.wikipedia.org/wiki/Damping>`__
   effect.

If you have multiple surfaces, you need to tell ODE which surface belongs to
which geometry. You can assign surfaces to your geometry using
``ode_space.set_surface_type(geometry, surface_id)``

Collision Events
----------------

It is also possible to receive an event when a collision occurs. You need to set
the name of the event by doing:

.. only:: python

   .. code-block:: python

      space.set_collision_event("your_collision")

.. only:: cpp

   .. code-block:: cpp

      space.set_collision_event("your_collision");

You can then use this event name in an ``accept()`` call. The parameter passed
to the event is an OdeCollisionEntry, which holds all the geoms and contacts in
the collision. See the API Reference page for
:class:`~panda3d.ode.OdeCollisionEntry` for more details.

The following code shows how it works (the methods used are not real):

.. code-block:: python

   # Setup collision event
   def on_collision(entry):
       geom1 = entry.get_geom1()
       geom2 = entry.get_geom2()
       body1 = entry.get_body1()
       body2 = entry.get_body2()
       if (body1 and body1 == spear) or (body2 and body2 == spear):
           # Must have hit someone
           for p in entry.get_contact_points()
               particle_system.draw_blood(p)

   space.set_collision_event("ode-collision")
   base.accept("ode-collision", on_collision)

Example
-------

This is an example of some random boxes falling down and colliding with the
floor.

.. code-block:: python

   from direct.directbase import DirectStart
   from panda3d.ode import OdeWorld, OdeSimpleSpace, OdeJointGroup
   from panda3d.ode import OdeBody, OdeMass, OdeBoxGeom, OdePlaneGeom
   from panda3d.core import BitMask32, CardMaker, Vec4, Quat
   from random import randint, random

   # Setup our physics world
   world = OdeWorld()
   world.set_gravity(0, 0, -9.81)

   # The surface table is needed for auto_collide
   world.init_surface_table(1)
   world.set_surface_entry(0, 0, 150, 0.0, 9.1, 0.9, 0.00001, 0.0, 0.002)

   # Create a space and add a contactgroup to it to add the contact joints
   space = OdeSimpleSpace()
   space.set_auto_collide_world(world)
   contactgroup = OdeJointGroup()
   space.set_auto_collide_joint_group(contactgroup)

   # Load the box
   box = loader.load_model("box")
   # Make sure its center is at 0, 0, 0 like OdeBoxGeom
   box.set_pos(-.5, -.5, -.5)
   box.flatten_light() # Apply transform
   box.set_texture_off()

   # Add a random amount of boxes
   boxes = []
   for i in range(randint(15, 30)):
       # Setup the geometry
       box_np = box.copy_to(render)
       box_np.set_pos(randint(-10, 10), randint(-10, 10), 10 + random())
       box_np.set_color(random(), random(), random(), 1)
       box_np.set_hpr(randint(-45, 45), randint(-45, 45), randint(-45, 45))
       # Create the body and set the mass
       box_body = OdeBody(world)
       M = OdeMass()
       M.set_box(50, 1, 1, 1)
       box_body.set_mass(M)
       box_body.set_position(box_np.get_pos(render))
       box_body.set_quaternion(box_np.get_quat(render))
       # Create a BoxGeom
       box_geom = OdeBoxGeom(space, 1, 1, 1)
       box_geom.set_collide_bits(BitMask32(0x00000002))
       box_geom.set_category_bits(BitMask32(0x00000001))
       box_geom.set_body(box_body)
       boxes.append((box_np, box_body))

   # Add a plane to collide with
   cm = CardMaker("ground")
   cm.set_frame(-20, 20, -20, 20)
   ground = render.attach_new_node(cm.generate())
   ground.set_pos(0, 0, 0); ground.look_at(0, 0, -1)
   ground_geom = OdePlaneGeom(space, Vec4(0, 0, 1, 0))
   ground_geom.set_collide_bits(BitMask32(0x00000001))
   ground_geom.set_category_bits(BitMask32(0x00000002))

   # Set the camera position
   base.disable_mouse()
   base.camera.set_pos(40, 40, 20)
   base.camera.look_at(0, 0, 0)

   # The task for our simulation
   def simulation_task(task):
       space.auto_collide() # Setup the contact joints
       # Step the simulation and set the new positions
       world.quick_step(base.clock.dt)
       for np, body in boxes:
           np.set_pos_quat(render, body.get_position(), Quat(body.get_quaternion()))
       contactgroup.empty() # Clear the contact joints
       return task.cont

   # Wait a split second, then start the simulation
   task_mgr.do_method_later(0.5, simulation_task, "Physics Simulation")

   base.run()

In this example, we're creating a random amount of boxes with a random
orientation and position, assigning collision solids to them, and adding a tuple
of the :ref:`NodePath <the-scene-graph>` and the body to a list. This way we can
easily keep track of all the boxes and loop through them to copy over the
positions from the OdeBody to Panda's NodePath in the simulation loop.
