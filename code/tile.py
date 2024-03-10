import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type):
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.image = pygame.image.load('../graphics/rock.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0,0)

