import pygame
from settings import *
from car import Car
from tile import Tile
from debug import debug
from support import *
from typing import List
from YsortCameraGroup import *

class Level:
	def __init__(self):

		# get the display surface / the screen
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.floor_sprites = YSortCameraGroup()
		self.checkpoint_sprites = pygame.sprite.Group()

		self.grass_numbers = [4,31,33,40,44] #all the grass numbers in the csv file



		self.layout: dict[str: List[list[int]]] = {
			'floor' : MAPS['1']['floor'] ,
			'checkpoints' : MAPS['1']['checkpoints'],
			'checkpoints_num' : MAPS['1']['checkpoints_num']
		}

		#the map building
		self.create_map()

	def create_map(self):
		self.car = Car((1536, 832), [self.visible_sprites], self.obstacle_sprites, self.display_surface,180,self.checkpoint_sprites)
		for style, layout in self.layout.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE

						if style == 'floor':
							tile_path = f'../graphics/tileparts/{col}.png'
							image_surf = pygame.image.load(tile_path).convert_alpha()
							if int(col) in self.grass_numbers:
								Tile((x, y), [self.floor_sprites,self.obstacle_sprites], 'grass', image_surf)
							else:
								Tile((x, y), [self.floor_sprites], 'floor', image_surf)
						elif style == 'checkpoints':
							Tile((x, y), [self.checkpoint_sprites], f'{col}', image_surf) #the checkpoint type will be his number (51 for finish line)
						else:
							pass

	def run(self):
		# update and draw the game
		self.floor_sprites.custom_draw(self.car)
		self.floor_sprites.update()

		self.visible_sprites.custom_draw(self.car)
		self.visible_sprites.update()


