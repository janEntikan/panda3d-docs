from direct.showbase.ShowBase import ShowBase


base = ShowBase()

# Copy the environment model to render.
scene = base.loader.load_model("models/environment").copy_to(base.render)
# Copy the environment model to render.
scene.set_pos_hpr_scale((-8, 42, 0), (0,0,0), (0.25, 0.25, 0.25))

base.run()
