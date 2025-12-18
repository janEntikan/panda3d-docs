.. _particle-factories:

Particle Factories
==================

There are two types of particle factories, Point and ZSpin. The particle panel
shows a third, Oriented, but this factory does not currently work. The
differences between these factories lie in the orientation and rotational
abilities. First, there are some common variables to the factories.

====================== ================================== =============
**Variable**           **Definition**                     **Values**
lifespan_base           Average lifespan in seconds        [0, infinity)
lifespan_spread         Variation in lifespan              [0, infinity)
mass_base               Average particle mass              [0, infinity)
mass_spread             Variation in particle mass         [0, infinity)
terminal_velocity_base   Average particle terminal velocity [0, infinity)
terminal_velocity_spread Variation in terminal velocity     [0, infinity)
====================== ================================== =============


Point particle factories generate simple particles. They have no additional
parameters. ZSpin particle factories generate particles that spin around the Z
axis, the vertical axis in Panda3D. They have some additional parameters.

================== ========================= ==========
**Variable**       **Definition**            **Values**
initial_angle       Starting angle in degrees [0, 360]
initial_angle_spread Spread of initial angle   [0, 360]
final_angle         Final angle in degrees    [0, 360]
fnal_angle_spread    Spread of final angle     [0, 360]
================== ========================= ==========
