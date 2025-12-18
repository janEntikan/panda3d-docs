.. _projectile-intervals:

Projectile Intervals
====================

Projectile intervals are used to move a NodePath through the trajectory of a
projectile under the influence of gravity.

.. code-block:: python

   my_interval = ProjectileInterval(<Node Path>,
       start_pos=Point3(X, Y, Z), end_pos=Point3(X, Y, Z),
       duration=<Time in seconds>, start_vel=Point3(X, Y, Z),
       end_z=Z, gravity_mult=<multiplier>, name=<Name>)

All parameters don't have to be specified. Here are a combination of parameters
that will allow you to create a projectile interval. (If start_pos is not
provided, it will be obtained from the node's position at the time that the
interval is first started. Note that in this case you must provide a duration.)

-  start_pos, end_pos, duration - go from start_pos to end_pos in duration seconds
-  start_pos, start_vel, duration - given a starting velocity, go for a specific
   time period
-  start_pos, start_vel, end_z - given a starting velocity, go until you hit a
   given Z plane

In addition you may alter gravity by providing a multiplier in 'gravity_mult'.
'2' will make gravity twice as strong, '.5' half as strong.'-1' will reverse
gravity.

Here's a little snippet of code that will demonstrate projectile intervals:

.. code-block:: python

   camera.set_pos(0,-45,0)

   # load the ball model
   self.ball = loader.load_model("smiley")
   self.ball.reparent_to(render)
   self.ball.set_pos(-15,0,0)

   # setup the projectile interval
   self.trajectory = ProjectileInterval(self.ball, duration=1,
                                        start_pos=Point3(-15,0,0),
                                        end_pos=Point3(15,0, 0))
   self.trajectory.loop()
