import math
import random
import ast
import pygame
from settings import *
from debug import debug
import numpy
from item import Item
from turtle import Turlte
from other_cars import Other_cars


class Car(pygame.sprite.Sprite):
    def __init__(self, pos ,groups, obstacle_sprites,display_surface,angle,boxes,checkpoint_sprites,item_sprites,car_to_send,network,car_skin,map_num):
        super().__init__(groups)
        # drift_acceleration from 0.1 to 2, max_velocity should be less than 1.5
        pygame.sprite.Sprite.__init__(self)

        self.network = network

        self.obstacle_sprites = obstacle_sprites
        self.checkpoint_sprites = checkpoint_sprites
        self.display_surface = display_surface
        self.item_sprites = item_sprites

        self.boxes = boxes #all the boxes list

        #for the moving:
        self.forward_acceleration = 1.5
        self.backward_acceleration = 2
        self.froward_acceleration_const = 1.5  # the speed while off road
        self.backward_acceleration_const = 2 # the speed while off road
        self.max_velocity = 8
        self.max_velocity_const = 1
        self.drift_acceleration = 0.1
        self.friction = 1.08
        self.velocity_friction = 5

        self.reverse = False #for the reverse

        self.grass_deceleration = -1.2 #for the grass moving
        self.grass_velocity = -1.5 #for the grass velocity

        #input buttons:
        self.button_forward = pygame.K_UP
        self.button_backward = pygame.K_DOWN
        self.button_right = pygame.K_RIGHT
        self.button_left = pygame.K_LEFT

        self.button_power = pygame.K_SPACE

        #for the car image:

        self.car_skin = car_skin
        self.map_num = map_num


        self.original_image = pygame.image.load(f'../graphics/cars/{self.car_skin}').convert_alpha() #the car image
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)
        self.real_x = pos[0]
        self.real_y = pos[1]


        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle) #that the car will start facing its angle
        self.speed = 0 #speed

        self.moving_vector = pygame.Vector2() #the vector of moving

        self.moving_vector.x = 0 #the chage of angle
        self.moving_vector.y = 0 #the change if angle

        self.mask = pygame.mask.from_surface(self.image) #for the collision
        self.on_grass = False
        self.on_finish = False

        #for the chackpoints and finish line
        self.were_in_checkpoints :int = []
        self.lap_num = 0

        #items
        self.item_on = ''
        self.can_bump_items = True
        self.can_bump_items_time = 0


        self.can_move = False #if i can move
        self.start = True #for the beggining of a game
        self.can_move_time = 0

        #for the sending:
        self.car_to_send = car_to_send

        self.car_to_send.update_car_skin(self.car_skin)

        self.items = {}
        self.item_num = 0 #for tracking the item
        self.player = self.network.player #the number of the player in the server

        self.traffic_light_on = False #for starting the game
        self.traffic_light_on_time = 0
        self.empty_light = True
        self.red_light = False
        self.yellow_light = False
        self.green_light = False
        self.the_light_to_display = pygame.image.load('../graphics/light/empty_light.png')

        self.do_sound = True #for the sound
        self.start_sound = pygame.mixer.Sound('../graphics/sound/start_sound.wav')
        self.sound_track = pygame.mixer.Sound('../graphics/sound/sound_track.wav')
        self.end_start_music = pygame.mixer.Sound('../graphics/sound/end_start.wav')
        self.end_loop_music = pygame.mixer.Sound('../graphics/sound/end_loop.wav')
        self.end_loose_start_music = pygame.mixer.Sound('../graphics/sound/end_start_loose.wav')
        self.end_loose_loop_music = pygame.mixer.Sound('../graphics/sound/end_loop_loose.wav')
        self.played_end_loop = False
        self.play_end_start_time = 0
        self.sound_channel = None


        self.didnt_start = True

        self.start_time = 0 #for the clock
        self.number_of_players = 3 #the players amount
        self.lap_time_list = []
        self.gap_time = 0

        self.finished = False #for the end of the race
        self.final_time = 0
        self.didnt_start = True

        #for the cooldowns
        self.can_use_item = True
        self.can_use_item_time = 0

        self.can_mute = True
        self.can_mute_time = 0

        self.can_press_s = True

        self.wait_till_finish = False
        self.wait_till_finish_time = 0


    def start_game(self):
        self.traffic_light_on = True
        self.start = True
        self.traffic_light_on_time = pygame.time.get_ticks()


    def create_turtle(self,rect,angle,item_name):
        Turlte(rect, self.item_sprites, 'turtle', angle,item_name)
        print('created a turtle')

    def create_banana(self,rect,item_name):
        Item(rect, self.item_sprites, 'banana',item_name)
        print('created a banana')

    def input(self):

        pressed = keys = pygame.key.get_pressed()

        #forward and backwards:
        if self.can_move: #if can _move is false, i wont be able to press the forward and backwards buttons
            if pressed[self.button_forward]:
                self.speed += 0.85 / (self.speed + self.forward_acceleration) #the origin
                #self.speed += 0.5
            if pressed[self.button_backward]:
                self.speed -= 0.85 / (abs(self.speed) + self.backward_acceleration)
                self.reverse =True
            elif self.reverse:
                self.reverse = False #if not on reverse

        #sideways:
        if pressed[self.button_left]:  # left turn
            self.turn_left(self.moving_vector.x, self.moving_vector.y)
        if pressed[self.button_right]:  # right turn
            self.turn_right(self.moving_vector.x, self.moving_vector.y)

        if pressed[self.button_power] and self.can_use_item: #power
            if len(self.item_on)!=0:
                if self.item_on == 'banana':
                    name = f'p{self.player}i{self.item_num}'
                    self.item_num += 1
                    new_i = Item(self.rect.center, self.item_sprites, 'banana',name)
                    self.network.send_item(new_i) #for the server update
                    self.can_bump_items = False #to not bump into my own banana imidiatly
                    self.can_bump_items_time = pygame.time.get_ticks()
                if self.item_on == 'turtle':
                    name = f'p{self.player}i{self.item_num}'
                    self.item_num += 1
                    new_t = Turlte(self.rect.center,self.item_sprites,'turtle',self.angle,name)
                    self.network.send_item(new_t)#for the server update
                    self.can_bump_items = False  # to not bump into my own banana imidiatly
                    self.can_bump_items_time = pygame.time.get_ticks()
                self.item_on = ''
                self.can_use_item = False
                self.can_use_item_time = pygame.time.get_ticks()
        if pressed[pygame.K_m] and self.can_mute and self.sound_channel != None:
            #for testing laps
            # current_time = pygame.time.get_ticks()
            # time_since_start = current_time - self.start_time
            # self.were_in_checkpoints.clear()
            # self.lap_num += 1
            # self.network.lap_send(self.lap_num, time_since_start)

            #


            self.can_mute = False
            self.can_mute_time = pygame.time.get_ticks()
            if self.sound_channel.get_volume() == 0:
                self.sound_channel.set_volume(1)
            else:
                self.sound_channel.set_volume(0)
        if self.can_press_s and pressed[pygame.K_s]:
            self.network.start_send()
            # self.didnt_start = False
            # self.traffic_light_on = True
            # self.traffic_light_on_time = pygame.time.get_ticks()
            # self.can_press_s = False


    def acceleration(self):
        self.speed = min(self.max_velocity, self.speed)  # for the valocity not being above max
        self.moving_vector.x += math.sin(math.radians(self.angle)) * self.speed  # for the car rotate of diraction
        self.moving_vector.y += math.cos(math.radians(self.angle)) * self.speed  # for the car rotate of diraction
        self.rect.x += int(self.moving_vector.x)  # for the rect to change
        self.rect.y += int(self.moving_vector.y)  # for the rect to change
        self.real_x += int(self.moving_vector.x)  # for the rect to change
        self.real_y += int(self.moving_vector.y)  # for the rect to change


    def traction(self):
        self.moving_vector.x /= self.friction  # for the turn to be less sharper
        self.moving_vector.y /= self.friction  # for the turn to be less sharper
        self.speed /= self.velocity_friction  # to reduce the speed
        if abs(self.speed) < 0.01 and self.speed != 0:
            self.speed = 0  # to make the speed 0


        self.angle = int(self.angle)
        self.angle %= 360  # for the angle to be 0 < angle < 360




    def turn_left(self, x, y):  #adjusting the object's angle of rotation based on its current movement direction
        if self.reverse:
            self.angle += 2
        else:
            angle = int(+(self.drift_acceleration + (self.speed) / 3) * math.sqrt(x ** 2 + y ** 2)) *3
            self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        center_x, center_y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (center_x, center_y)

    def turn_right(self, x, y):  # adjusting the object's angle of rotation based on its current movement direction
        if self.reverse: #for the reverse turning
            self.angle -= 2
        else:
            angle = int(-(self.drift_acceleration + (self.speed) / 3) * math.sqrt(x ** 2 + y ** 2))*3
            self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        center_x, center_y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (center_x, center_y)

    def collision(self): #for the grass
        try:
            on_grass_now = False
            for obstacle in self.obstacle_sprites:
                if pygame.sprite.collide_mask(self, obstacle):
                    if obstacle.sprite_type == 'grass':
                        on_grass_now = True #for the turn off of on grass function
                        if self.on_grass is False:
                            self.max_velocity -= self.grass_velocity
                            self.forward_acceleration -= self.grass_deceleration
                            self.backward_acceleration -= self.grass_deceleration
                            self.on_grass = True
            if not on_grass_now and self.on_grass: #if not on grass, drive normaly
                self.max_velocity = self.max_velocity_const
                self.forward_acceleration = self.froward_acceleration_const
                self.backward_acceleration = self.backward_acceleration_const
                self.on_grass = False
        except:
            pass

    def finish(self):
        copy_list = self.lap_time_list.copy()
        looser = False
        for dict in copy_list:
            if dict['lap'] != int(MAPS[str(self.map_num)]['lap_num']):
                copy_list.remove(dict)

        for i , dict in enumerate(copy_list):
            if self.final_time == dict['time']:
                if i != 0:
                    self.end_start_music = self.end_loose_start_music
                    self.end_loop_music = self.end_loose_loop_music

        self.can_move = False
        self.sound_channel.stop()
        self.finished = True
        self.play_end_start_time = pygame.time.get_ticks()
        self.sound_channel = self.end_start_music.play()


    def checkpoints_collision(self):
        for checkpoint in self.checkpoint_sprites:
            if pygame.sprite.collide_mask(self,checkpoint):
                if len(self.were_in_checkpoints) == 0:
                    if checkpoint.sprite_type == '1':
                        self.were_in_checkpoints.append(1)
                elif self.were_in_checkpoints[-1] == int(MAPS['1']['checkpoints_num']):
                    if checkpoint.sprite_type == '51': #finished lap!!!
                        current_time = pygame.time.get_ticks()
                        time_since_start = current_time - self.start_time
                        self.were_in_checkpoints.clear()
                        self.lap_num += 1
                        self.network.lap_send(self.lap_num, time_since_start)
                        if self.lap_num == int(MAPS[self.map_num]['lap_num']):
                            self.final_time = time_since_start
                            self.wait_till_finish = True
                            self.wait_till_finish_time = pygame.time.get_ticks()


                else:
                    if int(checkpoint.sprite_type) - 1 == self.were_in_checkpoints[-1]:
                        self.were_in_checkpoints.append(int(checkpoint.sprite_type))


    def item_collision(self):
        copy_items = self.item_sprites.sprites().copy()
        for item in copy_items:
            if pygame.sprite.collide_mask(self, item):
                if item.sprite_type == 'box': #for the box collide
                    if len(self.item_on) == 0: #if i got no items on
                        self.item_on = random.choice(item_list)
                        for box_name , box_dict in self.boxes.items():
                            if item.name == box_name:
                                self.network.delete_box_send(box_name)
                                item.kill() #remove the sprite


                if (item.sprite_type == 'banana' or item.sprite_type == 'turtle') and self.can_bump_items:
                    name = item.name
                    c_items = self.items.copy()
                    for key_names in c_items: #for the server to delete the item for everyone
                        if name == key_names:
                            self.network.delete_item_send(key_names)
                            del self.items[key_names]

                    item.kill()
                    #making the car stop
                    self.speed = 0
                    self.moving_vector.x = 0
                    self.moving_vector.y = 0
                    self.can_move = False
                    self.can_move_time = pygame.time.get_ticks()


    def back_on_box(self,box_name):
        Item(self.boxes[box_name]['location'], self.item_sprites, "box", box_name)  # box create
        self.boxes[box_name]['is_on'] = True


    def timer(self):
        current_time = pygame.time.get_ticks()
        if not self.can_bump_items:
            if current_time - self.can_bump_items_time >= 500:
                self.can_bump_items = True

        if not self.can_move and not self.start:
            if current_time - self.can_move_time >= 1000: #how many time i cant move after a hit
                self.can_move = True
        if not self.can_use_item:
            if current_time - self.can_use_item_time >= 500:
                self.can_use_item = True

        if not self.can_mute:
            if current_time - self.can_mute_time >= 500:
                self.can_mute = True
        if self.wait_till_finish:
            if current_time - self.wait_till_finish_time >= 50:
                self.wait_till_finish = False
                self.finish()


    def traffic_lights(self):
        current_time = pygame.time.get_ticks()
        if self.empty_light:
            if self.do_sound:
                if current_time - self.traffic_light_on_time >= 4000:
                    self.start_sound.play()
                    self.do_sound = False
            else:
                if current_time - self.traffic_light_on_time >= 5000:
                    self.red_light = True
                    self.empty_light = False
                    self.traffic_light_on_time = pygame.time.get_ticks()
                    self.the_light_to_display = pygame.image.load('../graphics/light/red_light.png')

        else:
            if current_time - self.traffic_light_on_time >= 1000:
                if self.red_light:
                    self.the_light_to_display = pygame.image.load('../graphics/light/yellow_light.png')
                    self.yellow_light = True
                    self.red_light = False
                    self.traffic_light_on_time = pygame.time.get_ticks()
                elif self.yellow_light:
                    self.the_light_to_display = pygame.image.load('../graphics/light/green_light.png')
                    self.can_move = True
                    self.yellow_light = False
                    self.green_light = True
                    self.traffic_light_on_time = pygame.time.get_ticks()

                    self.start_time = pygame.time.get_ticks() #for the clock
                elif self.green_light:
                    self.green_light = False
                    self.traffic_light_on = False
                    self.start = False
                    self.sound_channel = self.sound_track.play(loops=-1)




        for i in range(30):
            self.display_surface.blit(self.the_light_to_display, (0 + i * 43, 0))

    def didnt_start_screen_draw(self):
        transparent_surface = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        transparent_surface.fill((0, 0, 0, 0))
        big_rect = pygame.rect.Rect(70, 10, 1150, 200)
        pygame.draw.rect(transparent_surface, (150, 150, 150, 230), big_rect)
        pygame.draw.rect(transparent_surface, (100, 100, 100, 230), big_rect, 3)
        self.display_surface.blit(transparent_surface, (0, 0))

        MENU_TEXT = pygame.font.Font("../graphics/font/joystix.ttf", 80).render("TO START THE GAME", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 50))
        self.display_surface.blit(MENU_TEXT, MENU_RECT)

        MENU_TEXT = pygame.font.Font("../graphics/font/joystix.ttf", 80).render("PRESS S", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 150))
        self.display_surface.blit(MENU_TEXT, MENU_RECT)



    def update(self):
        if not self.finished:
            self.input()  # for the inputs
            self.collision() #for the collisions
            self.checkpoints_collision()
            self.acceleration()  # for the car to gain speed
            self.item_collision() #for the items collision
            self.traction()  # for the traction of the car
        else: #if finished the game
            current_time = pygame.time.get_ticks()
            music_len = self.end_start_music.get_length()
            music_len = int(music_len * 1000)
            if not self.played_end_loop and current_time - self.play_end_start_time >= music_len:
                self.played_end_loop = True
                self.sound_channel = self.end_loop_music.play(loops=-1)



        self.timer()
        self.car_to_send.update_own_data(self.rect,self.angle)

        if self.traffic_light_on:
            self.traffic_lights()

        if self.didnt_start:
            self.didnt_start_screen_draw()


        



