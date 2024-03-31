import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))): #make a sprite tile
		super().__init__(groups)
		self.sprite_type = sprite_type
		self.image = surface
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect
		if sprite_type == 'grass':
			self.hitbox = self.hitbox.inflate(10,10) #for the grass hitbox
		else:
			self.hitbox = self.rect.inflate(0,0)

