import pygame

class Rocket():

    def __init__(self, ai_settings, screen):
    #Инициализирует ракету и задает ее начальную позицию

        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('rocket2.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Каждая новая ракета появляется в центре экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.center = self.screen_rect.center

        #Сохранение вещественной координаты ракеты
        self.center = float(self.rect.centerx) 

        #Флаги перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False

    def update(self):
        #Обновляет позицию ракеты с учетом флагов
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.rocket_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.rocket_speed_factor
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.center += self.ai_settings.rocket_speed_factor
        if self.moving_top and self.rect.top > 0:
            self.center -= self.ai_settings.rocket_speed_factor

        #Обновление атрибута rect на основании self.center
        self.rect.centerx = self.center

    def blitme(self):
        #Вывод изображения ракеты на экран
        self.screen.blit(self.image, self.rect)

