import pygame
import random
import time
import math
import os, sys
from Player import *
from Bullet import *
from Spawner import *
from AbstractPowerUp import *
from DestroyEnemies import *
from SpeedUp import *
from SpeedDown import *
from Mirror import *
from SonarEndPoint import *
from ShieldMinion import *

#Caption and Icon
pygame.display.set_caption('Circumference')
icon = pygame.image.load('Images\Circumference_icon.png')
pygame.display.set_icon(icon)

#Music and Sounds
intro_song = 'Music\extenz - Sky.mp3'
gameOverSound = pygame.mixer.Sound('Sounds\gameover.ogg')
clickSound = pygame.mixer.Sound('Sounds\click.ogg')
powerupSound = pygame.mixer.Sound('Sounds\powerup.ogg')
powerdownSound = pygame.mixer.Sound('Sounds\powerdown.ogg')
destroyedSound = pygame.mixer.Sound('Sounds\destroyed.ogg')
overheatSound = pygame.mixer.Sound('Sounds\overheat.ogg')
collideSound = pygame.mixer.Sound('Sounds\collide.ogg')

#RGB
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
darker_red = (200,0,0)
darker_green = (0,200,0)
darker_blue = (0,0,200)
purple = (255,0,255)
darker_purple = (153,0,153)
orange = (255, 165, 0)
darker_orange = (200, 150, 0)

#Booleans
game_over = False
is_moving_left = False
is_moving_right = False
bullet = False
pause = False
godMode = False
godModeOn = False
creditsOn = False
auxCreditslider = -500
firstTimeIntro = True

radius = 250
mirrorTicks = 0
enemiesCount = 0
secondsToAdd = 0
centershots = 0
speed_up_time = 0

globalspeedmultiplier = 3


class GameManager:

    def __init__(self, display_width, display_height):
        self.display_w = display_width
        self.display_h = display_height
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("xirod/xirod.ttf",15)
        self.powerupdestroycircle = False
        
        
        self.test1 = 5
        self.shotcenter = False
        self.gothit = False
        self.test2 = radius + 50
        self.test3 = radius + 50
        self.rotatesonar = math.pi
        self.ammo = -400
        self.isStage4 = False
        self.gettingHard = False
        self.shieldaux = 6
        self.ismorehard = False
        self.isStage5 = False
        self.miniondied = True
        self.flag42 = False
        self.gothurt = False
        self.lastbool = True

    def getDimensions(self):
        return (self.display_w, self.display_h)

    def getClock(self):
        return self.clock

    def getGameDisplay(self):
        return self.gameDisplay
        
    def getFont(self):
        return self.font

    def setFont(self, size):
        self.font = pygame.font.Font("xirod/xirod.ttf",size)

    def quitGame(self):
        pygame.quit()
        quit()

    def checkCollisions(self, enemies, power_ups_list,mirror_list, bullet_list):
        global secondsToAdd
        if not self.miniondied:
            for bullet in bullet_list:
                if bullet.getRadius() <= self.shieldaux:
                    bullet_list.remove(bullet)
                    if(self.shieldaux >= 20 + 6):
                        self.shieldaux -= 20 
        for enemy in enemies:
            if self.powerupdestroycircle:
                if enemy.getRadius() >= self.test3:
                    enemies.remove(enemy)
                    secondsToAdd -= 5
                    pygame.mixer.Sound.play(collideSound)
            if enemy.getRadius() >= radius+50:
                enemies.remove(enemy)
                self.gothit = True
                for power in power_ups_list:
                    power_ups_list.remove(power)
                for mirror in mirror_list:
                    mirror_list.remove(mirror)                 
                secondsToAdd += 10
                self.gothurt = True
                pygame.mixer.Sound.play(collideSound)

    def powerUpSpawn(self, power_ups_list, all_sprites_list):
        power = random.randrange(0,100)
        if power < 40:
            pUp = DestroyEnemies(radius, random.randrange(0,360))
            power_ups_list.add(pUp)
            all_sprites_list.add(pUp)
        elif power < 60:
            pUp = SpeedUp(radius, random.randrange(0,360))
            power_ups_list.add(pUp)
            all_sprites_list.add(pUp)
        elif power < 65:
            pUp = SpeedDown(radius, random.randrange(0,360))
            power_ups_list.add(pUp)
            all_sprites_list.add(pUp)
        elif power < 100:
            pUp = Mirror(radius, random.randrange(0,360))
            power_ups_list.add(pUp)
            all_sprites_list.add(pUp)

    def powerUpCollide(self, player, power_ups_list, enemies_list, spawner, mirror_list, all_sprites_list):
        power_ups_hits = pygame.sprite.spritecollide(player, power_ups_list, True)
        for power in power_ups_hits:
            self.powerUp(power, player, enemies_list, spawner, mirror_list, all_sprites_list)
        for mirror in mirror_list:
            power_ups_hits = pygame.sprite.spritecollide(mirror, power_ups_list, True)
            for power in power_ups_hits:
                self.powerUp(power, player, enemies_list, spawner, mirror_list, all_sprites_list)

    def powerUp(self, power, player, enemies_list, spawner, mirror_list, all_sprites_list):
        global mirrorTicks
        global enemiesCount
        global secondsToAdd
        global speed_up_time
        
        if type(power) == DestroyEnemies:
            self.powerupdestroycircle = True
            pygame.mixer.Sound.play(powerupSound)
        elif type(power) == SpeedUp:
            player.setSpeed(0.015 * globalspeedmultiplier)
            pygame.mixer.Sound.play(powerupSound)
            for mirror in mirror_list:
                mirror.setSpeed(0.015 * globalspeedmultiplier)
            speed_up_time = pygame.time.get_ticks()
        elif type(power) == SpeedDown:
            pygame.mixer.Sound.play(powerdownSound)
            player.setSpeed(0.005 * globalspeedmultiplier)
            for mirror in mirror_list:
                mirror.setSpeed(0.005 * globalspeedmultiplier)
            speed_up_time = pygame.time.get_ticks()
        elif type(power) == Mirror:
            pygame.mixer.Sound.play(powerupSound)
            mirror = None
            if(len(mirror_list)==0):
                mirror = Player(player.getRadius(), (player.getTeta()+(math.pi)), player.getSpeed())
            elif(len(mirror_list)==1):
                mirror = Player(player.getRadius(), (player.getTeta()+(math.pi)/2), player.getSpeed())            
            elif(len(mirror_list) == 2):
                mirror = Player(player.getRadius(), (player.getTeta()+(3*math.pi)/2), player.getSpeed())
            if(not (mirror == None)):
                mirror_list.add(mirror)
                all_sprites_list.add(mirror)
                mirrorTicks = pygame.time.get_ticks()

    def text_objects(self, text, color):
        textSurface = self.getFont().render(text, True, color)
        return textSurface, textSurface.get_rect()

    def writeText(self, text, size, color, place = None): #place in case we need to specify where
        self.setFont(size)
        textSurface, textRect = self.text_objects(text, color)
        if place == None:
            textRect.center = (self.getDimensions()[0]/2, self.getDimensions()[1]/2)
            self.getGameDisplay().blit(textSurface, textRect)
        else:
            self.getGameDisplay().blit(textSurface,place)
    
    def DrawCircleDinamic(self):
        if(self.shotcenter):
            if not(self.test1 >= radius + 50):
                self.test1 += 2
                pygame.draw.circle(self.getGameDisplay(), darker_blue, [self.getDimensions()[0]//2, self.getDimensions()[1]//2], self.test1, 5)
            else:
                self.test1 = 5
                self.shotcenter = False
    def DrawCircleDinamicDestroy(self):
        if(self.powerupdestroycircle):
            if (self.test3 > 5):
                circle = pygame.draw.circle(self.getGameDisplay(),purple, [self.getDimensions()[0]//2, self.getDimensions()[1]//2], self.test3, 5)
                self.test3 -= 2      
            else:
                self.test3 = radius + 50
                self.powerupdestroycircle = False    
    def ReverseDinamicCircle(self):
        if(self.gothit):
            if (self.test2 > 5):
                pygame.draw.circle(self.getGameDisplay(), red, [self.getDimensions()[0]//2, self.getDimensions()[1]//2], self.test2, 5)
                self.test2 -= 2
            else:
                self.test2 = radius + 50
                self.gothit = False
    def DrawEnemyShield(self):
        if(not self.miniondied):
            if (self.shieldaux < 150):
                pygame.draw.circle(self.getGameDisplay(), orange, [self.getDimensions()[0]//2, self.getDimensions()[1]//2],self.shieldaux, 6)
                self.shieldaux+=1
            else:
                pygame.draw.circle(self.getGameDisplay(), orange, [self.getDimensions()[0]//2, self.getDimensions()[1]//2],150, 6)
        else:
            self.shieldaux = 6
                
    def DrawOverHeatingGun(self):
        if(self.ammo <= -100):
            pygame.draw.rect(self.getGameDisplay(),green,(50,450,30,self.ammo))#400
            pygame.mixer.Sound.stop(overheatSound)
        elif(self.ammo <= 0):
            pygame.draw.rect(self.getGameDisplay(),yellow,(50,450,30,self.ammo))#400
            pygame.mixer.Sound.stop(overheatSound)
        else:
            pygame.draw.rect(self.getGameDisplay(),red,(50,460,30,self.ammo))#400
            pygame.mixer.Sound.play(overheatSound)
        
        self.writeText('AMMO', 15, white, (30,530))
    
    def DrawSonar(self,endpoint,endpoint2):
        if(self.isStage4):
            self.getGameDisplay().blit(endpoint.getImg(), (endpoint.getPos()[0], endpoint.getPos()[1]))
            pygame.draw.line(self.getGameDisplay(),darker_red,[400,300],endpoint.getPos(),10)
            if(self.ismorehard):
                self.getGameDisplay().blit(endpoint.getImg(), (endpoint2.getPos()[0], endpoint2.getPos()[1]))
                pygame.draw.line(self.getGameDisplay(),darker_red,[400,300],endpoint2.getPos(),10)
        
                
    def blitAll(self, spawner, player, bullet_list, enemies_list, power_ups_list, mirror_list,endpoint,endpoint2,shieldMinion):
        sizemanel = self.display_w, self.display_h
        self.getGameDisplay().fill(black)
        pygame.draw.circle(self.getGameDisplay(), darker_blue, [self.getDimensions()[0]//2, self.getDimensions()[1]//2], radius + 50, 5)
        self.DrawOverHeatingGun()
        self.DrawCircleDinamic()
        self.ReverseDinamicCircle()
        self.getGameDisplay().blit(player.getImg(),(player.getPos()[0], player.getPos()[1]))
        self.getGameDisplay().blit(spawner.getImg(),(spawner.getPos()[0], spawner.getPos()[1]))
        for bullet in bullet_list:
            self.getGameDisplay().blit(bullet.getImg(),(bullet.getPos()[0], bullet.getPos()[1]))
        for enemy in enemies_list:
            self.getGameDisplay().blit(enemy.getImg(),(enemy.getPos()[0], enemy.getPos()[1]))
        for power in power_ups_list:
            self.getGameDisplay().blit(power.getImg(),(power.getPos()[0], power.getPos()[1]))
        for mirror in mirror_list:
            self.getGameDisplay().blit(mirror.getImg(),(mirror.getPos()[0], mirror.getPos()[1]))
        self.DrawEnemyShield()
        if(self.isStage5 and not self.miniondied):
            self.getGameDisplay().blit(shieldMinion.getImg(),(shieldMinion.getPos()[0],shieldMinion.getPos()[1]))
        self.DrawCircleDinamicDestroy()
        self.DrawSonar(endpoint,endpoint2)
    
    def renderTimeText(self,time):
        initialTime = 301
        minutesTime = int((initialTime - time) / 60)
        secondsTime = int((initialTime - time) - (minutesTime * 60))
        if(secondsTime >= 0 and minutesTime >= 0):
            if(minutesTime < 10):
                labelmin = '0' + str(minutesTime)
                if(secondsTime < 10):
                    labelsec = '0' +str(secondsTime)
                else:
                    labelsec = str(secondsTime)
            else:
                labelmin = str(minutesTime)
                if(secondsTime < 10):
                    labelsec = '0' + str(secondsTime)
                else:
                    labelsec = str(secondsTime)
            
            minpos = 290,270
            secpos = 420,270
            thingpos = 400,270
            
            if(minutesTime == 0 and secondsTime <= 30):
                if(secondsTime < 10):
                    if not(secondsTime%2 == 0):
                        self.writeText(labelmin,50,red,minpos)
                        self.writeText(':',50,red,thingpos)
                        self.writeText(labelsec,50,red,secpos)
                else:
                    self.writeText(labelmin,50,red,minpos)
                    self.writeText(':',50,red,thingpos)
                    self.writeText(labelsec,50,red,secpos)
                    
            else:
                self.writeText(labelmin,50,green,minpos)
                self.writeText(':',50,green,thingpos)
                self.writeText(labelsec,50,green,secpos)                
        else:
            
            score_list = list()
            done = False
            new_highscore = False
            try:
                file = open('highscores.txt', 'r+')
            except:
                file = open('highscores.txt', 'w').close() #create file
                file = open('highscores.txt', 'r+')         #open file
            for line in file:
                lineSplitted = line.rstrip('\n').split(" - ")
                score_list.append((lineSplitted[0],int(lineSplitted[1])))
                score_list.sort(key=lambda tup:tup[1], reverse = True)
            count = len(score_list)
            if count > 4:
                count = 5
            i = 0
            new_list = list()
            while i < count:
                if enemiesCount*100 + centershots - damagescore > score_list[i][1] and not done:
                    name = self.ask(self.getGameDisplay(), "Name")
                    new_list.append((name, enemiesCount*100 + centershots - damagescore))
                    done = True
                    new_highscore = True
                    i -= 1
                else:
                    new_list.append((score_list[i][0], score_list[i][1]))
                i += 1
            if count < 5 and not done:
                name = self.ask(self.getGameDisplay(), "Name")
                new_list.append((name, enemiesCount*100 + centershots - damagescore))
                new_highscore = True

            file.seek(0)
            file.truncate(0)
            for highscore in new_list:
                file.write(highscore[0] + " - " + str(highscore[1])+"\n")
            file.close()

            if new_highscore:
                self.highScore()
            else:
                self.gameOver()

    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                return event.key
            else:
                pass

    def display_box(self,screen, message):

        self.writeText('Congratulations!', 50, green, place = (30,40))
        self.writeText('New HighScore!', 50, blue, place = (75,160))

        
        "Print a message in a box in the middle of the screen"
        self.setFont(18)
        pygame.draw.rect(screen, black,
                       ((self.getDimensions()[0] / 2) - 180,
                        (self.getDimensions()[1] / 2) - 10,
                        290,20), 0)
        pygame.draw.rect(screen, white,
                       ((self.getDimensions()[0] / 2) - 180,
                        (self.getDimensions()[1] / 2) - 12,
                        290,24), 1)
        if len(message) != 0:
            screen.blit(self.getFont().render(message, 1, white),
                    ((self.getDimensions()[0] / 2) - 180, (self.getDimensions()[1] / 2) - 10))
        pygame.display.flip()

    def ask(self, screen, question):
        "ask(screen, question) -> answer"
        string = ""
        self.getGameDisplay().fill(black)  
        current_string = []
        
        self.display_box(self.getGameDisplay(), question + ": " + string.join(current_string))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
            inkey = self.get_key()
            if inkey == pygame.K_BACKSPACE:
                current_string = current_string[0:-1]
            elif inkey == pygame.K_RETURN:
                break
            elif inkey == pygame.K_MINUS:
                current_string.append("_")
            elif inkey <= 127 and len(current_string)<10:
                current_string.append(chr(inkey))
            self.display_box(self.getGameDisplay(), question + ": " + string.join(current_string))
            pygame.display.update()
            self.getClock().tick(60)
        return string.join(current_string)

    def button(self, msg, posX, posY, width, height, darkColor, color, action=None, font = None):
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if posX+width > mouse[0] > posX and posY+height > mouse[1] > posY:
            pygame.draw.rect(self.getGameDisplay(), color, (posX, posY, width, height))
            if click[0] == 1 and action != None:
                pygame.mixer.Sound.play(clickSound)
                action()
                    
        else:
            pygame.draw.rect(self.getGameDisplay(), darkColor, (posX, posY, width, height))

        if not font:   
            self.setFont(20)
        else:
            self.setFont(font)
        playSurf, playRect = self.text_objects(msg, black)
        playRect.center = ((posX+(width/2)), (posY+(height/2)))
        self.getGameDisplay().blit(playSurf,playRect)

    def paused(self):

        pygame.mixer.music.pause()

        self.writeText('Paused', 95, white, place = (125, 100))
        
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.unpause()

            if not godModeOn and not creditsOn:
                self.button("Continue", 310, 400, 160, 75, darker_green, green, self.unpause)
                self.button("Quit", 510, 400, 160, 75, darker_red, red, self.quitGame)
                self.button("Menu", 110, 400, 160, 75, darker_purple, purple, self.game_intro)
            else:
                self.button("Continue", 110, 400, 160, 75, darker_green, green, self.unpause)
                self.button("Quit", 510, 400, 160, 75, darker_red, red, self.quitGame)
            
            pygame.display.update()
            self.getClock().tick(60)

    def unpause(self):
        global pause
        pygame.mixer.music.unpause()
        pause = False

    def gameOver(self):
        global firstTimeIntro
        firstTimeIntro = True
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(gameOverSound)
        pygame.time.wait(500)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_loop()

            sizemanel = self.display_w, self.display_h
            self.getGameDisplay().fill(black)               
            self.writeText('Game Over', 90, blue, place = (0,120))
            self.writeText('Score: ' + str(enemiesCount*100 + centershots - damagescore), 25, purple, place = (self.getDimensions()[0]/2-100,50))

            self.button("Play", self.getDimensions()[0]/2 - 90, 250, 180, 75, darker_green, green, self.game_loop)
            self.button("Menu", self.getDimensions()[0]/2 - 90, 350, 180, 75, darker_blue, blue, self.game_intro)
            self.button("Quit", self.getDimensions()[0]/2 - 90, 450, 180, 75, darker_red, red, self.quitGame)
            
            pygame.display.update()
            self.getClock().tick(15)

    def highScore(self):
        high_score = True
        
        while high_score:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()

            
            sizemanel = self.display_w, self.display_h
            self.getGameDisplay().fill(black)   
            self.writeText('High Score', 70, blue, place = (self.getDimensions()[0]/2-300,50))

            try:
                file = open('highscores.txt', 'r')
                height = 150
                i = 0
                for line in file:
                    if i < 5:
                        line = line.rstrip('\n')
                        self.writeText(line, 25, darker_green, place = (self.getDimensions()[0]/2-160,height))
                        height += 50
                    else:
                        break
                    i+=1
                if i == 0:
                    self.writeText('No Highscores yet', 35, blue)
                file.close()
            except:
                self.writeText('No Highscores yet', 35, blue)


            self.button("Menu", 110, 450, 180, 75, darker_green, green, self.game_intro)
            self.button("Quit", 510, 450, 180, 75, darker_red, red, self.quitGame)

            pygame.display.update()
            self.getClock().tick(15)

    def game_intro(self):
        pygame.time.delay(100) #wait 100ms for mouse click unpress
        #Use Sky Music in the intro and don't forget to credit the guy!!!!!!!!!!!
        global firstTimeIntro
        global creditsOn
        global godModeOn
        creditsOn = False
        godModeOn = False
        intro = True
        auxintroslider = -100
        auxintroslider2 = 1700
        auxintroslider3 = -1000

        if firstTimeIntro:
            pygame.mixer.music.load(intro_song)
            pygame.mixer.music.play(-1)
            firstTimeIntro = False
        
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
            if(auxintroslider >= 1800):
                auxintroslider = -900
            if auxintroslider2 >= 1800:
                auxintroslider2 = -900
            if(auxintroslider3 >= 1800):
                auxintroslider3 = -900
            auxintroslider += 2
            auxintroslider2 += 5
            auxintroslider3 += 3
            
            sizemanel = self.display_w, self.display_h
            self.getGameDisplay().fill(black)
            pygame.draw.circle(self.getGameDisplay(), darker_blue, [self.getDimensions()[0]//2, self.getDimensions()[1]//2], radius + 50, 5)
            self.shotcenter = True
            self.DrawCircleDinamic()            
            self.writeText('Circumference', 64, blue, place = (0,20))
            try:
                file = open('highscores.txt', 'r')
                line = file.readline().rstrip('\n').split(" - ")
                best_player = line[0]
                best_score = line[1]
            except:
                best_player = "-"
                best_score = "-"
                           
            self.writeText('Circumference is a game created by Manuel Silva and Ricardo Pereira', 15, darker_green,place = (-auxintroslider,120))
            self.writeText('Best Player: ' +str(best_player) + ' Score: ' +str(best_score), 15, white,place = (auxintroslider2,140))
            self.writeText('Controls : "a" "d" "SPACE" "P"      Do not let the red enemies get past you !!!!', 15, red, place = (auxintroslider3,160))
            

            self.button("Play", self.getDimensions()[0]/2 - 90, 250, 180, 75, darker_green, green, self.game_loop)
            self.button("High Score", self.getDimensions()[0]/2 - 90, 350, 180, 75, darker_blue, blue, self.highScore)
            self.button("Quit", self.getDimensions()[0]/2 - 90, 450, 180, 75, darker_red, red, self.quitGame)
            
            self.button("Credits", self.getDimensions()[0]/2 - 350, 500, 100,75,darker_purple, purple, self.credits, font = 12)
            self.button("God Mode", self.getDimensions()[0]/2 + 250, 500, 100, 75, darker_orange, orange, self.god_mode, font=12)

            pygame.display.update()
            self.getClock().tick(30)

    def godModeOff(self):
        global godModeOn
        global firstTimeIntro
        firstTimeIntro = True
        godModeOn = False
        pygame.time.delay(150)
        self.game_intro()

    def god_mode(self):
        global godMode
        global godModeOn
        godMode = True
        godModeOn = True
        pygame.time.delay(150)
        self.game_loop()

    def playlist(self, playlistFolderPath = "Music\Playlist/"):
        """ gets all files and folders in given folder into a list and returns it
        """
        lista = list()
        # use os module to manipulate file system
        try:
            for i in os.listdir(playlistFolderPath):
                lista.append(i)
            return lista
        except:
            print ("create playlist folder to listen to your songs")

    def playPlaylist(self, playlistFolderPath = "Music\Playlist/"):
        """ plays songs in a folder in random order
        """
        #play playlist on shuffle
        SongList = self.playlist(playlistFolderPath)
        if SongList == None: # no playlist folder
            return
        listLen = len(SongList)
        if listLen == 0:
            return
        i = random.randint(0,listLen-1)
        pygame.mixer.music.load(playlistFolderPath + SongList[i]) # sets filename from "playlist" folder
        pygame.mixer.music.set_endevent(pygame.USEREVENT+2) # sends ou event when song finishses
        pygame.mixer.music.play()

    def credits(self):
        global godMode
        global godModeOn        
        global creditsOn
        global auxCreditslider
        auxCreditslider = -500
        creditsOn = True
        godMode = True
        godModeOn = True
        pygame.time.delay(150)
        self.game_loop()        
        
    def game_loop(self):
        global game_over
        global is_moving_left
        global is_moving_right
        global pause
        global mirrorTicks
        global enemiesCount
        global secondsToAdd
        global centershots
        global damagescore
        global speed_up_time
        global godMode
        global godModeOn
        global firstTimeIntro
        global black
        global white
        global green
        global creditsOn
        global auxCreditslider
        
        self.lastbool = True
        firstTimeIntro = True
        
        if not godModeOn:
            godMode = False

        self.playPlaylist()        
        stagenum = -1
        centershots = 0
        enemiesCount = 0
        damagescore = 0
        self.ammo = -400
        self.shotcenter = False
        self.gothit = False
        is_moving_left = False
        is_moving_right = False


        self.ismorehard = False
        self.shieldaux = 6
        self.test1 = 5
        self.test2 = radius + 50
        self.test3 = radius + 50
        self.rotatesonar = math.pi
        self.isStage4 = False
        self.isStage5 = False
        self.gettingHard = False
        self.miniondied = True
        self.flag42 = False
        self.gothurt = False

        lock = True

        isShooting = False
        hasSpawnPower = False
        changedAlready = False
        
        enemiesSpeed = 0.5 * globalspeedmultiplier

        lastBulletTick = 0
        unpauseTicks = 0
        
        spawner = Spawner(enemiesSpeed)
        stage = spawner.getStage()
        
        if(stage == 0):
            spawningTime = 3000
        prevStage = stage

        SPAWN = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN, spawningTime)



        mirror_list = pygame.sprite.Group()
        bullet_list = pygame.sprite.Group()
        all_sprites_list = pygame.sprite.Group()
        enemies_list = pygame.sprite.Group()
        power_ups_list = pygame.sprite.Group()
        endPoint_list = pygame.sprite.Group()
        endPoint_list2 = pygame.sprite.Group()

        player = Player(radius, 0, 0.01 * globalspeedmultiplier)
        endPoint = SonarEndPoint(radius,math.pi/2, 0.025)
        endPoint2 = SonarEndPoint(radius,3*math.pi/2, 0.025)

        endPoint_list.add(endPoint)
        endPoint_list2.add(endPoint2)
        
        shieldminion = ShieldMinion(100, math.pi/2, 0.04)

        all_sprites_list.add(player)
        all_sprites_list.add(spawner)
        
        startTicks = pygame.time.get_ticks()
        spawnTicks = 0
        secondsToAdd = 0
        counter = 0
            
        flagtest = False
        otherflagtest = False
        
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
                elif event.type == SPAWN:
                    spawn = False
                    while not spawn:
                        enemy = spawner.spawn()
                        if(otherflagtest and counter < 10):
                            self.powerUpSpawn(power_ups_list, all_sprites_list)
                            counter+=1
                        if len(pygame.sprite.spritecollide(enemy, enemies_list, False)) == 0:               
                            enemies_list.add(enemy)
                            all_sprites_list.add(enemy)
                            spawn = True
                elif event.type == pygame.USEREVENT+2:
                    self.playPlaylist()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        is_moving_left = True
                    elif event.key == pygame.K_d:
                        is_moving_right = True
                    elif event.key == pygame.K_p:
                        pauseTicks = pygame.time.get_ticks()
                        if (pauseTicks - unpauseTicks)/1000 >= 1:
                            pause = True
                            self.paused()
                            if pygame.key.get_pressed()[pygame.K_a] == False:
                                is_moving_left = False
                            if pygame.key.get_pressed()[pygame.K_d] == False:
                                is_moving_right = False
                            if pygame.key.get_pressed()[pygame.K_SPACE] == False:
                                isShooting = False
                            startTicks += pygame.time.get_ticks() - pauseTicks
                            mirrorTicks += pygame.time.get_ticks() - pauseTicks
                            speed_up_time += pygame.time.get_ticks() - pauseTicks
                            unpauseTicks = pauseTicks
                    elif event.key == pygame.K_r:
                        self.game_loop()
                    if event.key == pygame.K_SPACE:
                        isShooting = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        is_moving_left = False
                        is_moving_right = False
                    if event.key == pygame.K_SPACE:
                        isShooting = False
                        
            if is_moving_left:
                player.subTeta()
                for mirror in mirror_list:
                    mirror.subTeta()
            elif is_moving_right:
                player.addTeta()
                for mirror in mirror_list:
                    mirror.addTeta()

            if isShooting:
                bulletTick = pygame.time.get_ticks()
                if ((bulletTick - lastBulletTick)/1000 >= 0.5/globalspeedmultiplier) and self.ammo <= 0:
                    bullet = Bullet(player, 2*globalspeedmultiplier,white)
                    self.ammo += 20
                    if self.ammo > 0:
                        self.ammo += 40
                    for mirror in mirror_list:
                        mirror_bullet = Bullet(mirror, 2*globalspeedmultiplier,white)
                        all_sprites_list.add(mirror_bullet)
                        bullet_list.add(mirror_bullet)
                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)
                    lastBulletTick = bulletTick
            else:
                if not(self.ammo == -400):
                    self.ammo -=1
            

            if ((pygame.time.get_ticks() - speed_up_time)/1000) >= 5:
                    player.setSpeed(0.01 * globalspeedmultiplier)
                    for mirror in mirror_list:
                        mirror.setSpeed(0.01 * globalspeedmultiplier)

            
            all_sprites_list.update()
            if(self.isStage4):
                endPoint.update()
                endPoint2.update()
            if(self.isStage5 and not self.miniondied):
                shieldminion.update()
            self.blitAll(spawner, player, bullet_list, enemies_list, power_ups_list, mirror_list,endPoint,endPoint2,shieldminion)
            
            if(self.isStage5):
                if(len(pygame.sprite.spritecollide(shieldminion,bullet_list,False))>0):
                    self.miniondied = True
                    self.flag42 = True
                elif(not self.flag42):
                    self.miniondied = False            
            
            
            
            if(((len(pygame.sprite.spritecollide(player, endPoint_list, False))>0) or len(pygame.sprite.spritecollide(endPoint, mirror_list,False))>0 or
                ((len(pygame.sprite.spritecollide(player,endPoint_list2,False))>0 or len(pygame.sprite.spritecollide(endPoint2,mirror_list,False))>0)and(self.ismorehard)))
               and self.isStage4):
                #collide
                pygame.mixer.Sound.play(collideSound)
                secondsToAdd += 1
                self.gothurt = True
                for mirror in mirror_list:
                    mirror_list.remove(mirror)                
                if(self.ammo < 0):
                    self.ammo += 100
                else:
                    self.ammo = 0
                if(enemiesCount*100 + centershots - damagescore >= 200):
                    damagescore += 200
                else:
                    while (enemiesCount*100 + centershots - damagescore > 0):
                        damagescore += 1
                        
            enemiesCrashed = pygame.sprite.spritecollide(player, enemies_list, True)
            for enemy in enemiesCrashed:
                pygame.mixer.Sound.play(collideSound)
                secondsToAdd += 3

            mirrorCrashed = list()
            
            for mirror in mirror_list:
                mirrorCrashed = pygame.sprite.spritecollide(mirror, enemies_list, True)
                secondsToAdd += len(mirrorCrashed)*3
                mirror_list.remove(mirrorCrashed)
            
            if len(enemiesCrashed) !=0 or len(mirrorCrashed) != 0:
                self.gothurt = True
                for mirror in mirror_list:
                    mirror_list.remove(mirror)                
                if(self.ammo < 0):
                    self.ammo += 50
                else:
                    self.ammo = 40
                if(enemiesCount*100 + centershots - damagescore >= 200):
                    damagescore += 200
                else:
                    while (enemiesCount*100 + centershots - damagescore > 0):
                        damagescore += 1 
            
            enemiesDestroyed = pygame.sprite.groupcollide(bullet_list, enemies_list, True, True)
            for enemy in enemiesDestroyed:
                pygame.mixer.Sound.play(destroyedSound)
            if len(enemiesDestroyed) > 0:
                for cene in enemiesDestroyed:
                    if self.ammo > -380: 
                        self.ammo -= 20
            
            enemiesCount += len(enemiesDestroyed)
            secondsToAdd -= len(enemiesDestroyed)*2
            
            self.writeText("Score: " +str(enemiesCount*100 + centershots - damagescore), 20, blue, place = (550,0))
            
            rippleFlagAux = pygame.sprite.spritecollide(spawner,bullet_list,False)
            for bulletAux in rippleFlagAux:
                self.shotcenter = True
                centershots += 1

            
            stage = spawner.getStage()
            if(stage == 1):
                spawningTime = spawner.getSpawner1()
            elif(stage == 2):
                spawningTime = 2000
            elif(stage == 3):
                spawningTime = 3000 
            elif(stage == 4):
                spawningTime = 3000
                self.isStage4 = True
            elif(stage == 5):
                spawningTime = 5000
                self.isStage5 = True
            elif(stage == 6):
                if(not otherflagtest):
                    spawningTime = 1000
                self.miniondied = False
                self.isStage4 = True
                self.ismorehard = True
                otherflagtest = True
                flagtest = True
                self.ammo = -400
                
            if not(stage == 4 or stage ==6):
                self.isStage4 = False
            if not(stage == 5):
                self.isStage5 = False
                self.flag42 = False
            
            
            if stage == 2 and enemiesCount != 0 and not hasSpawnPower:
                if(not self.gothurt):
                    self.powerUpSpawn(power_ups_list, all_sprites_list)
                hasSpawnPower = True
            elif stage != 2:
                hasSpawnPower = False 
                
            
            if not(prevStage == stage):
                stagenum +=1
                self.gothurt = False
                pygame.time.set_timer(SPAWN, spawningTime)
                if(prevStage == 4):
                    self.miniondied = True
                prevStage = stage
                if(stage == 4):
                    endPoint.setDirect()
                    endPoint2.setDirect()
                
              
            if flagtest:
                black = (255,255,255)
                white = (0,0,0)
                green = darker_green
                if(self.lastbool):
                    self.lastbool = False
                    secondsToAdd -= 30
            
            
            pygame.sprite.spritecollide(spawner, bullet_list, True)
            

            self.powerUpCollide(player, power_ups_list, enemies_list, spawner, mirror_list, all_sprites_list)
                    
            self.checkCollisions(enemies_list, power_ups_list,mirror_list,bullet_list)
            
            if(spawner.getloop() >= 3):
                self.ismorehard = True
            
            if not godMode:
                seconds = (pygame.time.get_ticks() - startTicks)/1000 + secondsToAdd
                self.renderTimeText(seconds)
                self.writeText('Level: ' +str(spawner.getloop()), 20, green,(600,560))
            else:
                if not creditsOn:
                    self.writeText('Level: ' +str(spawner.getloop()), 20, green,(340,300))
                    self.writeText('Infinity',30,green,(310,270))
                else:
                    if(auxCreditslider < 12000):
                        auxCreditslider += 1
                    else:
                        auxCreditslider = -500
                    self.writeText('Circumference is a game created by Manuel Silva and Ricardo Pereira - Team GreatQuestion           Music Resources taken from OpenGameArt.org:     "Sky" by Extenz            "Droid Glitch", "Stars" and "Disco Century" by neocry - neocry.com        Sound effects taken from: https://www.freesound.org/              Input box for highscore taken from: http://www.pygame.org/pcr/inputbox/          Playlist idea taken from: https://github.com/danielreis1/Snake           Thank you For Playing =)           ',30,green,(-auxCreditslider,270))
                self.button("Menu", self.getDimensions()[0]/2 + 250, 500, 100, 75, darker_red, red, self.godModeOff)
            
            pygame.display.update()
            self.getClock().tick(60)
