.. _queries:

Bullet Queries
==============

Bullet offers a bunch of different queries for retrieving information about
collision objects. A common usecase is sensors needed by game logic components.
For example to find out if the space in front of an NPC object is blocked by a
solid obstacle, or to find out if an NPC can see some other object.

Ray Test
--------

Raycasting is to shoot a ray from one position (the from-position) to another
position (the to-position). Both the from-position and the to-position have to
be specified in global coordinates. The ray test methods will then return a
result object which contains information about which objects the ray has hit.

There are two different ray test method: The first method (``ray_test_all``)
returns all collision objects hit by the ray. But sometimes we are only
interested in the first collision object hit by the ray. Then we can use the
second ray test method (``ray_test_closest``).

Example for closest hit:

.. only:: python

   .. code-block:: python

      p_from = Point3(0, 0, 0)
      p_to = Point3(10, 0, 0)

      result = world.ray_test_closest(p_from, p_to)

      print(result.has_hit())
      print(result.get_hit_pos())
      print(result.get_hit_normal())
      print(result.get_hit_fraction())
      print(result.get_node())

.. only:: cpp

   .. code-block:: cpp

      LPoint3 p_from(0, 0, 0);
      LPoint3 p_to(10, 0, 0);
      BulletAllHitsRayResult result = world->ray_test_closest(p_from, p_to);

Example for all hits:

.. only:: python

   .. code-block:: python

      p_from = Point3(0, 0, 0)
      p_to = p_from + Vec3(1, 0, 0) * 99999

      result = world.ray_test_all(p_from, p_to)

      print(result.has_hits())
      print(result.get_closest_hit_fraction())
      print(result.get_num_hits())

      for hit in result.get_hits():
          print(hit.get_hit_pos())
          print(hit.get_hit_normal())
          print(hit.get_hit_fraction())
          print(hit.get_node())

.. only:: cpp

   .. code-block:: cpp

      LPoint3 p_from = LPoint3(0, 0, 0);
      LPoint3 p_to = p_from + LVector3d(1, 0, 0) * 99999;
      BulletAllHitsRayResult result = world->ray_test_all(p_from, p_to);

Often users want to pick or select an object by clicking on it with the mouse.
We can use the ``ray_test_closest`` to find the collision object which is "under"
the mouse pointer, but we have to convert the coordinates in camera space to
global coordinates world space. The following example shows how this can be
done.

.. only:: python

   .. code-block:: python

      # Get to and from pos in camera coordinates
      p_mouse = base.mouse_watcher_node.get_mouse()
      p_from = Point3()
      p_to = Point3()
      base.cam_lens.extrude(p_mouse, p_from, p_to)

      # Transform to global coordinates
      p_from = render.get_relative_point(base.cam, p_from)
      p_to = render.get_relative_point(base.cam, p_to)

.. only:: cpp

   .. code-block:: cpp

      TODO

Sweep Test
----------

The sweep test is similar to the ray test. There are two differences: (1) The
sweep test does not use an infinite thin ray, like the ray test, but checks for
collisions with a convex shape which is "moved" along the from from-position to
to-position. (2) The sweep test wants to have "from" and "to" specified as
``TransformState``. The sweep test can for example be used to predict if an
object would collide with something else if it was moving from it's current
position to some other position.

The sweep test can only be used with shapes that are convex, otherwise the call
will fail. Many primitive shapes (sphere, box, etc.) are convex, but a triangle
mesh is not. (If you have geometry that is convex, use a BulletConvexHullShape
instead of a BulletTriangleMeshShape.)

.. only:: python

   Example for sweep testing:

   .. code-block:: python

      ts_from = TransformState.make_pos(Point3(0, 0, 0))
      ts_to = TransformState.make_pos(Point3(10, 0, 0))

      shape = BulletSphereShape(0.5)
      penetration = 0.0

      result = world.sweep_test_closest(shape, ts_from, ts_to, penetration)

      print(result.has_hit())
      print(result.get_hit_pos())
      print(result.get_hit_normal())
      print(result.get_hit_fraction())
      print(result.get_node())

Contact Test
------------

There are two contact tests. One which checks if a collision objects is in
contact with other collision objects, and another which checks for a pair of
collision objects if they are in contact.

.. only:: python

   Example for contact testing:

   .. code-block:: python

      body1 = BulletRigidBodyNode("body1")
      ...

      body2 = BulletRigidBodyNode("body2")
      ...

      result = world.contact_test(node1)
      result = world.contact_test_pair(node1, node2)

      print(result.get_num_contacts())

      for contact in result.get_contacts():
        print(contact.get_node0())
        print(contact.get_node1())

        mpoint = contact.get_manifold_point()
        print(mpoint.get_distance())
        print(mpoint.get_applied_impulse())
        print(mpoint.get_position_world_on_a())
        print(mpoint.get_position_world_on_b())
        print(mpoint.get_local_point_a())
        print(mpoint.get_local_point_b())

Filtering
---------

The test methods on BulletWorld also take an optional ``mask`` argument that can
be used to limit which groups are matched against (see
:ref:`collision-filtering` for information about collision groups). The default
is ``BitMask32.all_on()``, which indicates that bodies in all groups are
considered for the test.

For example, the following query will consider object A and C, but ignore
object B:

.. code-block:: python

   # These three bodies are in different groups
   obj_a.set_collide_mask(BitMask32.bit(0))
   obj_b.set_collide_mask(BitMask32.bit(1))
   obj_c.set_collide_mask(BitMask32.bit(2))

   fro = (0, 0, 0)
   to = (1, 0, 0)
   mask = BitMask32.bit(0) | BitMask32.bit(2)
   result = world.ray_test_closest(fro, to, mask)

Of particular note if you are using the ``groups-mask`` filter algorithm is that
the mask matches directly against the collide mask of the bodies, ignoring the
group matrix entirely. For example, if you specify ``BitMask32.bit(1)``, it will
consider all bodies that have a collide mask with this bit enabled (ie. all
bodies that are in group 1). It does not behave as though the ray itself were a
body in group 1.
