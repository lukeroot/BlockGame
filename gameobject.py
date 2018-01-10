class GameObject(object):
    def __init__(self, properties, game):
        self.game = game

        for name, value in properties.iteritems():
            setattr(self, name, value)

    def draw(self, location):
        self.game.screen.blit(self.appearance, location)
