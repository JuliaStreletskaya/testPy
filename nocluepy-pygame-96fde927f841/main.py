import pygame
from GameManager import *

def main():
    pygame.init()
    gameMan = GameManager(800,600)
    gameMan.game_intro()

main()