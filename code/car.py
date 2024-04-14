import math
import random

import pygame
from settings import *
from debug import debug
import numpy
from item import Item
from turtle import Turlte


class Car(pygame.sprite.Sprite):
    def __init__(self, pos ,groups, obstacle_sprites,display_surface,angle,boxes,checkpoint_sprites,item_sprites ):
        super().__init__(groups)
        # drift_acceleration from 0.1 to 2, max_velocity should be less than 1.5
        pygame.sprite.Sprite.__init__(self)

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

        self.original_image = pygame.image.load('../graphics/car.png').convert_alpha() #the car image
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
        self.item_on = 'banana'
        self.can_bump_items = True
        self.can_bump_items_time = 0


        self.can_move = True #if i can move
        self.can_move_time = 0



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

        if pressed[self.button_power]: #power
            if len(self.item_on)!=0:
                if self.item_on == 'banana':
                    Item(self.rect.center, self.item_sprites, 'banana')
                    self.can_bump_items = False #to not bump into my own banana imidiatly
                    self.can_bump_items_time = pygame.time.get_ticks()
                # if self.item_on == 'turtle':
                #     Turlte(self.rect.center,self.item_sprites,'turtle',self.angle)
                self.item_on = ''


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

    def checkpoints_collision(self):
        for checkpoint in self.checkpoint_sprites:
            if pygame.sprite.collide_mask(self,checkpoint):
                if len(self.were_in_checkpoints) == 0:
                    if checkpoint.sprite_type == '1':
                        self.were_in_checkpoints.append(1)
                elif self.were_in_checkpoints[-1] == int(MAPS['1']['checkpoints_num']):
                    if checkpoint.sprite_type == '51': #finished lap!!!
                        self.were_in_checkpoints.clear()
                        self.lap_num += 1
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
                            if item.rect[:2] == list(box_dict['location']):
                                box_dict['is_on'] = False
                                box_dict['time_off'] = pygame.time.get_ticks()
                                item.kill()#remove the sprite
                if item.sprite_type == 'banana' and self.can_bump_items:
                    item.kill()
                    #making the car stop
                    self.speed = 0
                    self.moving_vector.x = 0
                    self.moving_vector.y = 0
                    self.can_move = False
                    self.can_move_time = pygame.time.get_ticks()


    def box_return(self):
        current_time = pygame.time.get_ticks()
        for box_name, box_dict in self.boxes.items():
            if box_dict['is_on'] == False:
                if current_time - box_dict['time_off'] >= box_retime:
                    Item(box_dict['location'], self.item_sprites, "box")  # box create
                    box_dict['is_on'] = True

    def timer(self):
        current_time = pygame.time.get_ticks()
        if not self.can_bump_items:
            if current_time - self.can_bump_items_time >= 500:
                self.can_bump_items = True

        if not self.can_move:
            if current_time - self.can_move_time >= 1000: #how many time i cant move after a hit
                self.can_move = True


    def update(self):

        self.input()  # for the inputs
        self.collision() #for the collisions
        self.checkpoints_collision()
        self.acceleration()  # for the car to gain speed
        self.item_collision() #for the items collision
        self.box_return() #for the boxes to be back after disappering
        self.timer()

        self.traction()  # for the traction of the car

        #debug(str(self.moving_vector.x) + '  ,  ' + str(self.moving_vector.y) )
        #debug(self.were_in_checkpoints)
        debug(self.can_bump_items)
        



