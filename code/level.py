import pygame
from settings import *
from car import Car
from tile import Tile
from debug import debug

class Level:
	def __init__(self):

		# get the display surface / the screen
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		#the map building
		self.create_map()

	def create_map(self):
		for row_index,row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Tile((x,y),[self.visible_sprites,self.obstacle_sprites], 'rock')
				if col == 'p':
					self.car = Car((x,y),[self.visible_sprites],self.obstacle_sprites,self.display_surface)

	def run(self):
		# update and draw the game
		self.visible_sprites.custom_draw(self.car)
		self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

	def custom_draw(self,car):

		# getting the offset
		self.offset.x = car.rect.centerx - self.half_width
		self.offset.y = car.rect.centery - self.half_height

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			# if sprite is not car:
			# 	offset_pos = sprite.rect.topleft - self.offset
			# 	self.display_surface.blit(sprite.image,offset_pos)
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)
