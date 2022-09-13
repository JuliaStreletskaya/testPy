import sys

import pygame

from elephant12_2 import Elephant

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((1200,700))
    pygame.display.set_caption("Sky")

    bg_color = (0, 0, 100)
    elephant = Elephant(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(bg_color)
        elephant.blitme()
        pygame.display.flip()
        

run_game()