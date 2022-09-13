import pygame
import math
from Player import * 


white = (255,255,255)

pygame.init()

display_center_x = 400
display_center_y = 300


class Bullet(pygame.sprite.Sprite):

    def __init__(self, player,speed,cor):
        pygame.sprite.Sprite.__init__(self)
        self.teta = player.getTeta()
        self.radius = player.getRadius()
        self.img = pygame.Surface([5, 5])
        self.rect = self.img.get_rect()
        self.player_w = player.getDimensions()[0]
        self.player_h = player.getDimensions()[1]
        self.rect.x = player.getPos()[0] + self.player_w/2
        self.rect.y = player.getPos()[1] + self.player_h/2

        self.speed = speed
        self.img.fill(cor)

    def getRadius(self):
        return self.radius

    def getTeta(self):
        return self.teta

    def getPos(self):
        return (self.rect.x, self.rect.y)

    def getSpeed(self):
        return self.speed

    def getImg(self):
        return self.img

    def setSpeed(self, newSpeed):
        self.speed = newSpeed

    def update(self):
        self.radius -= self.getSpeed()
        self.rect.x = display_center_x + self.getRadius()*math.cos(self.getTeta()) + self.player_w/2
        self.rect.y = display_center_y + self.getRadius()*math.sin(self.getTeta()) + self.player_h/2

        
    def addSpeed(self):
        self.speed += 5
