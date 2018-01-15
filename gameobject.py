class GameObject(object):
    def __init__(self, pos, properties, game):
        self.pos = pos
        self.game = game

        for name, value in properties.iteritems():
            setattr(self, name, value)

    def draw(self, location):
        self.objectRect = self.game.screen.blit(self.appearance, location)
