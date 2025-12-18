.. _path-follow:

Path Follow
===========

'Path Follow' is a behavior where an AICharacter moves from one path to the
other without stopping at any path. It can be used for a patrolling type of
behavior.

https://www.youtube.com/watch?v=hIDyzUJgu2w

--------------

In PandAI, path follow is defined as :


.. code-block:: python

   ai_behaviors.path_follow(float priority)
   ai_behaviors.add_to_path(Vec3 position)

   ai_behaviors.start_follow() // Required to start the follow

Position is a point in
3D space which falls on the path which the AI Character needs to traverse.

(Note: that you need to add multiple positions to create a path say for
example Vec3(-10,10,0) Vec3(0,0,0) Vec3(10,10,0) Vec3(-10,10,0) will generate
a rectangular path in the XY plane)

Note: the add_to_path works backwards. So, your last call to add_to_path will be
your first position your AICharacter will go to.

--------------

The full working code in Panda3D is :


.. code-block:: python

   import direct.directbase.DirectStart
   from panda3d.core import *
   from direct.task import Task
   from direct.actor.Actor import Actor
   from panda3d.ai import *

   class World(object):

       def __init__(self):
           base.disable_mouse()
           base.cam.set_pos_hpr(0, 0, 55, 0, -90, 0)

           self.load_models()
           self.set_ai()

       def load_models(self):
           # Seeker
           ralph_start_pos = Vec3(-10, 0, 0)
           self.seeker = Actor("models/ralph",
                               {"run":"models/ralph-run"})
           self.seeker.reparent_to(render)
           self.seeker.set_scale(0.5)
           self.seeker.set_pos(ralph_start_pos)
           # Target1
           self.target1 = loader.load_model("models/arrow")
           self.target1.set_color(1,0,0)
           self.target1.set_pos(10,-10,0)
           self.target1.set_scale(1)
           self.target1.reparent_to(render)
           # Target2
           self.target2 = loader.load_model("models/arrow")
           self.target2.set_color(0,1,0)
           self.target2.set_pos(10,10,0)
           self.target2.set_scale(1)
           self.target2.reparent_to(render)
           # Target3
           self.target3 = loader.load_model("models/arrow")
           self.target3.set_color(0,0,1)
           self.target3.set_pos(-10,10,0)
           self.target3.set_scale(1)
           self.target3.reparent_to(render)
           # Target4
           self.target4 = loader.load_model("models/arrow")
           self.target4.set_color(1,0,1)
           self.target4.set_pos(-10,-10,0)
           self.target4.set_scale(1)
           self.target4.reparent_to(render)

           self.seeker.loop("run")

       def set_ai(self):
           # Creating AI World
           self.AIworld = AIWorld(render)

           self.AIchar = AICharacter("seeker", self.seeker, 60, 0.05, 5)
           self.AIworld.add_ai_char(self.AIchar)
           self.AIbehaviors = self.AIchar.get_ai_behaviors()

           # Path follow (note the order is reveresed)
           self.AIbehaviors.path_follow(1.0)
           self.AIbehaviors.add_to_path(self.target4.get_pos())
           self.AIbehaviors.add_to_path(self.target3.get_pos())
           self.AIbehaviors.add_to_path(self.target2.get_pos())
           self.AIbehaviors.add_to_path(self.target1.get_pos())

           self.AIbehaviors.start_follow()

           #AI World update
           task_mgr.add(self.AIUpdate, "AIUpdate")

       def AIUpdate(self,task):
           self.AIworld.update()
           return Task.cont

   w = World()
   base.run()

To get the full working demo, please visit:

https://sites.google.com/site/etcpandai/documentation/steering-behaviors/path-follow/PandAIPathFollowTutorial.zip?attredirects=0&d=1
