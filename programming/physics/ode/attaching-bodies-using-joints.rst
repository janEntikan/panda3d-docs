.. _attaching-bodies-using-joints:

Attaching Bodies using Joints
=============================

Joints
------

In most situations, you won't have just solid box-shaped or cylinder-shaped
models, but for example a human character has multiple body parts which can all
move in a different way. If you would make the entire character one solid body,
you wouldn't be able to move them independently of each other, and if you made
every body part a separate solid body, all the body parts would fall off since
they are not attached to each other. This is where Joints come in.

Joints are basically used to attach bodies to each other, or to attach a body to
the environment. There are several different kinds of joints: OdeHingeJoint,
OdeBallJoint, OdeSliderJoint, just to name a few. (Check the :mod:`panda3d.ode`
page in the API Reference for a more complete list.)

OdeBallJoint example
--------------------

To explain how joints work, look at the following example:

.. code-block:: python

   from direct.directbase import DirectStart
   from direct.directtools.DirectGeometry import LineNodePath
   from panda3d.core import *
   from panda3d.ode import *

   # Load the smiley and frowney models
   smiley = loader.load_model("smiley.egg")
   smiley.reparent_to(render)
   smiley.set_pos(-5, 0, -5)
   frowney = loader.load_model("frowney.egg")
   frowney.reparent_to(render)
   frowney.set_pos(-12.5, 0, -7.5)

   # Setup our physics world
   world = OdeWorld()
   world.set_gravity(0, 0, -9.81)

   # Setup the body for the smiley
   smiley_body = OdeBody(world)
   M = OdeMass()
   M.set_sphere(5000, 1.0)
   smiley_body.set_mass(M)
   smiley_body.set_position(smiley.get_pos(render))
   smiley_body.set_quaternion(smiley.get_quat(render))

   # Now, the body for the frowney
   frowney_body = OdeBody(world)
   M = OdeMass()
   M.set_sphere(5000, 1.0)
   frowney_body.set_mass(M)
   frowney_body.set_position(frowney.get_pos(render))
   frowney_body.set_quaternion(frowney.get_quat(render))

   # Create the joints
   smiley_joint = OdeBallJoint(world)
   smiley_joint.attach(smiley_body, None) # Attach it to the environment
   smiley_joint.set_anchor(0, 0, 0)
   frowney_joint = OdeBallJoint(world)
   frowney_joint.attach(smiley_body, frowney_body)
   frowney_joint.set_anchor(-5, 0, -5)

   # Set the camera position
   base.disable_mouse()
   base.camera.set_pos(0, 50, -7.5)
   base.camera.look_at(0, 0, -7.5)

   # We are going to be drawing some lines between the anchor points and the joints
   lines = LineNodePath(parent=render, thickness=3.0, color_vec=(1, 0, 0, 1))
   def draw_lines():
       # Draws lines between the smiley and frowney.
       lines.reset()
       lines.draw_lines([((frowney.get_x(), frowney.get_y(), frowney.get_z()),
                         (smiley.get_x(), smiley.get_y(), smiley.get_z())),
                        ((smiley.get_x(), smiley.get_y(), smiley.get_z()),
                         (0, 0, 0))])
       lines.create()

   # The task for our simulation
   def simulation_task(task):
       # Step the simulation and set the new positions
       world.quick_step(base.clock.dt)
       frowney.set_pos_quat(render, frowney_body.get_position(), frowney_body.get_quaternion())
       smiley.set_pos_quat(render, smiley_body.get_position(), smiley_body.get_quaternion())
       draw_lines()
       return task.cont

   draw_lines()
   task_mgr.do_method_later(0.5, simulation_task, "Physics Simulation")

   base.run()

The part of the code that does the magic is this:

.. code-block:: python

   # Create the joints
   smiley_joint = OdeBallJoint(world)
   smiley_joint.attach(smiley_body, None) # Attach it to the environment
   smiley_joint.set_anchor(0, 0, 0)
   frowney_joint = OdeBallJoint(world)
   frowney_joint.attach(smiley_body, frowney_body)
   frowney_joint.set_anchor(-5, 0, -5)

This creates two joints, the first to attach the smiley to the environment, and
the second to attach the frowney to the smiley. The ``attach()`` method on the
joint is used to set the two bodies that are attached; you can replace either
argument with None to attach them to the environment. The ``set_anchor`` method
is used to set the anchor point for the joints.

In this image you can see how the joints are set up:

.. image:: balljointexample2.jpg
