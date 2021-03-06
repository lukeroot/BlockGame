import pygame, random, math
from characters import Player
from blocks import Air, Grass, Dirt, Stone

class Game:
    # Cheeky/Lazy way of importing pygame once
    py = pygame
    ## Might struggle with user changing keybinds at later date
    KEY_BINDS = {
        py.K_q  :   "quit",
        py.K_a  :   "move_1",
        py.K_d  :   "move_-1",
    }

    def __init__(self):
        pygame.init()

        self.isLive = True
        self.currentTick = 0
        self.update = True

        self.screen = pygame.display.set_mode((850,800))
        self.cameraLocation = [(0, 0), (17, 16)]

        self.blocks = {}
        self.currentBlocks = {}

        self.player = Player({
            "health"    :   100,
            "imgPath"   :   "player",
        }, self)

    def run(self):
        while self.isLive:

            self.handleKeyPresses()
            self.handleMousePresses()
            self.handleTicks()

            if self.update:
                self.update = False
                self.getSetCurrentBlocks()
                self.drawScreen()
                self.checkGravity()

        pygame.quit()
        quit()

    def handleKeyPresses(self):
        if self.tickCheck():
            return
        keys = pygame.key.get_pressed()
        # Check if we're pressing a button
        if sum(list(keys)) == 0:
            return
        # Looping through the possible keys to check for a match
        for key, call in self.KEY_BINDS.iteritems():
            if keys[key]:
                underscoreLoc = call.find("_")
                if underscoreLoc != -1:
                    getattr(self, call[:underscoreLoc])(call[underscoreLoc + 1:])
                else:
                    getattr(self, call)()

    def handleMousePresses(self):
        # TODO entire function (looping currentBlocks to check collide)
        if self.tickCheck():
            return

        event = pygame.event.get()

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            for translatedXY, block in self.currentBlocks.iteritems():
                if block.objectRect.collidepoint(pos):
                    isDestroyed = block.destroy()
                    if isDestroyed:
                        self.update = True
                        del block
                    break

    def tickCheck(self):
        # Keep the press acknowledgement at a resonable speed
        if int(self.currentTick) % 10000 != 0:
            return True

    def handleTicks(self):
        if self.currentTick > 1000000:
            self.currentTick = 0

        self.currentTick += 1

    def getSetCurrentBlocks(self):
        self.currentBlocks = {}
        (xLow, yLow), (xHigh, yHigh) = self.cameraLocation

        for x in xrange(int(math.floor(xLow)), int(math.ceil(xHigh))):
            for y in xrange(int(math.floor(yLow)), int(math.ceil(yHigh))):
                # The key of currentBlocks is the translated x, y coords for drawing on screen
                xTranslated = ((x - xLow) * 50)
                yTranslated = ((y - yLow) * 50)

                # Don't overwrite known blocks
                if (x, y) not in self.blocks:
                    self.blocks[(x, y)] = self.generateBlockFromLoc(x, y)

                self.currentBlocks[(xTranslated, yTranslated)] = self.blocks[(x,y)]

    def generateBlockFromLoc(self, x, y):
        ''' For now, some hard coded locations of where blocks spawn.
            The idea will be to have a class that uses a noise algorithm to
            determine the block, depending on the location (factoring in the seed also) '''
        # return random.choice([Air(self), Grass(self), Dirt(self)])
        pos = (x, y)
        if y < 8:
            return Air(pos, self)
        elif y == 8:
            return Grass(pos, self)
        elif y in [9, 10, 11]:
            return Dirt(pos, self)
        else:
            return Stone(pos, self)

    def drawScreen(self):
        for translatedXY, block in self.currentBlocks.iteritems():
            block.draw(translatedXY)

        self.player.draw()
        self.py.display.flip()

    def checkGravity(self):
        def drop():
            # Need to implement a 'V = gt' logic here as to enable realistic fall speed
            self.cameraLocation = [(xLow, yLow + 0.1), (xHigh, yHigh + 0.1)]
            self.update = True

        (xLow, yLow), (xHigh, yHigh) = self.cameraLocation
        x = int((xHigh + xLow) / 2.0)
        y = int((yHigh + yLow) / 2.0)

        ''' As the player is always static in the middle of the screen,
            There will only ever be 1 or 2 block/s underneath '''
        if self.blocks[(x, y)].isAir:
            # Only one block is underneath us at this point (to within a tolerance)
            if xLow % 1 <= 0.1 or xLow % 1 >= 0.9:
                drop()
            # Two block reside underneath at this point so we need to work out which side they're on
            elif xLow % 1 > 0.5 and self.blocks[(x - 1, y)].isAir:
                drop()
            elif self.blocks[(x + 1, y)].isAir:
                drop()

    def quit(self):
        self.isLive = False

    def move(self, direction):
        direction = int(direction)
        self.player.directionChange(direction)

        (xLow, yLow), (xHigh, yHigh) = self.cameraLocation
        self.cameraLocation = [(xLow - (0.1 * direction), yLow), (xHigh - (0.1 * direction), yHigh)]
        self.update = True

if __name__ == '__main__':
    game = Game()
    game.run()
