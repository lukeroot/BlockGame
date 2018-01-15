import os, random
from gameobject import GameObject

class Block(GameObject):
    def __init__(self, pos, properties, game):
        self.isAir = False
        super(Block, self).__init__(pos, properties, game)

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

    def destroy(self):
        if self.isAir:
            return

        self.resistance -= 1

        if self.resistance == 0:
            pos = self.pos
            self.game.blocks[(pos)] = Air(pos, self.game)
            return True

class Air(Block):
    def __init__(self, pos, game):
        properties = {
            "isAir"         :   True,
            "imgPath"       :   "air",
        }
        super(Air, self).__init__(pos, properties, game)

class Grass(Block):
    def __init__(self, pos, game):
        properties = {
            "resistance"    :   30,
            "imgPath"       :   "grass",
        }
        super(Grass, self).__init__(pos, properties, game)

class Dirt(Block):
    def __init__(self, pos, game):
        properties = {
            "resistance"    :   30,
            "imgPath"       :   "dirt",
        }
        super(Dirt, self).__init__(pos, properties, game)

class Stone(Block):
    def __init__(self, pos, game):
        properties = {
            "resistance"    :   100,
            "imgPath"       :   "stone",
            "imgCount"      :   3,
        }
        super(Stone, self).__init__(pos, properties, game)
