.. _actor-intervals:

Actor Intervals
===============

.. only:: python

   Actor intervals allow actor animations to be played as an interval, which
   allows them to be combined with other intervals through sequences and
   parallels.

   The subrange of the animation to be played may be specified via frames
   (``start_frame`` up to and including ``end_frame``) or seconds (``start_time``
   up to and including ``end_time``). It may also be specified with a
   ``start_frame`` or ``start_time`` in conjunction with the duration, in seconds.
   If none of these is specified, then the default is to play the entire range
   of the animation.

   If ``end_frame`` is before ``start_frame``, or if the play rate is negative,
   then the animation will be played backwards.

   You may specify a subrange that is longer than the actual animation, but if
   you do so, you probably also want to specify either ``loop=1`` or
   ``constrained_loop=1``; see below.

   The loop parameter is a boolean value. When it is true, it means that the
   animation restarts and plays again if the interval extends beyond the
   animation's last frame. When it is false, it means that the animation stops
   and holds its final pose when the interval extends beyond the animation's
   last frame. Note that, in neither case, will the ActorInterval loop
   indefinitely: all intervals always have a specific, finite duration, and the
   duration of an ActorInterval is controlled by either the duration parameter,
   the ``start_time``/``end_time`` parameters, or the ``start_frame``/``end_frame``
   parameters. Setting ``loop=1`` has no effect on the duration of the
   ActorInterval, it only controls what the actor does if you try to play past
   the end of the animation.

   The parameter ``constrained_loop`` works similarly to loop, but while
   ``loop=1`` implies a loop within the entire range of animation,
   ``constrained_loop=1`` implies a loop within ``start_frame`` and ``end_frame``
   only. That is, if you specify ``loop=1`` and the animation plays past
   ``end_frame``, in the next frame it will play beginning at frame 0; while if
   you specify ``constrained_loop=1`` instead, then the next frame after
   ``end_frame`` will be ``start_frame`` again.

   All parameters other than the animation name are optional.

   .. code-block:: python

      from direct.interval.ActorInterval import ActorInterval

      my_interval = myactor.actor_interval(
          "Animation Name",
          loop=<0 or 1>,
          constrained_loop=<0 or 1>,
          duration=D,
          start_time=T1,
          end_time=T2,
          start_frame=N1,
          end_frame=N2,
          play_rate=R,
          part_name=PN,
          lod_name=LN,
      )

.. only:: cpp

   As ActorInterval is implemented in Python, this section does not apply to C++.
