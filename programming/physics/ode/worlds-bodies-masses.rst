.. _worlds-bodies-and-masses:

Worlds, Bodies and Masses
=========================

Worlds
------

To use the ODE physics system, you need to have an OdeWorld. A world is an
essential component in the physics structure, it holds all your rigid bodies and
joints, and controls global parameters, such as gravity, for the scene.

.. only:: python

   .. code-block:: python

      from panda3d.ode import OdeWorld
      my_world = OdeWorld()
      my_world.set_gravity(0, 0, -9.81)

.. only:: cpp

   .. code-block:: cpp

      #include "odeWorld.h"

      OdeWorld my_world;
      my_world.set_gravity(0, 0, -9.81);

As you can see, the gravity is set to a downward vector with length 9.81. This
value is the average gravity acceleration on Earth. If you want objects to fall
faster or slower, (e.g. if your game plays on the Moon, where the gravity
acceleration is 1.62 m/s²) you need to change this value, but in most cases you
want to leave it around 9.81 m/s².

Bodies and masses
-----------------

In physics space, the objects that matter are called bodies. In order to have
something affected by physics, you need to create an OdeBody, and set an OdeMass
on it.

An OdeMass does not just define how much an object weighs. You roughly have to
specify a shape so ODE will know how the mass is divided over the body. Also,
ODE will have to know either the density of the object or the mass.

In the following example the geometry is assumed to be a box-shaped object made
of lead, and the box has a width, length and height of 1 meter.

.. only:: python

   .. code-block:: python

      from panda3d.ode import OdeBody, OdeMass
      my_body = OdeBody(my_world)
      my_body.set_position(some_panda_object.get_pos(render))
      my_body.set_quaternion(some_panda_object.get_quat(render))
      my_mass = OdeMass()
      my_mass.set_box(11340, 1, 1, 1)
      my_body.set_mass(my_mass)

.. only:: cpp

   .. code-block:: cpp

      #include "odeBody.h"
      #include "odeMass.h"

      OdeBody my_body (my_world);
      my_body.set_position(some_panda_object.get_pos(render));
      my_body.set_quaternion(some_panda_object.get_quat(render));
      OdeMass my_mass;
      my_mass.set_box(11340, 1, 1, 1);
      my_body.set_mass(my_mass);

First, the position and quaternion are set of the body, this is directly copied
from the NodePath's pos and quat; do note that when using get_pos and get_quat,
you need to get them in global coordinate space, this is done here by specifying
``render`` as first argument.

Then, a mass is set for the body. The first argument specified in the set_box
call is the `density <https://en.wikipedia.org/wiki/Density>`__ of the object,
the second is the dimensions (lx, ly, lz) of the box. Each material has it's own
density, for example, water has a density of 1000 kg/m³, copper usually between
8920 and 8960 kg/m³. The value shown in the example above is the density for
lead.

There are of course cases where you don't know the density (although it is easy
to calculate), or when the object is not easy to fit in a box shape. OdeMass
provides the following methods:

.. currentmodule:: panda3d.core

.. py:method:: OdeMass.set_zero()
   :noindex:

   Sets all the mass parameters to 0, meaning it will have no mass at all.

.. py:method:: OdeMass.set_sphere(density, radius)
   :noindex:

   This specifies that the object's mass is spherical with the given radius.

.. py:method:: OdeMass.set_sphere_total(total_mass, radius)
   :noindex:

   Use this if you don't know the density but do know the total mass of the
   object.

.. py:method:: OdeMass.set_box(density, lx, ly, lz)
   :noindex:

   Use this for box-shaped objects.

.. py:method:: OdeMass.set_box_total(total_mass, lx, ly, lz)
   :noindex:

   The same as the former, but specifies the total mass instead of the density.

.. py:method:: OdeMass.set_cylinder(density, direction, radius, length)
   :noindex:

   To be used for objects shaped like a cylinder.

.. py:method:: OdeMass.set_cylinder_total(total_mass, direction, radius, length)
   :noindex:

   Again the same cylinder, but specifies the mass instead of the density.

.. py:method:: OdeMass.set_capsule(density, direction, radius, length)
   :noindex:

   A capsule is similar to a cylinder, but has capped edges.

.. py:method:: OdeMass.set_capsule_total(total_mass, direction, radius, length)
   :noindex:

   Use this if you only have a mass and not the density.

.. py:method:: OdeMass.add(other)
   :noindex:

   Adds an other OdeMass object to this mass.

.. py:method:: OdeMass.adjust(total_mass)
   :noindex:

   Adjusts the mass parameters to have the specified total mass.

.. py:method:: OdeMass.rotate(matrix)
   :noindex:

   Rotates the matrix using the specified Mat3 object.

More methods are listed on the :class:`~panda3d.ode.OdeMass` page in the API
Reference.

For more complex shapes, you might want to decompose the object into several
simple ones, and use the ``add(other)`` method to add the masses together. If
that still isn't enough, you might want to set the individual parameters of the
mass using ``set_parameters``, which is not explained here because it that goes
beyond the scope of this manual page. Note that the shape you set is not
actually used for collisions: it's just used to roughly determine how the mass
is divided in the object.
