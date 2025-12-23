from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor

# Initialite the engine. 'base' is now accesible from anywhere.
base = ShowBase()

# Load and copy the model to render.
scene = base.loader.load_model("models/environment").copy_to(base.render)
# Apply position, rotation and scale transforms on the model.
scene.set_pos_hpr_scale((-8, 42, 0), (0,0,0), (0.25, 0.25, 0.25))


# Load and transform the panda actor.
panda_actor = Actor("models/panda-model", {"walk": "models/panda-walk4"})
panda_actor.set_scale(0.005, 0.005, 0.005)
panda_actor.reparent_to(base.render)
# Loop its animation.
panda_actor.loop("walk")


# Create a pivot for the camera to orbit around.
pivot = base.render.attach_new_node("camera pivot")
# Define a Task procedure to rotate this camera pivot.
def spin_pivot_task(task):
    # We set the pivot's heading relative to itself, increasing it.
    pivot.set_h(pivot, 6*base.clock.dt)
    # We tell the task manager to continue running this task.
    return task.cont
# Add the Task procedure to the task manager.
base.task_mgr.add(spin_pivot_task, "spin pivot task")
# Reparent the camera to the rotating pivot so it is also rotating.
base.cam.reparent_to(pivot)
# Set an offset position to the camera. Now it orbits.
base.cam.set_pos(0, -20, 1)


base.run()
