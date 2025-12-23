from direct.showbase.ShowBase import ShowBase

# Initialite the engine. 'base' is now accesible from anywhere.
base = ShowBase()

# Load and copy the model to render.
scene = base.loader.load_model("models/environment").copy_to(base.render)
# Apply position, rotation and scale transforms on the model.
scene.set_pos_hpr_scale((-8, 42, 0), (0,0,0), (0.25, 0.25, 0.25))


base.run()
