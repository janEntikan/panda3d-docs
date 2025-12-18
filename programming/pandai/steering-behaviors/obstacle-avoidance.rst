.. _obstacle-avoidance:

Obstacle Avoidance
==================

'Obstacle Avoidance' is a behavior where an AI Character steers away from
obstacles in its path.

https://www.youtube.com/watch?v=xZnuWRiKL6I

--------------

In PandAI, obstacle avoidance is defined as :

.. code-block:: python

   ai_behaviors.obstacle_avoidance(float feeler_length)

Feeler length is the
range at which the obstacle can be detected by the AI Character

(Note : This does not correspond to actual length in render. The algorithm
computes the feeler’s length based on AI Character’s speed and size and also
the Obstacle size and the feeler length which is input to it simply a
multiplier)

--------------

For the algorithm to work, the obstacles need to be added to the world like
this :

.. code-block:: python

   ai_world.add_obstacle(NodePath  obstacle)

Also you can
remove an obstacle at any time needed by using

.. code-block:: python

   ai_world.remove_obstacle(NodePath obstacle)

--------------

The full working code in Panda3D is :

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
       return OnscreenText(text=msg, style=1, fg=(1,1,1,1), font = font,
                           pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

   class World(DirectObject):

       def __init__(self):
           base.disable_mouse()
           base.cam.set_pos_hpr(0,0,55,0,-90,0)

           self.load_models()
           self.set_ai()
           self.set_movement()

       def load_models(self):
           # Seeker
           ralph_start_pos = Vec3(-10, 0, 0)
           self.pursuer = Actor("models/ralph",
                                    {"run":"models/ralph-run"})
           self.pursuer.reparent_to(render)
           self.pursuer.set_scale(0.5)
           self.pursuer.set_pos(ralph_start_pos)
           # Target
           self.target = loader.load_model("models/arrow")
           self.target.set_color(1,0,0)
           self.target.set_pos(5,0,0)
           self.target.set_scale(1)
           self.target.reparent_to(render)
           # Obstacle 1
           self.obstacle1 = loader.load_model("models/arrow")
           self.obstacle1.set_color(0,0,1)
           self.obstacle1.set_pos(2,0,0)
           self.obstacle1.set_scale(1)
           self.obstacle1.reparent_to(render)
           # Obstacle 2
           self.obstacle2 = loader.load_model("models/arrow")
           self.obstacle2.set_color(0,0,1)
           self.obstacle2.set_pos(5,5,0)
           self.obstacle2.set_scale(1)
           self.obstacle2.reparent_to(render)

           self.pursuer.loop("run")

       def set_ai(self):
           #Creating AI World
           self.AIworld = AIWorld(render)

           self.AIchar = AICharacter("pursuer",self.pursuer, 100, 0.05, 5)
           self.AIworld.add_ai_char(self.AIchar)
           self.AIbehaviors = self.AIchar.get_ai_behaviors()

           self.AIbehaviors.pursue(self.target)

           # Obstacle avoidance
           self.AIbehaviors.obstacle_avoidance(1.0)
           self.AIworld.add_obstacle(self.obstacle1)
           self.AIworld.add_obstacle(self.obstacle2)

           #AI World update
           task_mgr.add(self.AIUpdate,"AIUpdate")

       #to update the AIWorld
       def AIUpdate(self,task):
           self.AIworld.update()
           return Task.cont

       #All the movement functions for the Target
       def set_movement(self):
           self.key_map = {"left":0, "right":0, "up":0, "down":0}
           self.accept("arrow_left", self.set_key, ["left",1])
           self.accept("arrow_right", self.set_key, ["right",1])
           self.accept("arrow_up", self.set_key, ["up",1])
           self.accept("arrow_down", self.set_key, ["down",1])
           self.accept("arrow_left-up", self.set_key, ["left",0])
           self.accept("arrow_right-up", self.set_key, ["right",0])
           self.accept("arrow_up-up", self.set_key, ["up",0])
           self.accept("arrow_down-up", self.set_key, ["down",0])
           #movement task
           task_mgr.add(self.Mover,"Mover")

           add_instructions(0.9, "Use the Arrow keys to move the Red Target")

       def set_key(self, key, value):
           self.key_map[key] = value

       def Mover(self,task):
           start_pos = self.target.get_pos()
           if (self.key_map["left"]!=0):
                   self.target.set_pos(start_pos + Point3(-speed,0,0))
           if (self.key_map["right"]!=0):
                   self.target.set_pos(start_pos + Point3(speed,0,0))
           if (self.key_map["up"]!=0):
                   self.target.set_pos(start_pos + Point3(0,speed,0))
           if (self.key_map["down"]!=0):
                   self.target.set_pos(start_pos + Point3(0,-speed,0))

           return Task.cont

   w = World()
   run()

To get the full working
demo, please visit :

https://sites.google.com/site/etcpandai/documentation/steering-behaviors/obstacle-avoidance/PandAIObstacleAvoidanceExample.zip?attredirects=0&d=1
