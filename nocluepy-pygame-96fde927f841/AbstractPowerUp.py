import pygame
##from DestroyEnemies import *

class AbstractPowerUp(pygame.sprite.Sprite):

    def __init__(self, radius, teta):
        pygame.sprite.Sprite.__init__(self)
        self.teta = teta
        self. radius = radius

    def getTeta(self):
        return self.teta

    def getRadius(self):
        return self.radius
    
##    def spawn(self):
##        destroyAll = DestroyEnemies(self.getRadius(), self.getTeta())
##        return destroyAll
    
