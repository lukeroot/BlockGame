import os, random
from gameobject import GameObject

class Block(GameObject):
    def __init__(self, properties, game):
        super(Block, self).__init__(properties, game)

        try:
            imgList = []
            for image in xrange(1, self.imgCount + 1):
                imgList.append(image)
            self.imgPath += str(random.choice(imgList))
        except (AttributeError):
            pass
        # Blocks are always 50px? :D
        self.appearance = game.py.image.load(os.path.join("assets", self.imgPath + ".png")).convert()
        self.appearance = game.py.transform.scale(self.appearance, (50, 50))

class Air(Block):
    def __init__(self, game):
        properties = {
            "resistance"    :   0,
            "imgPath"       :   "air",
        }
        super(Air, self).__init__(properties, game)

class Grass(Block):
    def __init__(self, game):
        properties = {
            "resistance"    :   30,
            "imgPath"       :   "grass",
        }
        super(Grass, self).__init__(properties, game)

class Dirt(Block):
    def __init__(self, game):
        properties = {
            "resistance"    :   30,
            "imgPath"       :   "dirt",
        }
        super(Dirt, self).__init__(properties, game)

class Stone(Block):
    def __init__(self, game):
        properties = {
            "resistance"    :   100,
            "imgPath"       :   "stone",
            "imgCount"      :   3,
        }
        super(Stone, self).__init__(properties, game)
