.. _simulating-the-physics-world:

Simulating the Physics World
============================

Simulating the physics scene
----------------------------

Now, we've only had some theory so far, but haven't seen any simulation yet. To
simulate, we will need to keep calling the ``quick_step(step_size)`` function on
the OdeWorld instance. step_size is how much time should be simulated in one
step. To get the most stable simulation, it is recommended that the step_size be
kept constant.

The problem with using the delta time of a task to step the simulation is that
the time between tasks might not be consistent. To get around this, a delta_time
accumulator is used to figure out how many steps must be taken. When a step is
performed, the world is iterated a few times, you can specify how much times the
world is being iterated by calling the ``set_quick_step_num_iterations(num)``
function on the OdeWorld instance.

Here's a small example showing a simple simulation showing an iron ball falling
from a ridge:

.. only:: python

   .. code-block:: python

      from direct.directbase import DirectStart
      from panda3d.ode import OdeWorld, OdeBody, OdeMass
      from panda3d.core import Quat

      # Load the cube where the ball will fall from
      cube = loader.load_model("box.egg")
      cube.reparent_to(render)
      cube.set_color(0.2, 0, 0.7)
      cube.set_scale(20)

      # Load the smiley model which will act as our iron ball
      sphere = loader.load_model("smiley.egg")
      sphere.reparent_to(render)
      sphere.set_pos(10, 1, 21)
      sphere.set_color(0.7, 0.4, 0.4)

      # Setup our physics world and the body
      world = OdeWorld()
      world.set_gravity(0, 0, -9.81)
      body = OdeBody(world)
      M = OdeMass()
      M.set_sphere(7874, 1.0)
      body.set_mass(M)
      body.set_position(sphere.get_pos(render))
      body.set_quaternion(sphere.get_quat(render))

      # Set the camera position
      base.disable_mouse()
      base.camera.set_pos(80, -20, 40)
      base.camera.look_at(0, 0, 10)

      # Create an accumulator to track the time since the sim
      # has been running
      delta_time_accumulator = 0.0
      # This step_size makes the simulation run at 90 frames per second
      step_size = 1.0 / 90.0

      # The task for our simulation
      def simulation_task(task):
          global delta_time_accumulator
          # Set the force on the body to push it off the ridge
          body.set_force(0, min(task.time**4 * 500000 - 500000, 0), 0)
          # Add the delta_time for the task to the accumulator
          delta_time_accumulator += base.clock.dt
          while delta_time_accumulator > step_size:
              # Remove a step_size from the accumulator until
              # the accumulated time is less than the stepsize
              delta_time_accumulator -= step_size
              # Step the simulation
              world.quick_step(step_size)
          # set the new positions
          sphere.set_pos_quat(render, body.get_position(), Quat(body.get_quaternion()))
          return task.cont

      task_mgr.do_method_later(1.0, simulation_task, "Physics Simulation")

      base.run()

.. only:: cpp

   .. code-block:: cpp

      // To keep the C++ samples short, we assume a running Panda environment,
      // with "framework", "window", "camera" and "taskMgr" variables in the
      // global scope. Likewise, only the includes relevant to this chapter
      // are shown. Check the beginning of the manual for a tutorial on making
      // a full Panda3D C++ app.
      // Sample entry point: simulation()

      #include "odeWorld.h"
      #include "odeBody.h"
      #include "odeMass.h"

      OdeBody *body;
      OdeWorld world;
      NodePath sphere;
      PT(ClockObject) clock = ClockObject::get_global_clock();

      // Create an accumulator to track the time since the sim
      // has been running
      float delta_time_accumulator = 0.0f;

      // This step_size makes the simulation run at 90 frames per second
      float step_size = 1.0f / 90.0f;

      AsyncTask::DoneStatus simulation_task(GenericAsyncTask *task, void *data);

      void simulation() {
        // Load the cube where the ball will fall from
        NodePath cube window->load_model(framework.get_models(), "models/box");
        cube.reparent_to(window->get_render());
        cube.set_scale(0.25, 0.25, 0.25);
        cube.set_pos(0, 0, 0);

        // Load the smiley model which will act as our iron ball
        sphere = window->load_model(framework.get_models(), "models/smiley");
        sphere.reparent_to(window->get_render());
        sphere.set_scale(0.25, 0.25, 0.25);
        sphere.set_pos(0, 0, 1);

        // Setup our physics world and the body
        world.set_gravity(0, 0, -9.81);
        body = new OdeBody(world);
        OdeMass M;
        M.set_sphere(7874, 1.0);
        body->set_mass(M);
        body->set_position(sphere.get_pos(window->get_render()));
        body->set_quaternion(sphere.get_quat(window->get_render()));

        // Set the camera position
        camera.set_pos(80, -20, 40);
        camera.look_at(0, 0, 0);

        PT(GenericAsyncTask) simulation_task_object =
          new GenericAsyncTask("startup task", &simulation_task, nullptr);
        simulation_task_object->set_delay(2);
        task_mgr->add(simulation_task_object);
      }

      // The task for our simulation
      AsyncTask::DoneStatus simulation_task (GenericAsyncTask *task, void *data) {
        // Set the force on the body to push it off the ridge
        body->set_force(0, min(pow(task->get_elapsed_time(),4) * 500000 - 500000, 0), 0);
        // Add the delta_time for the task to the accumulator
        delta_time_accumulator += clock->get_dt();
        while (delta_time_accumulator > step_size ) {
          // Remove a step_size from the accumulator until
          // the accumulated time is less than the stepsize
          delta_time_accumulator -= step_size;
          // Step the simulation
          world.quick_step(step_size);
        }
        // set the new positions
        sphere.set_pos_quat(window->get_render(),
          body->get_position(), body->get_quaternion());
        return AsyncTask::DS_cont;
      }
