import pygame
import math

display_center_x = 400
display_center_y = 300
red = (255,0,0)

class Enemies(pygame.sprite.Sprite):

    def __init__(self, speed, teta, image):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.teta = teta
        self.radius = 0
        self.img = pygame.Surface([20, 20])
        self.img.fill(red)
        self.rect = self.img.get_rect()
        self.rect.x = display_center_x + self.radius*math.cos(self.teta)
        self.rect.y = display_center_y + self.radius*math.sin(self.teta)

    def getPos(self):
        return (self.rect.x, self.rect.y)

    def getDimensions(self):
        return (self.rect.w, self.rect.h)

    def getImg(self):
        return self.img

    def getSpeed(self):
        return self.speed

    def getTeta(self):
        return self.teta

    def getRadius(self):
        return self.radius

    def setSpeed(self, newSpeed):
        self.speed = newSpeed

    def setTeta(self, newTeta):
        self.teta = newTeta

    def setRadius(self, newRadius):
        self.radius = newRadius

    def addRadius(self):
        self.radius += self.getSpeed()

    def update(self):
        self.addRadius()
        self.rect.x = display_center_x + self.getRadius()*math.cos(self.getTeta())
        self.rect.y = display_center_y + self.getRadius()*math.sin(self.getTeta())
    
