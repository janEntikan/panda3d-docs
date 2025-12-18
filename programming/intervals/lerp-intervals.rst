.. _lerp-intervals:

Lerp Intervals
==============

The "lerp interval" is the main workhorse of the Interval system. The word
"lerp" is short for "linearly interpolate" and means to smoothly adjust
properties, such as position, from one value to another over a period of time.
You can use lerp intervals to move and rotate objects around in your world.
The lerp interval is also the most complex of all of the intervals, since
there are many different parameters that you might want to specify to control
the lerp.

.. only:: python

   An overview of the NodePath-based LerpIntervals
   -----------------------------------------------

   Most ``LerpIntervals`` adjust the various transform properties of a
   ``NodePath``, such as ``pos``, ``hpr``, and ``scale``, and they all have a
   similar form. Consider the ``LerpPosInterval``, which will smoothly move a
   model from one point in space to another:

   .. code-block:: python

      from direct.interval.LerpInterval import LerpPosInterval
      i = LerpPosInterval(node_path,
                          duration,
                          pos,
                          start_pos=None,
                          other=None,
                          blend_type='no_blend',
                          bake_in_start=1,
                          fluid=0,
                          name=None)

   The only required parameters are the model whose position is being changed,
   the length of time to apply the move, and the model's new position. The
   remaining parameters are all optional and are often omitted. Here is a
   breakdown of what each parameter means:

   node_path
      The model whose position is being changed.

   duration
      The duration of the lerp in seconds.

   pos
      The model's target position (the new position it will move to). Usually
      this is a ``Point3(x, y, z)``, but as a special advanced feature, it might
      be a Python function that, when called, returns a ``Point3``. If it is a
      function, then it will be called at the time the lerp actually begins to
      play.

   start_pos
      The starting position of the model at the beginning of the lerp. If this
      is omitted, the model will start from its current position. As with
      ``pos``, above, this might be a Python function, which will be called at
      the time the lerp actually begins.

      Note that if you intend to move an object from its current position, it is
      better to omit this parameter altogether rather than try to specify it
      explicitly with something like ``start_pos=object.get_pos()`` since the
      latter will be evaluated at the time the interval is created; not when it
      is played. This is especially true if you plan to embed a series of
      consecutive ``LerpIntervals`` within a
      :ref:`Sequence <sequences-and-parallels>`.

   other
      Normally this is set to None to indicate a normal lerp. If a ``NodePath``
      is passed in, however, it indicates that this is a relative lerp, and the
      ``pos`` and ``start_pos`` will be computed as a relative transform from
      that ``NodePath``. The relative transform is recomputed each frame, so if
      the other ``NodePath`` is animating during the lerp, the animation will be
      reflected here. For this reason, you should not attempt to lerp a model
      relative to itself.

   blend_type
      This specifies how smoothly the lerp starts and stops. It may be any of
      the following values:

      +-----------------+------------------------------------------------------+
      | ``'ease_in'``    | The lerp begins slowly, ramps up to full speed, and  |
      |                 | stops abruptly.                                      |
      +-----------------+------------------------------------------------------+
      | ``'ease_out'``   | The lerp begins at full speed, and then slows to a   |
      |                 | gentle stop at the end.                              |
      +-----------------+------------------------------------------------------+
      | ``'ease_in_out'`` | The lerp begins slowly, ramps up to full speed, and  |
      |                 | then slows to a gentle stop.                         |
      +-----------------+------------------------------------------------------+
      | ``'no_blend'``   | The lerp begins and ends abruptly.                   |
      +-----------------+------------------------------------------------------+

   bake_in_start
      This is an advanced feature. Normally this is 1, which means the original
      starting position of the model is determined when the interval starts to
      play and saved for the duration of the interval. You almost always want to
      keep it that way. If you pass this as 0, however, the starting position is
      cleverly re-inferred at each frame, based on the model's current position
      and the elapsed time in the lerp; this allows your application to move the
      model even while it is being lerped, and the lerp will adapt. This has
      nothing to do with controlling when the ``start_pos`` parameter is
      evaluated.

   fluid
      If this is 1, then the lerp uses ``set_fluid_pos()`` rather than
      ``set_pos()`` to animate the model. See :ref:`rapidly-moving-objects`.
      This is meaningful only when the collision system is currently active on
      the model. Since usually there is no reason to have the collision system
      active while a model is under direct application control, this parameter
      is rarely used.

   name
      This specifies the name of the lerp, and may be useful for debugging.
      Also, by convention, there may only be one lerp with a given name playing
      at any given time, so if you put a name here, any other interval with the
      same name will automatically stop when this one is started. The default is
      to assign a unique name for each interval.

   Convenience Short-Hands
   -----------------------

   Various convenience methods are defined on the NodePath class which provide
   a short-hand syntax for creating a LerpInterval for that NodePath.
   These are called ``pos_interval()``, ``hpr_interval()``, ``quat_interval``, and
   so on. As an example:

   .. code-block::

      # This lets the actor move to point 10, 10, 10 in 1.0 second.
      my_interval1 = my_actor.pos_interval(1.0, Point3(10, 10, 10))

      # This move takes 2.0 seconds to complete.
      my_interval2 = my_actor.pos_interval(2.0, Point3(8, -5, 10))

      # You can specify a starting position, too.
      my_interval3 = my_actor.pos_interval(1.0, Point3(2, -3, 8), start_pos=Point3(2, 4, 1))

      # This rotates the actor 180 degrees on heading and 90 degrees on pitch.
      my_interval4 = my_actor.hpr_interval(1.0, Vec3(180, 90, 0))

   The rest of the NodePath-based LerpIntervals
   --------------------------------------------

   Many ``NodePath`` properties other than position may be controlled via a
   lerp. Here is the list of the various ``LerpIntervals`` that control
   ``NodePath`` properties:

   .. code-block:: python

      LerpPosInterval(node_path, duration, pos, start_pos)
      LerpHprInterval(node_path, duration, hpr, start_hpr)
      LerpQuatInterval(node_path, duration, quat, start_hpr, start_quat)
      LerpScaleInterval(node_path, duration, scale, start_scale)
      LerpShearInterval(node_path, duration, shear, start_shear)
      LerpColorInterval(node_path, duration, color, start_color)
      LerpColorScaleInterval(node_path, duration, color_scale, start_color_scale)

   Each of the above has a similar set of parameters as those of
   ``LerpPosInterval``. They also have a similar shortcut (e.g.
   ``model.hpr_interval()``, etc.) Finally, there is a handful of combination
   ``LerpIntervals`` that perform multiple lerps at the same time. (You can also
   achieve the same effect by combining several ``LerpIntervals`` within a
   :ref:`Parallel <sequences-and-parallels>`, but these combination intervals
   are often simpler to use, and they execute just a bit faster.)

   .. code-block:: python

      LerpPosHprInterval(node_path, duration, pos, hpr, start_pos, start_hpr)
      LerpPosQuatInterval(node_path, duration, pos, quat, start_pos, start_quat)
      LerpHprScaleInterval(node_path, duration, hpr, scale, start_hpr, start_scale)
      LerpQuatScaleInterval(node_path, duration, quat, scale, start_quat, start_scale)
      LerpPosHprScaleInterval(node_path, duration, pos, hpr, scale, start_pos, start_hpr, start_scale)
      LerpPosQuatScaleInterval(node_path, duration, pos, quat, scale, start_pos, start_quat, start_scale)
      LerpPosHprScaleShearInterval(node_path, duration, pos, hpr, scale, shear, start_pos, start_hpr, start_scale, start_shear)
      LerpPosQuatScaleShearInterval(node_path, duration, pos, quat, scale, shear, start_pos, start_quat, start_scale, start_shear)

   Other types of LerpInterval
   ---------------------------

   Beyond animating NodePaths, you can create a ``LerpInterval`` that blends any
   parameter of any object over time. This can be done with a
   ``LerpFunctionInterval``:

   .. code-block:: python

      def my_function(t):
          # Do something based on t.

      i = LerpFunc(my_function,
                   from_data=0,
                   to_data=1,
                   duration=0.0,
                   blend_type='no_blend',
                   extra_args=[],
                   name=None)

   This advanced interval has many things in common with all of the above
   ``LerpIntervals``, but instead of directly animating a value, it instead
   calls the function you specify, passing a single floating-point parameter,
   ``t``, that ranges from ``from_data`` to ``to_data`` over the duration of the
   interval. It is then up to your function to set whatever property of whatever
   object you like according to the current value of ``t``.

.. only:: cpp

   See the API reference for :class:`.CLerpNodePathInterval` to understand how
   to construct such an interval.
