import pygame
from settings import *
from car import Car
from tile import Tile
from debug import debug
from support import *
from typing import List
from YsortCameraGroup import *
from ui import UI
from item import Item

from _thread import *


class Level:
	def __init__(self,network):

		# get the display surface / the screen
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = YSortCameraGroup()
		self.floor_sprites = YSortCameraGroup()
		self.checkpoint_sprites = YSortCameraGroup()
		self.item_sprites = YSortCameraGroup()

		self.grass_numbers :int = [4,31,33,40,44] #all the grass numbers in the csv file

		#camera
		self.camera = pygame.math.Vector2()



		self.layout: dict[str: List[list[int]]] = {
			'floor' : MAPS['1']['floor'] ,
			'checkpoints' : MAPS['1']['checkpoints']
			#'checkpoints_num' : MAPS['1']['checkpoints_num']
		}

		self.boxes = MAPS['1']['boxes']

		#for the online:
		self.network = network

		#the map building
		self.create_map()

		# floor updating
		self.car_move = [0, 0]
		self.car_prev_location = self.car.rect[0:2]

		#for the ui
		self.ui = UI(self.item_sprites,self.car.lap_num)

		self.item = Item

		self.other_cars = []



	def create_map(self):
		self.car = Car((self.network.getP().pos[:2]), [self.visible_sprites], self.obstacle_sprites, self.display_surface,self.network.getP().angle,self.boxes ,self.checkpoint_sprites,self.item_sprites,self.network.getP())

		self.car_prev_location = self.car.rect[0:2]
		# Center camera
		self.camera.x = self.car.rect.centerx
		self.camera.y = self.car.rect.centery

		#box creating
		for box , values in self.boxes.items():
			Item(values['location'], self.item_sprites, "box")  # item create
			values['is_on'] = True


		#for printing around the player
		car_tile: pygame.math.Vector2 = pygame.math.Vector2(int(self.car.rect.x / TILESIZE),
															int(self.car.rect.y / TILESIZE))
		for style, layout in self.layout.items():
			for row_index in range(int(car_tile.y - ROW_LOAD_TILE_DISTANCE),
								   int(car_tile.y + ROW_LOAD_TILE_DISTANCE)):
				if 0 <= row_index < ROW_TILES:
					row = layout[row_index]
					for col_index in range(int(car_tile.x - COL_LOAD_TILE_DISTANCE),
										   int(car_tile.x + COL_LOAD_TILE_DISTANCE)):
						if 0 <= col_index < COL_TILES:
							col = row[col_index]
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
								tile_path = f'../graphics/tileparts/checkpoint.png'
								image_surf = pygame.image.load(tile_path).convert_alpha()
								Tile((x, y), [self.checkpoint_sprites], f'{col}', image_surf) #the checkpoint type will be his number (51 for finish line)
							else:
								pass

	def floor_update(self):

		car_tile: pygame.math.Vector2 = pygame.math.Vector2(int(self.car.rect.x / TILESIZE),
															   int(self.car.rect.y / TILESIZE))
		self.car_move[0] = (car_tile.x - self.car_prev_location[0] // TILESIZE)
		self.car_move[1] = (car_tile.y - self.car_prev_location[1] // TILESIZE)

		if self.car_move[1] != 0:
			if self.car_move[1] > 0:
				row_index_add = int(car_tile.y + (ROW_LOAD_TILE_DISTANCE - 1))
				row_index_remove = int(car_tile.y - (ROW_LOAD_TILE_DISTANCE))
			else:
				row_index_add = int(car_tile.y - (ROW_LOAD_TILE_DISTANCE - 1))
				row_index_remove = int(car_tile.y + (ROW_LOAD_TILE_DISTANCE))
			self.floor_sprites.remove_sprites_in_rect((row_index_remove * TILESIZE), 1)
			self.obstacle_sprites.remove_sprites_in_rect((row_index_remove * TILESIZE), 1)

			for style_index, (style, layout) in enumerate(self.layout.items()):
				self.floor_sprites.remove_sprites_in_rect(row_index_remove * TILESIZE, 1)
				self.obstacle_sprites.remove_sprites_in_rect(row_index_remove * TILESIZE, 1)
				if 0 <= row_index_add < ROW_TILES:
					row_add = layout[row_index_add]
					for col_index in range(int(car_tile.x - COL_LOAD_TILE_DISTANCE),
										   int(car_tile.x + COL_LOAD_TILE_DISTANCE)):
						if 0 <= col_index < COL_TILES:
							col = row_add[col_index]
							if col != '-1':  # -1 in csv means no tile, don't need to recreate the tile if it already exists
								x: int = col_index * TILESIZE
								y: int = row_index_add * TILESIZE
								self.floor_sprites.remove_sprites_in_rect(row_index_remove * TILESIZE, 1)
								self.obstacle_sprites.remove_sprites_in_rect(row_index_remove * TILESIZE, 1)

								if style == 'floor':
									tile_path = f'../graphics/tileparts/{col}.png'
									image_surf = pygame.image.load(tile_path).convert_alpha()
									if int(col) in self.grass_numbers:
										Tile((x, y), [self.floor_sprites , self.obstacle_sprites], 'grass', image_surf)
									else:
										Tile((x, y), [self.floor_sprites], 'floor', image_surf)
								elif style == 'checkpoints':
									tile_path = f'../graphics/tileparts/checkpoint.png'
									image_surf = pygame.image.load(tile_path).convert_alpha()
									Tile((x, y), [self.checkpoint_sprites], f'{col}', image_surf)  # the checkpoint type will be his number (51 for finish line)
								else:
									pass

		if self.car_move[0] != 0:
			if self.car_move[0] > 0:
				col_index_add = int(car_tile.x + (COL_LOAD_TILE_DISTANCE - 1))
				col_index_remove = int(car_tile.x - (COL_LOAD_TILE_DISTANCE))
			else:
				col_index_add = int(car_tile.x - (COL_LOAD_TILE_DISTANCE - 1))
				col_index_remove = int(car_tile.x + (COL_LOAD_TILE_DISTANCE))
			self.floor_sprites.remove_sprites_in_rect((col_index_remove * TILESIZE), 0)
			self.obstacle_sprites.remove_sprites_in_rect((col_index_remove * TILESIZE), 0)

			for style_index, (style, layout) in enumerate(self.layout.items()):
				for row_index in range(int(car_tile.y - ROW_LOAD_TILE_DISTANCE),
									   int(car_tile.y + ROW_LOAD_TILE_DISTANCE)):
					if 0 <= row_index < ROW_TILES:
						row = layout[row_index]
						if 0 <= col_index_add < COL_TILES:
							col = row[col_index_add]
							if col != '-1':  # -1 in csv means no tile, don't need to recreate the tile if it already exists
								x: int = col_index_add * TILESIZE
								y: int = row_index * TILESIZE

								if style == 'floor':
									tile_path = f'../graphics/tileparts/{col}.png'
									image_surf = pygame.image.load(tile_path).convert_alpha()
									if int(col) in self.grass_numbers:
										Tile((x, y), [self.floor_sprites , self.obstacle_sprites], 'grass', image_surf)
									else:
										Tile((x, y), [self.floor_sprites], 'floor', image_surf)
								elif style == 'checkpoints':
									tile_path = f'../graphics/tileparts/checkpoint.png'
									image_surf = pygame.image.load(tile_path).convert_alpha()
									Tile((x, y), [self.checkpoint_sprites], f'{col}', image_surf)  # the checkpoint type will be his number (51 for finish line)
								else:
									pass

		self.car_prev_location = self.car.rect[0:2]



	def run(self):
		# update and draw the game
		self.floor_sprites.custom_draw(self.car)
		self.floor_sprites.update()

		# to see the chekpoints:
		# self.checkpoint_sprites.custom_draw(self.car)
		# self.checkpoint_sprites.update()

		self.visible_sprites.custom_draw(self.car)
		self.visible_sprites.update()

		self.item_sprites.custom_draw(self.car)
		self.item_sprites.update()

		self.floor_update()

		#turtle move!!1
		for item in self.item_sprites:
			if item.sprite_type == 'turtle':
				item.move()

		self.network.send_car(self.car.car_to_send)
		if self.other_cars != None:
			if len(self.other_cars) != 0:
				for other_car in self.other_cars:
					other_car.blit_other_car(self.car.rect,self.display_surface)

		self.car.item_on = self.ui.ui_update(self.car.lap_num, self.car.item_on) #drawing the ui













