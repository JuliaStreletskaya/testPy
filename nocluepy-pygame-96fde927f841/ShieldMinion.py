import pygame
import math

orange = (255, 165, 0)
pygame.init()


display_center_x = 400
display_center_y = 300


class ShieldMinion(pygame.sprite.Sprite):
    
    

    def __init__(self, radius, teta, speed):
        pygame.sprite.Sprite.__init__(self)
        self.teta = teta
        self.radius = radius
        self.img = pygame.Surface([10, 10])
        self.rect = self.img.get_rect()
        self.rect.x = display_center_x + radius*math.cos(teta)
        self.rect.y = display_center_y + radius*math.sin(teta)
        self.speed = speed
        self.img.fill(orange)
        self.direct = 1 

    def getRadius(self):
        return self.radius

    def getTeta(self):
        return self.teta

    def getPos(self):
        return (self.rect.x, self.rect.y)

    def getDimensions(self):
        return (self.rect.w, self.rect.h)

    def getSpeed(self):
        return self.speed

    def getImg(self):
        return self.img
    
    def setDirect(self):
        self.direct = self.direct * (-1)

    def update(self):
        self.teta += self.speed*self.direct
        self.rect.x = display_center_x + self.getRadius()*math.cos(self.getTeta())
        self.rect.y = display_center_y + self.getRadius()*math.sin(self.getTeta())

    def addTeta(self):
        self.teta += self.getSpeed()

    def subTeta(self):
        self.teta -= self.getSpeed()