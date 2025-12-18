.. _evade:

Evade
=====

'Evade' is an AI behavior where an AICharacter will move in the opposite
direction to a target NodePath or position.

https://www.youtube.com/watch?v=JchuRRHqPUQ

In PandAI, 'Evade' is defined as :

.. code-block:: python

   ai_behaviors.evade(NodePath target, double panic_distance, double relax_distance, float priority)

where :

Panic Distance is the radius of detection.

Relax Distance is the distance from the panic distance radius after which the
object should stop evading once evade has been initiated.

priority is by default set to 1.0 and is used when using two or more steering
behaviors on an AICharacter.

--------------

The velocity at which the AICharacter evades is determined when you first
create your AICharacter object using the AICharacter constructor.

-  Note: 'Evade' recalculates the direction every frame and so is less
   efficient than Flee for a static object.

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
           base.cam.set_pos_hpr(0, 0, 55, 0, -90, 0)

           self.load_models()
           self.set_ai()
           self.set_movement()

       def load_models(self):
           # Seeker
           ralph_start_pos = Vec3(-10, 0, 0)
           self.evader = Actor("models/ralph",
                               {"run":"models/ralph-run"})
           self.evader.reparent_to(render)
           self.evader.set_scale(0.5)
           self.evader.set_pos(ralph_start_pos)
           # Target
           self.target = loader.load_model("models/arrow")
           self.target.set_color(1,0,0)
           self.target.set_pos(5,0,0)
           self.target.set_scale(1)
           self.target.reparent_to(render)

       def set_ai(self):
           #Creating AI World
           self.AIworld = AIWorld(render)

           self.AIchar = AICharacter("evader",self.evader, 100, 0.05, 5)
           self.AIworld.add_ai_char(self.AIchar)
           self.AIbehaviors = self.AIchar.get_ai_behaviors()

           self.AIbehaviors.evade(self.target, 5, 5)
           self.evader.loop("run")

           #AI World update
           task_mgr.add(self.AIUpdate, "AIUpdate")

       #to update the AIWorld
       def AIUpdate(self,task):
           self.AIworld.update()
           return Task.cont

       #All the movement functions for the Target
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

https://sites.google.com/site/etcpandai/documentation/steering-behaviors/evade/PandAIEvadeExample.zip?attredirects=0&d=1
