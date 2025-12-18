.. _projected-textures:

Projected Textures
==================

In a :ref:`previous section <texture-transforms>`, we introduced ways to apply
an explicit transformation to a model's texture coordinates, with methods like
:meth:`~.NodePath.set_tex_offset()` and :meth:`~.NodePath.set_tex_scale()`.
In addition to this explicit control, Panda3D offers a simple mechanism to apply
an automatic texture transform each frame, as computed from the relative
transform between any two nodes.

.. code-block:: python

   node_path.set_tex_projector(texture_stage, from_node_path, to_node_path)

When you have enabled this mode, the relative scene-graph transform from
``from_node_path`` to ``to_node_path``--that is, the result of
``from_node_path.get_transform(to_node_path)``--is automatically applied as a
texture-coordinate transform to the indicated texture_stage. The result is
more-or-less as if you executed the following command every frame:

.. code-block:: python

   node_path.set_tex_transform(texture_stage, from_node_path.get_transform(to_node_path))

There is no need for either ``from_node_path`` or ``to_node_path`` to have any
relation to the node_path that is receiving the
:meth:`~.NodePath.set_tex_projector()` call; they can be any two arbitrary
NodePaths. If either of them is just ``NodePath()``, it stands for the top of
the graph.

This has several useful applications. We have already introduced
:ref:`one application <automatic-texture-coordinates>`, in conjunction with
``MWorldPosition``, to move the generated texture coordinates from the root of
the graph to the model itself.

Interval-animated texture transforms
------------------------------------

Another handy application for a TexProjector is to enable the use of the various
:ref:`LerpIntervals <lerp-intervals>` to animate a texture transform. Although
there are no LerpIntervals that directly animate texture transforms, you can
make a LerpInterval animate a NodePath--and then set up a TexProjector effect to
follow that NodePath. For example:

.. code-block:: python

   smiley = loader.load_model('smiley.egg')
   lerper = NodePath('lerper')
   smiley.set_tex_projector(TextureStage.get_default(), NodePath(), lerper)
   i = lerper.pos_interval(5, VBase3(0, 1, 0))
   i.loop()

Note that you don't even have to parent the animated NodePath into the scene
graph. In the above example, we have set up the interval ``i`` to repeatedly
move the standalone NodePath ``lerper`` from position (0, 0, 0) to (0, 1, 0)
over 5 seconds. Since ``smiley`` is assigned a TexProjector that copies the
relative transform from ``NodePath()`` to ``lerper``--that is, the net transform
of ``lerper``--it means we are really animating the texture coordinates on
``smiley`` from (0, 0) to (0, 1) (the Z coordinate is ignored for an ordinary
2-D texture).

Projected Textures
------------------

Another useful application of the TexProjector is to implement projected
textures--that is, a texture applied to geometry as if it has been projected
from a lens somewhere in the world, something like a slide projector. You can
use this to implement a flashlight effect, for instance, or simple projected
shadows.

This works because the TexProjector effect does one additional trick: if the
second NodePath in the :meth:`~.NodePath.set_tex_projector()` call happens to be
a :class:`.LensNode`, then the TexProjector automatically applies the lens's
projection matrix to the texture coordinates (in addition to applying the
relative transform between the nodes).

To implement projected textures, you need to do three steps:

1. Apply the texture you want to the model you want to project it onto, usually
   on its own TextureStage, so that it is :ref:`multitextured <multitexture-introduction>`.

2. Put the ``MWorldPosition`` TexGen mode on the model. This copies the model's
   vertex positions into its texture coordinates, for your texture's TextureStage.

3. Call :meth:`model.set_tex_projector(texture_stage, NodePath(), projector)
   <.NodePath.set_tex_projector>`, where ``projector`` is the NodePath to the
   LensNode you want to project from.

For your convenience, the NodePath class defines the following method that
performs these three steps at once:

.. only:: python

   .. code-block:: python

      node_path.project_texture(texture_stage, texture, lens_node_path)

.. only:: cpp

   .. code-block:: cpp

      node_path.project_texture(texture_stage, texture, lens_node_path);

For instance, we could use it to project the bamboo texture ("envir-reeds.png")
onto the ripple.egg model, like this:

|Bamboo projected onto ripple|

You could move around the projector in the world, or even change the lens field
of view, and the bamboo image would follow it. (In the above image, the camera
model and the projection lines are made visible only for illustration purposes;
normally you wouldn't see them.)

This image was generated with the following code:

.. code-block:: python

   from direct.directbase.DirectStart import *
   from direct.actor import Actor
   from panda3d.core import *

   base.set_background_color(1, 1, 1, 1)

   ripple = Actor.Actor('ripple.egg')
   ripple.reparent_to(render)
   ripple.set_scale(10)
   ripple.pose('animation', 17)

   dl = DirectionalLight('dl')
   dlnp = camera.attach_new_node(dl)
   ripple.set_light(dlnp)

   proj = render.attach_new_node(LensNode('proj'))
   lens = PerspectiveLens()
   proj.node().set_lens(lens)
   proj.node().show_frustum()
   proj.find('frustum').set_color(1, 0, 0, 1)
   cam_model = loader.load_model('camera.egg')
   cam_model.reparent_to(proj)
   proj.reparent_to(render)
   proj.set_pos(1.5, -7.3, 2.9)
   proj.set_hpr(22, -15, 0)

   tex = loader.load_texture('maps/envir-reeds.png')
   tex.set_wrap_u(SamplerState.WMBorderColor)
   tex.set_wrap_v(SamplerState.WMBorderColor)
   tex.set_border_color((1, 1, 1, 0))
   ts = TextureStage('ts')
   ts.set_sort(1)
   ts.set_mode(TextureStage.MDecal)
   ripple.project_texture(ts, tex, proj)

   base.disable_mouse()
   camera.set_pos(-7.8, -22.4, 0)
   camera.set_hpr(-21, 0, 0)

   base.graphics_engine.render_frame()
   base.screenshot('projected_bamboo.jpg', default_filename=0)

.. |Bamboo projected onto ripple| image:: projected-bamboo.jpg
