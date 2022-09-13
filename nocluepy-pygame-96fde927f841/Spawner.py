import pygame
import random
import math
from Enemies import *

display_center_x = 400
display_center_y = 300
gettinginstageagain = False

class Spawner(pygame.sprite.Sprite):

    def __init__(self, enemySpeed):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load('Images\Spawner.png')
        self.rect = self.img.get_rect()
        self.rect.x = display_center_x - self.rect.w/2
        self.rect.y = display_center_y - self.rect.h/2
        self.enemySpeed = enemySpeed
        self.prevDeltaTeta = 0
        self.deltaTeta = 0
        self.auxspeed = 0
        self.iteration = 0
        self.stage = 0
        self.counter = 0
        self.spawner1 = 1000
        self.nextStage = 1
        self.loop = 0

    def getTime(self):
        return self.time

    def setTime(self, newTime):
        self.time = newTime

    def getImg(self):
        return self.img

    def getPos(self):
        return (self.rect.x, self.rect.y)

    def subTime(self):
        self.time -= 1
    def getStage(self):
        return self.stage
    def getSpawnNumber(self):
        return self.spawnnumber
    def getSpawner1(self):
        return self.spawner1
    def getloop(self):
        return self.loop

    def spawn(self):
        self.spawnsystem()
        enemy = Enemies(self.enemySpeed + self.auxspeed, self.deltaTeta ,'Images\enemy.png' )
        return enemy
    def spawnsystem(self):
        self.counter += 1
        negative = random.randint(0, 1)
        aux = 1
        if(negative == 0):
            aux = 1
        else:
            aux =-1
            
        if self.stage == 0:
            self.auxspeed = -1
            self.counter = 0
            self.stage = 3
            auxteta = 0
        elif(self.stage == 1):
            #speed stage
            auxteta = math.pi/8*aux
            self.auxspeed = 0
            if self.counter >= 15:
                gettinginstageagain = True
                self.counter = 0
                self.stage = 2
                if self.spawner1 > 500:
                    self.spawner1 -= 100
        elif(self.stage == 2):
            #random Standart
            auxteta = random.randint(0, 360)
            self.auxspeed = -.5
            if self.counter >= 1:
                if(self.loop >= 5):
                    self.stage = 6
                elif(self.nextStage == 1):
                    self.stage = 3
                    self.nextStage = 2
                elif(self.nextStage == 2):
                    self.stage = 1
                    self.nextStage = 3
                elif(self.nextStage == 3):
                    self.stage = 4
                    self.nextStage = 4
                elif(self.nextStage == 4):
                    self.stage = 5
                    self.nextStage = 1
                    self.loop +=1 
                self.counter = 0
                
        elif(self.stage == 3):
            #auxspeed cresce de -0.5 ate 1.5
            #pingpong
            auxteta = math.pi - math.pi/10*aux
            self.auxspeed = -.5 + self.iteration
            if self.counter >= 6:
                self.stage = 2
                self.counter = 0
                if self.auxspeed <= 2:
                    self.iteration += 0.5
        elif(self.stage == 4):
            #sonar stage
            auxteta = random.randint(0, 360)
            self.auxspeed = -1 + self.iteration*0.5
            if self.counter >= 5:
                self.stage = 2
                self.counter = 0
        elif(self.stage == 5):
            #Shield stage
            auxteta = random.randint(0, 360)
            self.auxspeed = -.5 + self.iteration*0.5
            if self.counter >= 6:
                self.stage = 2
                self.counter = 0
        elif(self.stage == 6):
            auxteta = random.randint(0, 360)
            self.auxspeed = 1
            
        self.deltaTeta = self.prevDeltaTeta + auxteta
        self.prevDeltaTeta = self.deltaTeta
        
            
