import pygame
import math

pygame.init()

display_center_x = 400
display_center_y = 300

darkred = (200,0,0)

class SonarEndPoint(pygame.sprite.Sprite):

    def __init__(self, radius, teta, speed):
        pygame.sprite.Sprite.__init__(self)
        self.teta = teta
        self.radius = radius
        self.img = pygame.Surface([5, 5])
        self.img2 = pygame.Surface([5,5])
        self.rect2 = self.img2.get_rect()
        self.rect = self.img.get_rect()
        self.rect.x = display_center_x + radius*math.cos(teta)
        self.rect.y = display_center_y + radius*math.sin(teta)
        self.rect2.x = display_center_x + radius*math.cos(teta)
        self.rect2.y = display_center_y + radius*math.sin(-teta)
        self.rect2.y = -self.rect.y
        self.speed = speed
        self.img.fill(darkred)
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
