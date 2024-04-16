import pygame

class Other_cars(pygame.sprite.Sprite):
    def __init__(self,name,pos,angle):
        self.name = name
        self.original_image = pygame.image.load('../graphics/car.png').convert_alpha()  # the car image