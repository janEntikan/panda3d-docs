.. _steering-behaviors:

Steering Behaviors
==================

These AI behaviors control the basic motion of NPC objects in a game and make
it look realistic.

PandAI is inbuilt with handling the functionality of the seven following basic
steering behaviors :

Seek

Flee

Pursue

Evade

Arrival

Wander

Flock

Obstacle Avoidance

Path Follow

Before you start exploring these various behaviors, let me give you a brief
introduction on how it is setup and what you need to begin :

All the Steering Behaviors are part of the Behavior class of any AI Character.
Hence, to use them you need to get a reference to it via 'get_ai_behaviors()'
function of the AICharacter class.

Once you get this reference, you can use it to call any steering behavior.

.. code-block:: python

   ai_behaviors = ai_character.get_ai_behaviors();
   ai_behaviors.seek(target_node_path);

-  Once you have read this page, you can proceed to explore the individual
   pages for each AI Behavior for details and even an example demo for each
   one working.

--------------

PRIORITIES :

Every steering behavior can also take a second parameter which is priority.
This ranges from 0 to 1 and it defines the behaviors intensity when combined
with other behaviors.

.. code-block:: python

   ai_behaviors.seek(targetNodePath_1, 0.5);
   ai_behaviors.flee(targetNodePath_2, 0.5);

This will cause the AICharacter's resultant force to be an equal balance of
seeking 'targetNodePath_1' and fleeing 'targetNodePath_2'.

--------------

HELPER FUNCTIONS :

(For beginners -> Come back to these when you need this functionality)

For the AIWorld class:

.. code-block:: cpp

   void add_ai_char(AICharacter ai_char);

   void remove_ai_char(string name);

   void add_flock(Flock *flock);

   void flock_off(int ID);

   void flock_on(int ID);

   Flock get_flock(int ID);

For the AICharacter class:

.. code-block:: cpp

   double get_mass();

   void set_mass(double m);

   LVecBase3 get_velocity();

   double get_max_force();

   void set_max_force(double max_force);

   NodePath get_node_path();

   void set_node_path(NodePath np);

For the AIBehaviors class:

.. code-block:: python

   ai_behaviors.behavior_status(string AIName)

This function
returns the status of an AI Behavior whether it is active, paused, done or
disabled. Returns -1 if an invalid string is passed.

-  Note for pathfinding status, use pathfollow as the string name, since
   pathfinding is a subset of pathfollow.

To remove any AI after their call has been instantiated.

.. code-block:: python

   void remove_ai(string "AIName");

-  Note for pathfinding removal, use pathfollow as the string name, since
   pathfinding is a subset of pathfollow.

To pause or resume any AI after their call has been instantiated.

.. code-block:: python

   void pause_ai(string "AIName");

   void resume_ai(string "AIName");

where AIName refers to:

"all" - removes all the Ai's

"seek" - removes seek

"flee" - removes flee

"pursue" - removes arrival

"evade" - removes pursuit

"arrival" - removes evade

"wander" - removes wander

"flock" - removes flock

"obstacle_avoidance" - removes obstacle_avoidance

"pathfollow" - removes pathfollow

--------------

.. toctree::
   :maxdepth: 2

   seek
   flee
   pursue
   evade
   wander
   flock
   obstacle-avoidance
   path-follow
