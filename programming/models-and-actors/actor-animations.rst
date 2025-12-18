.. _actor-animations:

Actor Animations
================

Since the :class:`~direct.actor.Actor.Actor` class inherits from
:class:`.NodePath`, everything that can be done to a NodePath, such as
:meth:`~.NodePath.reparent_to()` and :meth:`~.NodePath.set_pos()`, etc., may
also be done to an Actor.
In addition to the basic NodePath functionality, Actors have several additional
methods to control animation. In order for Actors to animate, their pointer
(variable) must be retained in memory.
The following is only a brief introduction; see the API reference page for
:py:mod:`~direct.actor.Actor` for a complete list.

Basic animation playing
-----------------------

Animations may either be played or looped. When an animation is played, the
actor goes through the animation once. When an animation is looped, the
animation will play continuously. There is no tweening done between the last and
the first frame, so if an animation is going to be looped, it needs to be
constructed with that thought in mind. Finally, animations may be stopped at any
point. When an animation is stopped, the actor will stay in the position it
stopped on.

.. only:: python

   .. code-block:: python

      actor.play('Animation Name')
      actor.loop('Animation Name')
      actor.stop()

You may use the :py:meth:`~direct.actor.Actor.Actor.pose()` method to tell an
actor to hold a particular frame of the animation.
Frames are numbered beginning at 0.

.. only:: python

   .. code-block:: python

      actor.pose('Animation Name', FrameNumber)

Posing an actor to a frame doesn't automatically specify the start frame of the
next starting animation. Instead, if you don't want to start at the first frame,
you can specify these using the optional parameters ``from_frame`` and
``to_frame`` to the methods :py:meth:`~direct.actor.Actor.Actor.play()` and
:py:meth:`~direct.actor.Actor.Actor.loop()`:

.. only:: python

   .. code-block:: python

      actor.play('Animation Name', from_frame=10)
      actor.loop('Animation Name', from_frame=24, to_frame=36)

However, the loop method does have another optional parameter called
``restart``, which is 1 by default, meaning the animation will restart from the
beginning. If you pass it 0 instead, then the animation will begin looping from
the current frame:

.. only:: python

   .. code-block:: python

      actor.pose('Animation Name', 30)
      actor.loop('Animation Name', restart=0, from_frame=24, to_frame=36)

You can get more information about an animation with these functions:

.. only:: python

   .. code-block:: python

      print(actor.get_num_frames('Animation Name')) # returns the total number of frames in the animation
      print(actor.get_current_anim()) # returns a string containing the name of the current playing animation
      print(actor.get_current_frame('Animation Name')) # returns the current frame of the animation.

AnimControl
-----------

AnimControl is a class that provides control over a certain animation. You don't
need to use this but this could be useful if you want to have the animation
control functions over a certain animation in a separate class.

.. only:: python

   .. code-block:: python

      my_anim_control = actor.get_anim_control('Animation Name') #get the AnimControl

      my_anim_control.is_playing() #returns a boolean whether the animation is playing or not
      my_anim_control.get_frame() #returns the current frame number
      my_anim_control #returns the speed of the animation, in frames per second
      my_anim_control.get_full_fframe() #returns a floating-point frame number exceeding the framecount. Not recommended.
      my_anim_control.get_full_frame() #returns an integer frame number exceeding the framecount. Not recommended.
      my_anim_control.get_next_frame() #returns the number of the next frame on the queue.
      my_anim_control.get_num_frames() #returns the total number of frames
      my_anim_control.get_play_rate() #returns the playrate. explained further below
      my_anim_control.loop() #starts playing the animation in a loop
      my_anim_control.play() #starts playing the animation
      my_anim_control.pose(frame) #poses at frame frame
      my_anim_control.set_play_rate(rate) #sets the playrate. explained further below
      my_anim_control.stop() #stops the animation

Play rate
---------

The animation play rate may be set to any floating point value, which can be
used to speed up or slow down the animation. This is a scale factor on the base
animation rate; 1.0 means to play the animation at its normal speed, while 2.0
plays it twice as fast, and 0.5 plays it at half speed. It is also possible to
play an animation backwards by specifying a negative play rate, for instance
-1.0.

.. only:: python

   .. code-block:: python

      actor.set_play_rate(new_play_rate, 'Animation Name')

Blending
--------

Multiple different animations for an actor may be played at the same time, and
the animations blended together at runtime. The net result is that, each frame,
the actor ends up somewhere between the different poses it would be in for each
contributing animation, if each animation were playing independently.

Note that in blend mode each contributing animation still affects the actor's
entire body. If you want to play one animation on, say, the left arm, while a
different animation is playing on the legs, then you need to use half-body
animation, which is different from blending.

To use blending, you must first call ``enable_blend()`` to activate the blending
mode and indicate your intention to play multiple animations at once. While the
actor is in blend mode, playing a new animation does not automatically stop the
previously playing animation. Also, while in blend mode, you must explicitly
specify how much each animation contributes to the overall effect, with the
``set_control_effect()`` method (the default for each animation is 0.0, or no
contribution). For example:

.. only:: python

   .. code-block:: python

      actor.enable_blend()
      actor.set_control_effect('animation1', 0.2)
      actor.set_control_effect('animation2', 0.8)
      actor.loop('animation1')
      actor.loop('animation2')

The above specifies that 20% of animation1 and 80% of animation2 will be visible
on the character at the same time. Note that you still have to start both
animations playing (and they can be playing from different frames or at
different play rates). Starting or stopping an animation in blend mode does not
change its control effect; you must set an animation's control effect to 0.0 if
you don't want it to affect the actor anymore.

When you call :py:meth:`~direct.actor.Actor.Actor.stop()` in blend mode, you can
stop a particular animation by name, if you want; or you can stop all of the
animations by calling :py:meth:`~direct.actor.Actor.Actor.stop()` with no
parameters:

.. only:: python

   .. code-block:: python

      actor.stop('animation1')

Note that specifying an animation name to stop() is only meaningful when you are
in blend mode. When not in blend mode, actor.stop() will always stop whatever
animation is currently playing, regardless of the animation name you specify.

When you are done using blending and want to return to the normal mode of only
playing one animation at a time, call ``disable_blend()``:

.. only:: python

   .. code-block:: python

      actor.disable_blend()

Half-body animation
-------------------

If you want different parts of your actor to play separate animations without
blending them together you have to create subparts. Each of these can then play
one animation without influencing the others.
Call :py:meth:`actor.make_subpart() <direct.actor.Actor.Actor.make_subpart>` with
the desired name, a list of joints to be included and a list of joints to be
excluded in the subpart. Inclusion / exclusion will descend attached joints.
Exclude always overrides include.

.. code-block:: python

   actor.make_subpart("legs", ["Left Thigh", "Right Thigh"])
   actor.make_subpart("torso", ["Head"], ["Left Thigh", "Right Thigh"])

If you want to play an animation on a subpart make sure to pass the name.

.. code-block:: python

   actor.loop("walk", part_name="legs")
   actor.loop("reload", part_name="torso")

Interpolation
-------------

Intra-frame interpolation is also supported. If you play an animation with only
few frames per second you can see your model "jump" from one frame to the next.
If you enable interpolation between frames, those "jumps" will be smoothed out.
This allows smooth animations with framerates as low as one frame per second or
even less. Intra-frame interpolation is disabled by default. To enable it, just
add the following lines to your code

.. only:: python

   .. code-block:: python

      from panda3d.core import load_prc_file_data
      load_prc_file_data("", "interpolate-frames 1")

From the FAQ:

"Interpolate-frames flag gets set in the PartBundle at the time it is first
created, and then baked into the bam cache.

Thenceforth, later changes to the interpolate-frames variable mean nothing. If
you changed interpolate-frames flag, you will also need to empty your
model-cache folder.

Actually, it is not recommended to use interpolate-frames; it is a global
setting. It's better to achieve the same effect via
:py:meth:`actor.setBlend(frameBlend=True) <direct.actor.Actor.Actor.setBlend>`,
which is a per-actor setting (and doesn't get baked into the model-cache)."

Actor Intervals
---------------

Another way to play an animation on an actor is to use an
:ref:`ActorInterval <actor-intervals>`, which gives you a lot more
frame-by-frame control over the animation, and is particularly useful when
building a complex script using Intervals. However, the ActorInterval interface
is a little bit slower than the above interfaces at runtime, so you should
prefer the more fundamental interfaces unless there is a good reason to use
ActorInterval.

The Task Manager
----------------

On a more complex program, you may find that animations can not be loaded from
any point in your program. In any application there needs to be exactly one call
to :py:meth:`base.run() <direct.showbase.ShowBase.ShowBase.run>`, and it should
be the last thing you do after starting up. This starts the task manager.
Think of this as the main loop of the application: your startup procedure is to
set up your loading screen, start any initial tasks or intervals, hang any
initial messenger hooks, and then go get lost in :py:meth:`base.run()
<direct.showbase.ShowBase.ShowBase.run>`.
Thereafter everything must run in a :ref:`task <tasks-and-event-handling>`, in
an interval, or is a response to a message. This is true for both animations and
:ref:`sound <loading-and-playing-sounds-and-music>`.
