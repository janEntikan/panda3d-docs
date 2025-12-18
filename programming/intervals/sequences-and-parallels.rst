.. _sequences-and-parallels:

Sequences and Parallels
=======================

You will need to have this import statement to use Sequences and Parallels.

.. code-block:: python

   from direct.interval.IntervalGlobal import *

Sequences and Parallels can control when intervals are played. Sequences play
intervals one after the other, effectively a “do in order” command. Parallels
are a “do together,” playing all intervals at the same time. Both have simple
formats, and every kind of interval may be used.

.. code-block:: python

   my_sequence = Sequence(my_interval1, ..., my_intervaln, name="Sequence Name")
   my_parallel = Parallel(my_interval1, ..., my_intervaln, name="Parallel Name")

To add to sequences or parallels after creating them, use the ``append`` method.

.. code-block:: python

   my_sequence.append(my_interval)
   my_parallel.append(my_interval)

Sequences and Parallels may also be combined for even greater control. Also,
there is a wait interval that can add a delay to Sequences. While it can be
defined beforehand, it does not have to be.

.. code-block:: python

   delay = Wait(2.5)
   panda_walk_seq =
       Sequence(
           Parallel(panda_walk, panda_walk_anim),
           delay,
           Parallel(panda_walk_back, panda_walk_anim),
           Wait(1.0),
           Func(my_function, arg1)
       )

In the above example, a wait interval is generated. After that, a Sequence is
made that uses a Parallel, the defined wait interval, another Parallel, and a
wait interval, and a call to the function function my_function is generated in
the Sequence. Such Sequences can get very long very quick, so it may be prudent
to define the internal Parallels and Sequences before creating the master
Sequence.

One can do very powerful things with Sequences and Parallels. Examine this
Sequence:

.. code-block:: python

   s = OnscreenImage('wav_is_playing.png')
   s.reparent_to(aspect2d)
   s.set_transparency(1)
   fade_in = s.color_scale_interval(3, (1, 1, 1, 1), (1, 1, 1, 0))
   fade_out = s.color_scale_interval(3, (1, 1, 1, 0))
   sound = loader.load_sfx('sound.wav')

   Sequence(
       fade_in,
       SoundInterval(sound),
       fade_out
   ).start()

   base.run()

It fades an image in, plays a sound, waits till sounds stops and then fades the
image out. Doing this conventional way would require a class to store state, a
task to check timings, and produce messy code.
