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

        self.font_15 = pygame.font.Font("../graphics/font/joystix.ttf", 15)





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
        path = item_data[item_on]['icon']
        image = pygame.image.load(path).convert_alpha()
        item_surf = image
        item_rect = item_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(item_surf, item_rect)


    def draw_every_lap_time(self,list):
        transparent_surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        big_rect = pygame.rect.Rect(10, 10, 325, 30)
        pygame.draw.rect(transparent_surface, (150, 150, 150, 160), big_rect)
        pygame.draw.rect(transparent_surface, (100, 100, 100, 160), big_rect, 3)

        place_list = [{'name':'player_1','time': 20549, 'gap':0},{'name':'player_2','time': 21579, 'gap':0},{'name':'player_3','time': 24549, 'gap':0}]

        for i , dict in enumerate(place_list):
            big_rect = pygame.rect.Rect(10, 37+i*27, 325, 30)
            pygame.draw.rect(transparent_surface, (60, 60, 60, 160), big_rect)
            pygame.draw.rect(transparent_surface, (100, 100, 100, 160), big_rect, 3)



            #for the gap
            gap_time = dict['time'] - place_list[0]['time'] - dict['gap']
            dig = len(str(gap_time))
            if dig < 5:
                gap_time_str = '0' * (5 - dig) + str(gap_time)
            else:
                gap_time_str = str(gap_time)
            split_index = len(gap_time_str) - 3
            gap_time_str = gap_time_str[:split_index] + "." + gap_time_str[split_index:]

            if gap_time < dict['gap']:
                gap_time_str = f" -{gap_time_str}"
                color = 'green'
            elif gap_time > dict['gap']:
                gap_time_str = f" +{gap_time_str}"
                color = 'red'
            else: #for 0 gap
                gap_time_str = f" +{gap_time_str}"
                color = 'grey'

            time_text = self.font_15.render(gap_time_str, True,color)
            time_text_rect = time_text.get_rect(topleft=(big_rect.x + 200, big_rect.y + 5))
            self.display_surface.blit(time_text, time_text_rect)




            time = str(dict['time'])
            split_index = len(time) - 3
            time = time[:split_index] + "." + time[split_index:]

            time_text = self.font_15.render(f"{dict['name']}: {time}", True, (180, 180, 180))
            time_text_rect = time_text.get_rect(topleft=(big_rect.x+5, big_rect.y +5))
            self.display_surface.blit(time_text, time_text_rect)

        self.display_surface.blit(transparent_surface, (0, 0))


        time_text = self.font_15.render('laps time:', True, (40, 40, 40))
        time_text_rect = time_text.get_rect(topleft=(15, 15))
        self.display_surface.blit(time_text, time_text_rect)





    def draw_time(self,time_past):
        current_time = pygame.time.get_ticks()
        time = current_time - time_past
        time = str(time)

        split_index = len(time) - 3
        time = time[:split_index] + "." + time[split_index:]

        transparent_surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        big_rect = pygame.rect.Rect(10, 670, 165, 30)
        pygame.draw.rect(transparent_surface, (150, 150, 150, 230), big_rect)
        pygame.draw.rect(transparent_surface, (100, 100, 100, 230), big_rect, 3)
        self.display_surface.blit(transparent_surface, (0, 0))

        time_text = pygame.font.Font("../graphics/font/joystix.ttf", 15).render(time, True, (40,40,40))
        time_text_rect = time_text.get_rect(topleft=(73, 675))
        self.display_surface.blit(time_text, time_text_rect)

        time_text = pygame.font.Font("../graphics/font/joystix.ttf", 15).render('time: ', True, (40, 40, 40))
        time_text_rect = time_text.get_rect(topleft=(13, 675))
        self.display_surface.blit(time_text, time_text_rect)


    def ui_update(self,lap_num,item_on,players_num,time_past):
        self.draw_lap_num(lap_num)
        if len(item_on) != 0:
            self.draw_item(item_on)
        self.draw_every_lap_time(players_num)
        self.draw_time(time_past)



        return item_on #if i has droped an item it will be empty

