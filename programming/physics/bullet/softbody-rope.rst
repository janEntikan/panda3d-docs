.. _softbody-rope:

Bullet Softbody Rope
====================

Soft body ropes are best compared to chains of interconnected nodes. This page
deals with setup, visualization and attaching things to soft body ropes.

Setup
-----

The following code will create a soft body rope with 8 segments (variable
``res``), and thus 8 + 2 = 10 nodes. ``p1`` is the initial position of the first
node, and ``p2`` is the initial position of the last node. ``fixeds`` will be
explained later on this page.

.. only:: python

   .. code-block:: python

      from panda3d.bullet import BulletSoftBodyNode

      info = self.world.get_world_info()
      info.set_air_density(1.2)
      info.set_water_density(0)
      info.set_water_offset(0)
      info.set_water_normal(Vec3(0, 0, 0))

      res = 8
      p1 = Point3(0, 0, 4)
      p2 = Point3(10, 0, 4)
      fixeds = 0

      body_node = BulletSoftBodyNode.make_rope(info, p1, p2, res, fixeds)
      body_node.set_total_mass(50.0)
      body_np = world_np.attach_new_node(body_node)
      world.attach_soft_body(body_node)

.. only:: cpp

   .. code-block:: cpp

      TODO

Visualisation
-------------

So far we have a physical object, the soft body rope, but aside from the debug
renderer this object is not shown in our scene. We need something to visualize
the rope.

There are two ways of rendering the rope. First we can make use of a NURBS
curve, or we can simple render the rope using geom lines. First we have a look
at how to render the rope using geom lines.

.. only:: python

   .. code-block:: python

      from panda3d.core import GeomNode

      geom = BulletHelper.make_geom_from_links(body_node)

      vis_node = GeomNode('')
      vis_node.add_geom(geom)
      vis_np = body_np.attach_new_node(vis_node)

      body_node.link_geom(geom)

.. only:: cpp

   .. code-block:: cpp

      TODO

The class ``BulletHelper`` has a convenience method which creates a ready-to-use
``Geom`` for us. We only need to wrap the ``Geom`` in a ``GeomNode``, and insert
it into the scene graph. Since we want the visualisation of the rope to be at
the same place as the rope we insert the ``GeomNode`` as a child of the
``BulletSoftBodyNode``.

There is just one thing missing. The ``GeomNode`` doesn't know that it is the
visualization of a soft body rope. When advancing the simulation time the soft
body rope will deform, but the visualization will always stay the way it has
been created. To fix this we can tell the soft body node that this particular
``Geom`` is it's visualization. The soft body node will now update the ``Geom``
each frame. This is done in the last line, by linking the geom to the soft body
node.

The result doesn't look very good. It's just a thin line. But instead of the
above code we can use a NURBS curve for visualization.

.. only:: python

   .. code-block:: python

      from panda3d.core import RopeNode
      from panda3d.core import NurbsCurveEvaluator

      curve = NurbsCurveEvaluator()
      curve.reset(res + 2)

      body_node.link_curve(curve)

      vis_node = RopeNode('')
      vis_node.set_curve(curve)
      vis_node.set_render_mode(RopeNode.RMTube)
      vis_node.set_uv_mode(RopeNode.UVParametric)
      vis_node.set_num_subdiv(4)
      vis_node.set_num_slices(8)
      vis_node.set_thickness(0.4)
      vis_np = self.world_np.attach_new_node(vis_node)
      vis_np.set_texture(loader.load_texture('some_texture.jpg'))

.. only:: cpp

   .. code-block:: cpp

      TODO

First we create a nurbs curve (``NurbsCurveEvaluator``), and then we link this
nurbs curve to the soft body rope node. The soft body node will update the nurbs
curve every frame from now on.

But we are not done yet. We still need to create something that can be seen in
the scene graph. A ``RopeNode`` can render a ``NurbsCurveEvaluator``. For
details on how to configure the ``RopeNode`` please refer to the Panda3D API
documentation; both the ``RopeNode`` and the ``NurbsCurveEvaluator`` are not
part of the panda3d.bullet, but core Panda3D classes.

Attaching the rope
------------------

Now we have created a rope, and we can render it. Next we want to attach the
rope to something, that is "glue" it either to some other object, usually a
rigid body, or to a specific position of the world.

At the beginning of this page we promised to deal with the ``fixeds`` parameter
later on the page. This is the place. Using the ``fixeds`` parameter we can
attach the rope to a position in the world (global coordinates!). Depending on
the value of this parameter we can attach different nodes/vertices of the rope:

-  0: No node/vertex is attached.
-  1: Only the first node/vertex is attached.
-  2: Only the last node/vertex is attached.
-  3: Both the first and the last node/vertex are attached.

Or we want to attach the soft body rope to a rigid body. In the following code
snippet the last node/vertex of a soft body rope is attached to a rigid body.

.. only:: python

   .. code-block:: python

      # NodePath for some BulletSoftBody "rope"
      soft_np = ...

      # NodePath for some BulletRigidBody
      rigid_np = ...

      # Index of the last node of the rope
      idx = soft_np.node().get_num_nodes() - 1

      # Attach the last node of the rope with the rigid body
      soft_np.node().append_anchor(idx, rigid_np.node())

.. only:: cpp

   .. code-block:: cpp

      TODO
