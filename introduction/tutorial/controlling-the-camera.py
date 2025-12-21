from direct.showbase.ShowBase import ShowBase




# Load and copy the model to render.
scene = base.loader.loadModel("models/environment").copy_to(base.render)
# Apply scale and position transforms on the model.
scene.set_pos_hpr_scale((-8, 42, 0), (0,0,0), (0.25, 0.25, 0.25))

# Define a procedure to move the camera.
def spin_camera_task(task):
    # Move camera to center of scene
    base.cam.set_pos(base.render, (0, 0, 0))
    # Rotate camera heading relative to itself
    base.cam.set_h(base.cam, 6*base.clock.dt)
    # Move camera backwards relative to itself
    base.cam.set_pos(base.cam, (0, -20, 1))
    return task.cont

# Add the spin_camera_task procedure to the task manager.
base.task_mgr.add(spin_camera_task, "spin camera task")


base = ShowBase()
base.game = Game()
base.run()
