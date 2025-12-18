.. _particle-intervals:

Particle Intervals
==================

Particle effects can be run from inside intervals as well, using the
:py:class:`~direct.interval.ParticleInterval.ParticleInterval` class:

.. code-block:: python

   interval_name = ParticleInterval(
       particle_effect,
       parent,
       world_relative=True,
       duration=my_duration
   )

Read more about :ref:`particle-effects`.
