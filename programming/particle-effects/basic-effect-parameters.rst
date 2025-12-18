.. _particle-effect-basic-parameters:

Particle Effect Basic Parameters
================================

Every particle effect needs at least eleven parameters. These govern the
overall properties, such as the number of particles on the screen, the birth
and death rates, and the renderer, emitter, and factory that are used.

=============================== ========================================= =============
Variable                        Definition                                Values
=============================== ========================================= =============
pool_size                        Maximum number of simultaneous particles  [0, infinity)
birth_rate                       Seconds between particle births           (0, infinity)
litter_size                      Number of particles created at each birth [1, infinity)
litter_spread                    Variation of litter size                  [0, infinity)
local_velocity_flag               Whether or not velocities are absolute    Boolean
system_grows_older                Whether or not the system has a lifespan  Boolean
system_lifespan                  Age of the system in seconds              [0, infinity)
BaseParticleRenderer\* renderer Pointer to particle renderer              Renderer type
BaseParticleRenderer\* emitter  Pointer to particle emitter               Emitter type
BaseParticleRenderer\* factory  Pointer to particle factory               Factory type
=============================== ========================================= =============

The renderer, emitter, and factory types will be discussed in the next three
sections.
