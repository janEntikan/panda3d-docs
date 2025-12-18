.. _flee:

Flee
====

'Flee' is an AI behavior where an AICharacter will move in the opposite
direction to a target NodePath or position.

https://www.youtube.com/watch?v=sXzzuK2Vnnk

In PandAI, 'Flee' is defined as:

.. code-block:: python

   aiBehaviors.flee(NodePath target, double panic_distance, double relax_distance, float priority)
   aiBehaviors.flee(Vec3 position, double panic_distance, double relax_distance, float priority)

where:

Panic Distance is the radius of detection.

Relax Distance is the distance from the panic distance radius after which the
object should stop fleeing once flee has been initiated.

priority is by default set to 1.0 and is used when using two or more steering
behaviors on an AICharacter.

--------------

The velocity at which the AICharacter flees is determined when you first create
your AICharacter object using the AICharacter constructor.

-  Note: 'Flee' takes in a target or a position to be fled away from; this
   position should be static. (For moving objects use Evade).

--------------

A fully working flee demo :

.. code-block:: python

   import direct.directbase.DirectStart
   from panda3d.core import *
   from direct.showbase.DirectObject import DirectObject
   from direct.task import Task
   from direct.actor.Actor import Actor
   #for Pandai
   from panda3d.ai import *

   class World(DirectObject):

       def __init__(self):
           base.disable_mouse()
           base.cam.set_pos_hpr(0,0,55,0,-90,0)

           self.load_models()
           self.set_ai()

       def load_models(self):
           # Seeker
           ralph_start_pos = Vec3(2, 0, 0)
           self.fleer = Actor("models/ralph",
                                    {"run":"models/ralph-run"})
           self.fleer.reparent_to(render)
           self.fleer.set_scale(0.5)
           self.fleer.set_pos(ralph_start_pos)
           # Target
           self.target = loader.load_model("models/arrow")
           self.target.set_color(1,0,0)
           self.target.set_pos(5,0,0)
           self.target.set_scale(1)
           self.target.reparent_to(render)

       def set_ai(self):
           #Creating AI World
           self.AIworld = AIWorld(render)

           self.AIchar = AICharacter("fleer",self.fleer, 100, 0.05, 5)
           self.AIworld.add_ai_char(self.AIchar)
           self.AIbehaviors = self.AIchar.get_ai_behaviors()

           self.AIbehaviors.flee(self.target, 5, 5)
           self.fleer.loop("run")

           #AI World update
           task_mgr.add(self.AIUpdate,"AIUpdate")

       #to update the AIWorld
       def AIUpdate(self,task):
           self.AIworld.update()
           return Task.cont

   w = World()
   base.run()

--------------

To get a working demo of this example, please visit:

https://sites.google.com/site/etcpandai/documentation/steering-behaviors/flee/PandAIFleeExample.zip?attredirects=0&d=1
