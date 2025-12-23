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
procedure ``spin_pivot_task()`` every frame. This is a procedure that we have
written to control the camera. As long as the procedure ``spin_pivot_task()``
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

In our code, the procedure ``spin_pivot_task()`` calculates the desired position
of the camera based on how much time has elapsed. There is some NodePath power on display here. We reparent the camera to a new NodePath we will call a pivot (but you can call it anything you want). We rotate this new parent instead. Because the camera is parented to it will rotate along with it. By then offsetting the camera position it will rotate around the pivot.

You can imagine the pivot as being a large rotating disk that you stand in the middle of, then you walk to a different position on the disk. Can you imagine how you are now rotating around the center of the disk? Don't get dizzy! This is one of the advantages of using a SceneGraph and allows you to do very complicated transformations without having to resort to complex math.

When the first argument to the :meth:`~.NodePath.set_pos()` (or any other transformation) call is another NodePath, it will be transformed relative to that NodePath. We rotate the pivot relative to itself in this case, meaning it will be spinning.


Run the Program
~~~~~~~~~~~~~~~

The camera should no longer be underground; and furthermore, it should now be
rotating about the clearing:

.. image:: tutorial2.jpg
