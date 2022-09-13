import pygame
import math
from AbstractPowerUp import *

display_center_x = 400
display_center_y = 300

purple = (255,0,255)

class DestroyEnemies(AbstractPowerUp):

    def __init__(self, radius, teta):
        AbstractPowerUp.__init__(self, radius, teta)
        self.img = pygame.Surface([15, 15])
        self.rect = self.img.get_rect()
        self.rect.x = display_center_x + self.radius*math.cos(self.teta)
        self.rect.y = display_center_y + self.radius*math.sin(self.teta)
        self.img.fill(purple)

    def getPos(self):
        return (self.rect.x, self.rect.y)

    def getImg(self):
        return self.img
