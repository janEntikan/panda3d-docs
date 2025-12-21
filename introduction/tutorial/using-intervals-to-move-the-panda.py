from panda3d.core import Point3

from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import (
    Sequence,
    LerpPosInterval,
    LerpHprInterval,
)
from direct.showbase.ShowBase import ShowBase


base = ShowBase()

# Copy the environment model to render.
scene = base.loader.load_model("models/environment").copy_to(base.render)
# Apply scale and position transforms on the model.
scene.set_scale(0.25, 0.25, 0.25)
scene.set_pos(-8, 42, 0)

# Load and transform the panda actor.
panda_actor = Actor("models/panda-model", {"walk": "models/panda-walk4"})
panda_actor.set_scale(0.005, 0.005, 0.005)
panda_actor.reparent_to(base.render)
# Loop its animation.
panda_actor.loop("walk")

# Define some points of interest.
pos_a, pos_b = (0, -10, 0), (0, 10, 0)
hpr_a, hpr_b = (180, 0, 0), (0, 0, 0)
# Use them to create the sequence of lerp intervals needed for the panda to
# walk back and forth.
panda_pace = Sequence(
    LerpPosInterval(panda_actor, 13, pos_a, startPos=pos_b),
    LerpHprInterval(panda_actor, 3,  hpr_a, startHpr=hpr_b),
    LerpPosInterval(panda_actor, 13, pos_b, startPos=pos_a),
    LerpHprInterval(panda_actor, 3,  hpr_b, startHpr=hpr_a),
    name="panda-pace"
)
panda_pace.loop()

# Define a procedure to move the camera.
def spin_camera_task(task):
    # Move camera to center of scene
    base.cam.set_pos(base.render, (0,0,0))
    # Rotate camera heading relative to itself
    base.cam.set_h(base.cam, 6*base.clock.dt)
    # Move camera backwards relative to itself
    base.cam.set_pos(base.cam, (0, -20, 1))
    return task.cont

base.task_mgr.add(spin_camera_task, "spin_camera_task")

base.run()
