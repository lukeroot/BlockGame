import os
from gameobject import GameObject

class Humanoid(GameObject):
    def __init__(self, pos, properties, game):
        super(Humanoid, self).__init__(pos, properties, game)
        self.appearance = game.py.image.load(os.path.join("assets", self.imgPath + ".png")).convert_alpha()

class Player(Humanoid):
    def __init__(self, properties, game):

        self.direction = 1
        self.currentLoc = [(0, 0), (17, 16)]

        super(Player, self).__init__((400, 320), properties, game)

        self.appearance = game.py.transform.scale(self.appearance, (50, 94))

    def draw(self):
        super(Player, self).draw(self.pos)

    def directionChange(self, direction):
        if direction != self.direction:
            self.appearance = self.game.py.transform.flip(self.appearance, True, False)
            self.direction = direction
