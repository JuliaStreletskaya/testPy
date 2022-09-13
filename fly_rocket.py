import pygame

from fly_settings import FlySettings

from rocket import Rocket

import fly_functions as ff

def run_game():
    pygame.init()
    ai_settings = FlySettings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Fly Rocket")

    #Создание ракеты
    rocket = Rocket(ai_settings, screen)

    #Запуск основного цикла игры
    while True:
        ff.check_events(rocket)
        rocket.update()
        ff.update_screen(ai_settings, screen, rocket)

    
run_game()
