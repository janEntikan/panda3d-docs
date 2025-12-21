from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor


base = ShowBase()

# Copy the environment model to render.
scene = base.loader.load_model("models/environment").copy_to(base.render)
# Apply position, scale and rotation transforms on the model.
scene.set_pos_hpr_scale(pos=(-8, 42, 0), hpr=(0, 0, 0), scale=(0.25, 0.25, 0.25))

# Load and transform the panda actor.
panda_actor = Actor("models/panda-model", {"walk": "models/panda-walk4"})
panda_actor.set_scale(0.005, 0.005, 0.005)
panda_actor.reparent_to(base.render)
# Loop its animation.
panda_actor.loop("walk")

# Define a procedure to move the camera.
def spin_camera_task(task):
    # Move camera to center of scene
    base.cam.set_pos(base.render, (0, 0, 0))
    # Rotate camera heading relative to itself
    base.cam.set_h(base.cam, 6*base.clock.dt)
    # Move camera backwards relative to itself
    base.cam.set_pos(base.cam, (0, -20, 1))
    return task.cont

base.task_mgr.add(spin_camera_task, "spin_camera_task")

base.run()
