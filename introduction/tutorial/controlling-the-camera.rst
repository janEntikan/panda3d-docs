.. _controlling-the-camera:

Controlling the Camera
======================

Default Camera Control System
-----------------------------

By default, Panda3D runs a task that allows you to move the camera using the
mouse.

.. only:: cpp

   To enable it, use the following command:

   .. code-block:: cpp

      window->setup_trackball();

The keys to navigate are:

======================== ============================================
Mouse Button             Action
======================== ============================================
Left Button              Pan left and right.
Right Button             Move forwards and backwards.
Middle Button            Rotate around the origin of the application.
Right and Middle Buttons Roll the point of view around the view axis.
======================== ============================================

Go ahead and try this camera control system. The problem with it is that it is
sometimes awkward. It is not always easy to get the camera pointed in the
direction we want.

:ref:`Tasks <tasks>`
--------------------

Update the Code
~~~~~~~~~~~~~~~

Instead, we are going to write a *task* that controls the camera's position
explicitly. A *task* is nothing but a procedure that gets called every frame.
Update your code as follows:

.. only:: python

   .. literalinclude:: controlling-the-camera.py
      :language: python
      :linenos:

.. only:: cpp

   .. literalinclude:: controlling-the-camera.cxx
      :language: cpp
      :linenos:

The procedure ``task_mgr.add()`` tells Panda3D's task manager to call the
procedure ``spin_camera_task()`` every frame. This is a procedure that we have
written to control the camera. As long as the procedure ``spin_camera_task()``
returns the constant ``AsyncTask.DS_cont``, the task manager will continue to
call it every frame.

.. only:: cpp

   The object passed to :meth:`task_mgr->add() <.AsyncTaskManager.add>` is a
   C++ ``std::function`` object, which can be a lambda or separate function.
   If defined as a separate function, it should look like this:

   .. code-block:: cpp

      AsyncTask::DoneStatus your_task(AsyncTask *task) {
        // Do your stuff here.

        // Tell the task manager to continue this task the next frame.
        // You can also pass DS_done if this task should not be run again.
        return AsyncTask::DS_cont;
      }

   For more advanced usage, you can also subclass AsyncTask and override the
   ``do_task`` method to make it do what you want.

In our code, the procedure ``spin_camera_task()`` calculates the desired position
of the camera based on how much time has elapsed.
There is some NodePath power on display here. We calculate the desired orientation
of the camera using relativity. The camera rotates 6 degrees every second.
When the first argument to the :meth:`~.NodePath.set_pos()` call is another NodePath
it will be positioned relative to the NodePath. The same goes for :meth:`~.NodePath.set_hpr()`
The first line places the camera to render's center, without rotating it.
Then it rotates relative to itself. Then it takes a "step back", meaning it points at where it was.
This is an incredibly useful and a powerful way of easily making very complicated transformations.


Run the Program
~~~~~~~~~~~~~~~

The camera should no longer be underground; and furthermore, it should now be
rotating about the clearing:

.. image:: tutorial2.jpg
