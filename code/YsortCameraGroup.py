from settings import *
from car import Car
from debug import debug
import itertools
import  pygame



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

	def remove_sprites_in_rect(self, rect, axis):
		for sprite in sorted(self.sprites(), key=lambda x: (x.rect.centery)):
			if sprite.rect.topleft[axis] == rect:
				sprite.kill()

	def earase_non_relevant_sprites(self, player):
		for sprite in self.sprites():
			if player.rect[0] - (COL_LOAD_TILE_DISTANCE * TILESIZE) > sprite.rect[0] or sprite.rect[0] > player.rect[
				0] + (COL_LOAD_TILE_DISTANCE * TILESIZE):
				sprite.kill()
			if player.rect[1] - (ROW_LOAD_TILE_DISTANCE * TILESIZE) > sprite.rect[1] or sprite.rect[1] > player.rect[
				1] + (ROW_LOAD_TILE_DISTANCE * TILESIZE):
				sprite.kill()

