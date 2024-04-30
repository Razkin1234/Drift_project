import pygame
from settings import *
from debug import debug
from car import Car

class UI:
    def __init__(self , item_sprites,num_lap,map_num):
        #general
        self.display_surface = pygame.display.get_surface()
        self.font =pygame.font.Font(UI_FONT,UI_FONT_SIZE) #our font
        self.item_sprites = item_sprites
        self.map_num = map_num
        self.number_of_laps = MAPS[self.map_num]['lap_num']
        self.num_lap = num_lap

        self.font_15 = pygame.font.Font("../graphics/font/joystix.ttf", 15)
        self.font_36 = pygame.font.Font("../graphics/font/joystix.ttf", 36)





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


    def draw_every_lap_time(self,lap_list):
        lap_list = sorted(lap_list, key=lambda x: (-x['lap'], x['time']))

        transparent_surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        big_rect = pygame.rect.Rect(10, 10, 340, 30)
        pygame.draw.rect(transparent_surface, (150, 150, 150, 160), big_rect)
        pygame.draw.rect(transparent_surface, (100, 100, 100, 160), big_rect, 3)

        #place_list = [{'name':'player_1','time': 20549, 'gap':0},{'name':'player_2','time': 21579, 'gap':0},{'name':'player_3','time': 24549, 'gap':0}]

        for i , dict in enumerate(lap_list):
            big_rect = pygame.rect.Rect(10, 37+i*27, 340, 30)
            pygame.draw.rect(transparent_surface, (60, 60, 60, 160), big_rect)
            pygame.draw.rect(transparent_surface, (100, 100, 100, 160), big_rect, 3)


            time = str(dict['time'])
            time_len = len(time)
            if time_len < 4:
                time = '0' * (4 - time_len) + time

            split_index = len(time) - 3
            time = time[:split_index] + "." + time[split_index:]

            time_text = self.font_15.render(f"{i+1}. {dict['name']}: {time}  lap:{dict['lap']}", True, (80, 80, 80))
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


    def draw_every_lap_time_finish(self,lap_list,final_time):
        #lap_list = sorted(lap_list, key=lambda x: (-x['lap'], x['time']))
        copy_list = lap_list.copy()
        for dict in copy_list:
            if dict['lap'] != int(self.number_of_laps):
                lap_list.remove(dict)


        transparent_surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        big_rect = pygame.rect.Rect(250, 75, 780, 72)
        pygame.draw.rect(transparent_surface, (125, 125, 125, 255), big_rect)
        pygame.draw.rect(transparent_surface, (100, 100, 100, 255), big_rect, 7)

        #lap_list = [{'name':'player_1','time': 20549, 'lap':9},{'name':'player_2','time': 21579, 'lap':7},{'name':'player_3','time': 24549, 'lap':8}]


        for i , dict in enumerate(lap_list):
            if dict['time'] == final_time:
                color = (125, 150, 125, 255)
            else:
                color = (150, 150, 150, 255)
            big_rect = pygame.rect.Rect(250, 142+i*65, 780, 72)
            pygame.draw.rect(self.display_surface, color, big_rect)
            pygame.draw.rect(self.display_surface, (100, 100, 100, 255), big_rect, 7)


            time = str(dict['time'])
            time_len = len(time)
            if time_len < 4:
                time = '0' * (4 - time_len) + time

            split_index = len(time) - 3
            time = time[:split_index] + "." + time[split_index:]

            time_text = self.font_36.render(f"  {dict['name']}: {time}", True, (230, 230, 230))
            time_text_rect = time_text.get_rect(topleft=(big_rect.x+12, big_rect.y +12))
            self.display_surface.blit(time_text, time_text_rect)
            time_text = self.font_36.render(f"{i + 1}", True, 'blue')
            time_text_rect = time_text.get_rect(topleft=(big_rect.x + 12, big_rect.y + 12))
            self.display_surface.blit(time_text, time_text_rect)

        self.display_surface.blit(transparent_surface, (0, 0))


        time_text = self.font_36.render('laps time:', True, 'black')
        time_text_rect = time_text.get_rect(topleft=(262, 87))
        self.display_surface.blit(time_text, time_text_rect)




    def ui_update(self,lap_num,item_on,lap_list,time_past):
        self.draw_lap_num(lap_num)
        if len(item_on) != 0:
            self.draw_item(item_on)
        self.draw_every_lap_time(lap_list)
        self.draw_time(time_past)
        return item_on  #if i has droped an item it will be empty

    def finish_update(self,lap_list,final_time):
        self.draw_every_lap_time_finish(lap_list,final_time)


