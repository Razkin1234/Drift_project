import pygame
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, groups, item_type,name):
        super().__init__(groups)
        path = item_data[item_type]['graphic']
        self.name = name
        self.sprite_type = item_type
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, 0)  # if i want to overlap itemes

