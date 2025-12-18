.. _vehicles:

Bullet Vehicles
===============

Bullet comes with a simple vehicle controller, which can be used for arcade
style vehicle simulations. Instead of simulation of each wheel and chassis as
separate rigid bodies connected by joints, it simply uses a single rigid body
for the chassis. Collision detection for the wheels is approximated by ray
casts, and the tire friction is a basic anisotropic friction model. This
approach to vehicle modelling is called "raycast vehicle", and it is used
widely in commercial and non-commercial driving games.

Setup
-----

In order to create a vehicle we first have to create an ordinary dynamic rigid
body. This rigid body will serve as the vehicle chassis. Then we can create a
new instance of :class:`.BulletVehicle`. We have to pass the
:class:`.BulletWorld` and the :class:`.BulletRigidBodyNode` as arguments to the
vehicle constructor.

.. only:: python

   The following code snippet shows how this could be done.

   .. code-block:: python

      from panda3d.bullet import BulletVehicle

      # Chassis body
      shape = BulletBoxShape(Vec3(0.7, 1.5, 0.5))
      ts = TransformState.make_pos(Point3(0, 0, 0.5))

      chassis_np = render.attach_new_node(BulletRigidBodyNode('Vehicle'))
      chassis_np.node().add_shape(shape, ts)
      chassis_np.set_pos(0, 0, 1)
      chassis_np.node().set_mass(800.0)
      chassis_np.node().set_deactivation_enabled(False)

      world.attach_rigid_body(chassis_np.node())

      # Chassis geometry
      loader.load_model('path/to/model').reparent_to(chassis_np)

      # Vehicle
      vehicle = BulletVehicle(world, chassis_np.node())
      vehicle.set_coordinate_system(ZUp)
      world.attach_vehicle(vehicle)

Wheels
------

Once we have created the chassis and the vehicle we can add wheels to the
vehicle. We can create a new wheel using the ``create_wheel`` factory method of
the previously created vehicle. Once created we still have to configure the
wheel, that is set friction parameters, offset of the wheel hub with respect to
the chassis, axle direction and so on.

.. only:: python

   The following sample shows how to create and configure a wheel. In this case
   a front wheel is created. Front wheels are steerable.

   .. code-block:: python

      wheel_np = loader.load_model('path/to/model')
      wheel_np.reparent_to(render)

      wheel = vehicle.create_wheel()

      wheel.set_node(wheel_np.node())
      wheel.set_chassis_connection_point_cs(Point3(0.8, 1.1, 0.3))
      wheel.set_front_wheel(True)

      wheel.set_wheel_direction_cs(Vec3(0, 0, -1))
      wheel.set_wheel_axle_cs(Vec3(1, 0, 0))
      wheel.set_wheel_radius(0.25)
      wheel.set_max_suspension_travel_cm(40.0)

      wheel.set_suspension_stiffness(40.0)
      wheel.set_wheels_damping_relaxation(2.3)
      wheel.set_wheels_damping_compression(4.4)
      wheel.set_friction_slip(100.0)
      wheel.set_roll_influence(0.1)

Steering and Engine/Brake
-------------------------

Finally we need to control steering and engine/brakes. This is best done using a
task, and keeping the current steering angle around somewhere in a variable.

Here we use a very simple model of controlling the steering angle. If 'turn_left'
or 'turn_right' keys are pressed the steering angle will increase/decrease at a
constant rate, until a maximum steering angle is achieved. No relaxation is
applied. Therefor we also define constants for the maximum steering angle (here:
steering_clamp) and the rate at which the steering angle increases/decreases
(here: steering_increment).

The engine force and brake model shown is very simple too. If 'forward' is
pressed then the engine force will be the maximum engine force, otherwise engine
force will be zero. Likewise for the brakes.

Once the steering angle and engine/brake forces are determined they will be
applied to the wheels. Each wheel - addressed by it's index, i. e. 0 to 3 for a
four-wheel car - can be individually assigned values for steering and
engine/brake force. This way front/rear drives or four-wheel-drives can be
simulated.

.. only:: python

   The following code snippet shows pseudocode for controlling steering and
   engine/brakes.

   .. code-block:: python

      # Steering info
      steering = 0.0            # degree
      steering_clamp = 45.0      # degree
      steering_increment = 120.0 # degree per second

      # Process input
      engine_force = 0.0
      brake_force = 0.0

      if input_state.is_set('forward'):
          engine_force = 1000.0
          brake_force = 0.0

      if input_state.is_set('reverse'):
          engine_force = 0.0
          brake_force = 100.0

      if input_state.is_set('turn_left'):
          steering += dt * steering_increment
          steering = min(steering, steering_clamp)

      if input_state.is_set('turn_right'):
          steering -= dt * steering_increment
          steering = max(steering, -steering_clamp)

      # Apply steering to front wheels
      vehicle.set_steering_value(steering, 0)
      vehicle.set_steering_value(steering, 1)

      # Apply engine and brake to rear wheels
      vehicle.apply_engine_force(engine_force, 2)
      vehicle.apply_engine_force(engine_force, 3)
      vehicle.set_brake(brake_force, 2)
      vehicle.set_brake(brake_force, 3)

More realistic control models can be invented, in order to meet the control
requirements of individual driving games. For example:

-  Relaxing the steering angle to zero if the user does no hold down the left
   or right keys.
-  Reducing the maximum steering angle with increasing vehicle speed.
-  Setting engine force based on an analogue input, or alternatively based on
   the duration of the forward key being pressed down.

However, it is up to you do invent such controls. What Bullet requires is that
you provide the steering angle and the engine and brake force.
