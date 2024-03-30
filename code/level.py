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

		self.layout: dict[str: List[list[int]]] = {
			'floor': import_csv_layout('../maps/1/map1.csv') }
			#'boundary': import_csv_layout('../map/map_FloorBlocks.csv')
			# ,'entities': import_csv_layout('../map/map_Entities.csv')

		#the map building
		self.create_map()

	def create_map(self):
		self.car = Car((1472, 832), [self.visible_sprites], self.obstacle_sprites, self.display_surface)
		for style, layout in self.layout.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE

						if style == 'floor':
							tile_path = f'../graphics/tileparts/{col}.png'
							image_surf = pygame.image.load(tile_path).convert_alpha()
							Tile((x, y), [self.floor_sprites], 'floor', image_surf)

						else:
							pass

	def run(self):
		# update and draw the game
		self.floor_sprites.custom_draw(self.car)
		self.floor_sprites.update()

		self.visible_sprites.custom_draw(self.car)
		self.visible_sprites.update()


