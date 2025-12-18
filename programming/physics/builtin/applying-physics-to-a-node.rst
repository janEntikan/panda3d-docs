.. _applying-physics-to-a-node:

Applying physics to a node
==========================

To apply forces to a physical object, collect them into a ForceNode and then
apply them to the object. The ForceNode is a node that specifies the "context"
of the force; i.e. the local coordinate transform that determines the
direction of the force. Because ForceNodes are separate from ActorNodes, a
ForceNode can be placed in a different portion of the model tree from the
ActorNode to which the forces applies. This allows for forces to be applied
indirectly to a model (such as wind sweeping across the scene, or a mechanical
impulse from an appendage of the model) without having to do the calculations
necessary to transform from the ActorNode's coordinates to the coordinates of
the force's source.

To add a force to a physical object, add the force using either the
add_linear_force method (for translational forces) or the add_angular_force method
(for rotational forces):

.. code-block:: python

   actor_node.add_linear_force(pusher_force)
   actor_node.add_angular_force(spinner_force)

Conversely, forces can be removed using the corresponding remove calls:

.. code-block:: python

   actor_node.remove_linear_force(pusher_force)
   actor_node.remove_angular_force(spinner_force)

By default, linear forces don't factor in the mass of the object upon which
they act (meaning they are more like accelerations). To factor in the mass of
the object when applying the linear force, use the following call to enable
mass-dependent calculations:

.. code-block:: python

   pusher_force.set_mass_dependent(1)

Example 1: Gravity
------------------

To apply a gravitational pull to the "jetpack guy" from the previous example:

.. code-block:: python

   gravity_fn=ForceNode('world-forces')
   gravity_fnp=render.attach_new_node(gravity_fn)
   gravity_force=LinearVectorForce(0,0,-9.81) #gravity acceleration
   gravity_fn.add_force(gravity_force)

   base.physics_mgr.add_linear_force(gravity_force)

Since the gravitational force is relative to the entire world (and shouldn't
change if, for example, the jetpack guy tumbles head-over-heels), the
gravity_force vector was added to a ForceNode attached to render. So regardless
of the orientation of the NodePath controlled by an, the force will always pull
towards the bottom of the scene.

Since all objects in the scene should be affected by gravity, the force was
added to the set of forces managed by the PhysicsManager itself. Since forces
ignore the mass of the objects they act upon by default, this force will pull
all objects towards the ground at standard gravitational acceleration. The
next example shows how to apply a force to a single object.

Example 2: Rotary Thruster
--------------------------

Here is another example of applying forces to objects and the way in which the
ForceNode alters the effect:

.. code-block:: python

   thruster=NodePath("thruster") # make a thruster for the jetpack
   thruster.reparent_to(jetpack_guy)
   thruster.set_pos(0,-2,3)

   thruster_fn=ForceNode('jetpack_guy-thruster') # Attach a thruster force
   thruster_fnp=thruster.attach_new_node(thruster_fn)
   thruster_force=LinearVectorForce(0,0,4000)
   thruster_force.set_mass_dependent(1)
   thruster_fn.add_force(thruster_force)

   an.get_physical(0).add_linear_force(thruster_force)

   thruster.set_p(-45) # bend the thruster nozzle out at 45 degrees

When this force is applied to the jetpack guy, it will push upwards and
forwards. If the thruster's pitch and roll were controlled (say, by a
joystick), then the jetpack could be moved around merely by changing the pitch
and roll values; the ForceNode would inherit the orientation of the thruster
and automatically change the direction it pushes.

The effect that this thruster force has upon the jetpack guy should be
dependent upon the mass of the system, so the set_mass_dependent call is used to
factor mass into the acceleration analysis.
