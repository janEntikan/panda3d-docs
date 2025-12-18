.. _softbody-patch:

Bullet Softbody Patch
=====================

Soft body patches are two-dimensional rectangular meshes, which can be used to
simulate for example a flag, a tapestry, or sheets of paper.

Setup
-----

Setting up a soft body patch is similar to soft body ropes, but a few extra
settings have to be done. The following code will create rectangular path with
31 by 31 segments, and thus 32 x 32 nodes.

.. only:: python

   .. code-block:: python

      from panda3d.bullet import BulletSoftBodyNode

      info = self.world.get_world_info()
      info.set_air_density(1.2)
      info.set_water_density(0)
      info.set_water_offset(0)
      info.set_water_normal(Vec3(0, 0, 0))

      resx = 31
      resy = 31

      p00 = Point3(-8, -8, 0)
      p10 = Point3( 8, -8, 0)
      p01 = Point3(-8,  8, 0)
      p11 = Point3( 8,  8, 0)

      fixeds = 1+2+4+8
      gendiags = True

      body_node = BulletSoftBodyNode.make_patch(info, p00, p10, p01, p11, resx, resy, fixeds, gendiags)

      material = body_node.append_material()
      material.set_linear_stiffness(0.4)
      body_node.generate_bending_constraints(2, material)

      body_node.set_total_mass(50.0)
      body_node.get_shape(0).set_margin(0.5)
      body_np = self.world_np.attach_new_node(body_node)
      world.attach_soft_body(body_node)

.. only:: cpp

   .. code-block:: cpp

      TODO

First we have to configure the soft body world properties, like we did for
soft body ropes too. Next we define variables for the resolution in x- and
y-direction, and for the four corner points of the patch.

The variable fixeds is set to the value 1+2+4+8=15, meaning that the patch
should be attached to the world on all four corners. To attach it to the first
and third corner (diagonal) we would set the value to 1+8=9, and to not attach
it at all we would set it to 0.

Now we can create the soft body node using the factory method
``make_patch``. The following
configuration differs from what we have seen for soft body ropes.

-  First we create an additional material attached to the soft body. Initially
   a soft body has already one material, but for this example we want a second
   one.
-  On the material we set the linear stiffness, and the create bending
   constraints for this material.
-  Finally we choose a value of about the grid spacing for the soft bodies
   margin. Other bodies colliding with the soft body could fall through in
   between the nodes if the value is too small, and if it is too large they
   will already collide with the soft body when still noticeably far away.

Visualisation
-------------

In order to have a visual representation of the soft body patch we need a
``GeomNode``. Panda3D's Bullet
module has a helper method which will do the work for us. The following code
snippet shows how use this helper method.

.. only:: python

   .. code-block:: python

      from panda3d.core import GeomVertexFormat
      from panda3d.bulletimport BulletHelper

      fmt = GeomVertexFormat.get_v3n3t2()
      geom = BulletHelper.make_geom_from_faces(body_node, fmt, True)
      body_node.link_geom(geom)
      vis_node = GeomNode('')
      vis_node.add_geom(geom)
      vis_np = body_np.attach_new_node(vis_node)

.. only:: cpp

   .. code-block:: cpp

      TODO

The third parameter to ``make_geom_from_faces``
is set to ``True``, making the
created geometry be two-sided. If set to
``False`` we would get a
one-sided geometry, which might be enough, depending on your requirements.

So far the generated geometry has no texture and no texture coordinates. But
the texture has already a column for texcoords, so we just need to write
texcoords using a ``GeomVertexRewriter``. The
following code shows a convenience method which will do this for us.

.. only:: python

   .. code-block:: python

      tex = loader.load_texture('models/panda.jpg')
      vis_np.set_texture(tex)
      BulletHelper.make_texcoords_for_patch(geom, resx, resy)

.. only:: cpp

   .. code-block:: cpp

      TODO

Note: It is also possible to render soft body patches using a
``NurbsSurfaceEvaluator`` and
``SheetNode``, but results are
usually better when rendering patches directly, that is using linked
``Geom``.
