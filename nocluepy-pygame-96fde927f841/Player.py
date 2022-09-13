import pygame
import math

pygame.init()

display_center_x = 400
display_center_y = 300

green = (0,255,0)

class Player(pygame.sprite.Sprite):

    def __init__(self, radius, teta, speed):
        pygame.sprite.Sprite.__init__(self)
        self.teta = teta
        self.radius = radius
        self.img = pygame.Surface([15, 15])
        self.rect = self.img.get_rect()
        self.rect.x = display_center_x + radius*math.cos(teta)
        self.rect.y = display_center_y + radius*math.sin(teta)
        self.speed = speed
        self.img.fill(green)

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

    def setTeta(self, newTeta):
        self.teta = newTeta

    def setSpeed(self, newSpeed):
        self.speed = newSpeed

    def update(self):
        self.rect.x = display_center_x + self.getRadius()*math.cos(self.getTeta())
        self.rect.y = display_center_y + self.getRadius()*math.sin(self.getTeta())

    def addTeta(self):
        self.teta += self.getSpeed()

    def subTeta(self):
        self.teta -= self.getSpeed()
