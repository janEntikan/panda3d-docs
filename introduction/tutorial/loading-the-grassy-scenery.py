from direct.showbase.ShowBase import ShowBase


class Game:
    def __init__(self):
        # Load and copy the model to render.
        self.scene = base.loader.loadModel("models/environment").copy_to(base.render)
        # Apply scale and position transforms on the model.
        self.scene.set_scale(0.25, 0.25, 0.25)
        self.scene.set_pos(-8, 42, 0)


base = ShowBase()
base.game = Game()
base.run()
