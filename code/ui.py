import pygame
from settings import *
from debug import debug
from car import Car

class UI:
    def __init__(self , item_sprites,num_lap):
        #general
        self.display_surface = pygame.display.get_surface()
        self.font =pygame.font.Font(UI_FONT,UI_FONT_SIZE) #our font
        self.item_sprites = item_sprites
        self.number_of_laps = MAPS['1']['lap_num']
        self.num_lap = num_lap





    def draw_lap_num(self,lap_num):
        text_surf = self.font.render(f'lap {lap_num}/{self.number_of_laps}', False, TEXT_COLOR)
        x = 1240  # where we put the abr
        y = 45
        text_rect = text_surf.get_rect(bottomright=(x, y))  # the bar

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate((45, 15)))  # filling the exp bar box
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate((45, 15)),3)  # borders to the exp bar

        self.display_surface.blit(text_surf, text_rect)

    def draw_item(self,item_on):
        #the box
        bg_rect = pygame.Rect(1180, 620, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        #the item
        path = item_data[item_on]['graphic']
        image = pygame.image.load(path).convert_alpha()
        item_surf = image
        item_rect = item_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(item_surf, item_rect)




    def ui_update(self,lap_num,item_on):
        self.draw_lap_num(lap_num)
        if len(item_on) != 0:
            self.draw_item(item_on)


        return item_on #if i has droped an item it will be empty

