.. _flock:

Flock
=====

What is flocking? Flocking is an emergent behavior and is the resultant of the
following forces:

cohesion -- finds average position of neighbors and tries to move to that
position separation -- object keeps a certain distance between itself and its
neighbor alignment -- finds average direction in which all neighbors are moving
and tries to move in that direction

Each NPC has a "visibility cone" and this is used to compute it's neighbors.
The neighbors contribute towards the forces mentioned above.

Tuners:

1. The angle and length of each NPC's "visibility cone".
2. Weight of cohesion, separation, and alignment (how much each sub-behavior of
   flock affects the overall flocking behavior).

.. note::

   Flocking behavior is NOT a standalone behavior. It needs to be combined with
   other steering behaviors such as seek, pursue, flee, evade etc. to function.

https://www.youtube.com/watch?v=dkfnlqH06IY

--------------

Using PandAI's flocking system:

.. code-block:: python

   // To create the flock
   flock_object = Flock(unsigned int flock_id, double vcone_angle,
                       double vcone_radius, unsigned int cohesion_wt,
                       unsigned int separation_wt, unsigned int alignment_wt)

"flock_id" is a value identifying the flock.

"vcone_angle" is the visibility angle of the character (represented by a cone
around it)

"vcone_radius" is the length of the visibility cone.

"cohesion_wt", "separation_wt" and "alignment_wt" is the amount of separation
force that contributes to the overall flocking behavior.

--------------

Some standard values to start you off with:

Type vcone_angle vcone_radius separation_wt cohesion_wt alignment_wt

Normal Pack 270 10 2 4 1

Loose Pack 180 10 2 4 5

Tight Pack 45 5 2 4 5

You could try experimenting with your own values to customize your flock.

--------------

To add your AI Character to the above created flock

.. code-block:: python

   flock_object.add_ai_char(ai_char)     # ai_char is an AICharacter object.

After all the AI Characters are added to the flock, add the flock to the
world.

.. code-block:: python

   ai_world.add_flock(flock_object)    # ai_world is an AIWorld object.

Specify the flock behavior priority. As mentioned earlier, flock behavior
works with other steering behaviors.

.. code-block:: python

   # ai_behaviors is an AIBehaviors object.
   ai_behaviors.flock(float priority)

   # Turns the flock behavior off.
   ai_world.flock_off(unsigned int flock_id)

   # Turns the flock behavior on.
   ai_world.flock_on(unsigned int flock_id)

   # Removes the flock behavior.
   # Note: This does NOT remove the AI characters of the flock.
   ai_world.remove_flock(unsigned int flock_id)

   # Returns a handle to the flock object.
   ai_world.get_flock(unsigned int flock_id)

--------------

The full working code in Panda3D :

.. code-block:: python

   import direct.directbase.DirectStart
   from panda3d.core import *
   from direct.showbase.DirectObject import DirectObject
   from direct.task import Task
   from direct.actor.Actor import Actor
   #for Pandai
   from panda3d.ai import *
   #for Onscreen GUI
   from direct.gui.OnscreenText import OnscreenText

   # Globals
   speed = 0.75

   # Function to put instructions on the screen.
   font = loader.load_font("cmss12")
   def add_instructions(pos, msg):
       return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), font=font,
                           pos=(-1.3, pos), align=TextNode.ALeft, scale=.05)

   class World(DirectObject):

       def __init__(self):
           base.disable_mouse()
           base.cam.set_pos_hpr(0, 0, 85, 0, -90, 0)

           self.load_models()
           self.set_ai()
           self.set_movement()

       def load_models(self):
           # Seeker
           self.flockers = []
           for i in range(10):
               ralph_start_pos = Vec3(-10+i, 0, 0)
               self.flockers.append(Actor("models/ralph",
                                        {"run": "models/ralph-run"}))
               self.flockers[i].reparent_to(render)
               self.flockers[i].set_scale(0.5)
               self.flockers[i].set_pos(ralph_start_pos)
               self.flockers[i].loop("run")

           # Target
           self.target = loader.load_model("models/arrow")
           self.target.set_color(1,0,0)
           self.target.set_pos(0,20,0)
           self.target.set_scale(1)
           self.target.reparent_to(render)

       def set_ai(self):
           #Creating AI World
           self.AIworld = AIWorld(render)

           #Flock functions
           self.MyFlock = Flock(1, 270, 10, 2, 4, 0.2)
           self.AIworld.add_flock(self.MyFlock)
           self.AIworld.flock_on(1)

           self.AIchar = []
           self.AIbehaviors = []
           for i in range(10):
               char = AICharacter("flockers" + str(i), self.flockers[i], 100, 0.05, 5)
               self.AIchar.append(char)
               self.AIworld.add_ai_char(char)
               self.AIbehaviors.append(char.get_ai_behaviors())
               self.MyFlock.add_ai_char(char)
               self.AIbehaviors[i].flock(0.5)
               self.AIbehaviors[i].pursue(self.target, 0.5)

           #AI World update
           task_mgr.add(self.AIUpdate, "AIUpdate")

       #to update the AIWorld
       def AIUpdate(self, task):
           self.AIworld.update()
           return Task.cont

       # All the movement functions for the Target
       def set_movement(self):
           self.key_map = {"left": 0, "right": 0, "up": 0, "down": 0}
           self.accept("arrow_left", self.set_key, ["left", 1])
           self.accept("arrow_right", self.set_key, ["right", 1])
           self.accept("arrow_up", self.set_key, ["up", 1])
           self.accept("arrow_down", self.set_key, ["down", 1])
           self.accept("arrow_left-up", self.set_key, ["left", 0])
           self.accept("arrow_right-up", self.set_key, ["right", 0])
           self.accept("arrow_up-up", self.set_key, ["up", 0])
           self.accept("arrow_down-up", self.set_key, ["down", 0])
           #movement task
           task_mgr.add(self.Mover, "Mover")

           add_instructions(0.9, "Use the Arrow keys to move the Red Target")

       def set_key(self, key, value):
           self.key_map[key] = value

       def Mover(self,task):
           start_pos = self.target.get_pos()
           if self.key_map["left"] != 0:
                   self.target.set_pos(start_pos + Point3(-speed, 0, 0))
           if self.key_map["right"] != 0:
                   self.target.set_pos(start_pos + Point3(speed, 0, 0))
           if self.key_map["up"] != 0:
                   self.target.set_pos(start_pos + Point3(0, speed, 0))
           if self.key_map["down"] != 0:
                   self.target.set_pos(start_pos + Point3(0, -speed, 0))

           return Task.cont

   w = World()
   base.run()

To get the full working demo, please visit:

https://sites.google.com/site/etcpandai/documentation/steering-behaviors/flock/PandAIFlockExample.zip?attredirects=0&d=1
