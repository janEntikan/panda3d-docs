.. _softbody-triangles:

Bullet Softbody Triangles
=========================

Soft bodies made from triangular meshes are similar to soft body patches. just
that they are not restricted to rectangular meshes; any two-dimensional triangle
mesh will do. An interesting use case for such a soft body is a triangular mesh
which is closed. Bullet supports simulation of a pressure for the volume
captured inside such a soft body.

Setup
-----

The following code snippet shows how to setup an gas-filled soft body. Instead
of defining the triangle mesh ourselves we use the convenience method
``make_ellipsoid``, which returns a ready-to-use soft body with the shape of an
ellipsoid. The last parameter to this convenience method is the "resolution" of
the ellipsoid. The soft body will have more faces if raising this value.
Increasing the value will make the soft body more realistic, but it also
requires more performance to simulate the soft body.

.. only:: python

   .. code-block:: python

      # Soft body world information
      info = world.get_world_info()
      info.set_air_density(1.2)
      info.set_water_density(0)
      info.set_water_offset(0)
      info.set_water_normal(Vec3(0, 0, 0))

      # Softbody
      center = Point3(0, 0, 0)
      radius = Vec3(1, 1, 1) * 1.5

      body_node = BulletSoftBodyNode.make_ellipsoid(info, center, radius, 128)
      body_node.set_name('Ellipsoid')
      body_node.get_material(0).set_linear_stiffness(0.1)
      body_node.get_cfg().set_dynamic_friction_coefficient(1)
      body_node.get_cfg().set_damping_coefficient(0.001)
      body_node.get_cfg().set_pressure_coefficient(1500)
      body_node.set_total_mass(30, True)
      body_node.set_pose(True, False)

      body_np = render.attach_new_node(body_node)
      body_np.set_pos(15, 0, 12)
      body_np.set_h(90.0)
      world.attach_soft_body(body_np.node())

.. only:: cpp

   .. code-block:: cpp

      TODO

When comparing the soft body setup with the previous page, the soft body patch
setup, we will find that there are two differences:

-  First, there are three lines which get the configuration objects for this
   soft body (``getCfg``), and then set different parameters on this
   configuration object, in particular the "pressure coefficient". For more
   detailed information on what these parameters do it is best to fall back to
   the original Bullet documentation. A mapping between the original Bullet
   members of the btSoftBodyConfig class and the Panda3D BulletSoftBodyConfig
   object returned by ``getCfg`` is given on the manual page
   :ref:`softbody-config`.

-  Second, the method ``setPose`` is called. This method sets the current state
   of the soft body as a "default pose" or "lowest energy state". The soft body
   will try to return to this state if possible. The first parameter to this
   method is the volume flag, and the second parameter the frame flag. It is
   usually the best thing to set both flags to ``True``.

Visualisation
-------------

Again, in order to have a visual representation of the soft body we need a
``GeomNode``. We can use almost the same code as we have been using for soft
body patches. The only difference is that we don't need to make the created
geometry two-sided, since the inside of the closed mesh is usually not visible.

.. only:: python

   .. code-block:: python

      from panda3d.core import GeomVertexFormat
      from panda3d.bullet import BulletHelper

      fmt = GeomVertexFormat.get_v3n3t2()
      geom = BulletHelper.make_geom_from_faces(body_node, fmt)
      body_node.link_geom(geom)
      vis_node = GeomNode('EllipsoidVisual')
      vis_node.add_geom(geom)
      vis_np = body_np.attach_new_node(vis_node)

.. only:: cpp

   .. code-block:: cpp

      TODO
