import math
import pygame
from settings import *
from debug import debug
import numpy


class Car(pygame.sprite.Sprite):
    def __init__(self, pos ,groups, obstacle_sprites,display_surface ):
        super().__init__(groups)
        # drift_acceleration from 0.1 to 2, max_velocity should be less than 1.5
        pygame.sprite.Sprite.__init__(self)

        self.obstacle_sprites = obstacle_sprites
        self.display_surface = display_surface

        #fir the moving:
        self.forward_acceleration = 1.0
        self.backward_acceleration = 1.0
        self.froward_acceleration_const = 1.0  # the speed while off road
        self.backward_acceleration_const = 1.0 # the speed while off road
        self.max_velocity = 0.8
        self.max_velocity_const = 1.0
        self.drift_acceleration = 0.3
        self.friction = 1.08
        self.velocity_friction = 5

        #for the car image:

        self.original_image = pygame.image.load('../graphics/car.png').convert_alpha() #the car image
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)
        self.real_x = pos[0]
        self.real_y = pos[1]


        self.angle = 0
        self.velocity = 0
        self.delta_x = 0 #the chage
        self.delta_y = 0 #the change
        self.mask = pygame.mask.from_surface(self.image) #for the collision
        self.on_grass = False
        self.on_finish = False


    def input(self):

        pressed = keys = pygame.key.get_pressed()

        #forward and backwards:
        if pressed[pygame.K_w]:
            self.velocity += 1 / (self.velocity + self.forward_acceleration)
        if pressed[pygame.K_s]:
            self.velocity -= 1 / (self.velocity + self.backward_acceleration)

        #sideways:
        if pressed[pygame.K_a]:  # left turn
            self.turn_left(self.delta_x, self.delta_y)
        if pressed[pygame.K_d]:  # right turn
            self.turn_right(self.delta_x, self.delta_y)


    def update(self):

        self.input()#for the inputs


        self.velocity = min(self.max_velocity, self.velocity) #for the valocity not being above max
        self.delta_x += math.sin(math.radians(self.angle)) * self.velocity #for the car rotate of diraction
        self.delta_y += math.cos(math.radians(self.angle)) * self.velocity #for the car rotate of diraction
        self.rect.x += int(self.delta_x) #for the rect to change
        self.rect.y += int(self.delta_y) #for the rect to change
        self.real_x += int(self.delta_x) #for the rect to change
        self.real_y += int(self.delta_y) #for the rect to change


        # for the traction of the car
        self.delta_x /= self.friction #for the turn to be less sharper
        self.delta_y /= self.friction #for the turn to be less sharper
        self.velocity /= self.velocity_friction #for the next time sharper
        if abs(self.velocity) < 0.01: self.velocity = 0  # to make the velocity 0
        self.angle = int(self.angle)
        self.angle %= 360  # for the angle to be 0 < angle < 360


    def turn_left(self, x, y):  #adjusting the object's angle of rotation based on its current movement direction
        angle = int(+(self.drift_acceleration + self.velocity / 3) * math.sqrt(x ** 2 + y ** 2))
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        center_x, center_y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (center_x, center_y)

    def turn_right(self, x, y):  # adjusting the object's angle of rotation based on its current movement direction
        angle = int(-(self.drift_acceleration + self.velocity / 3) * math.sqrt(x ** 2 + y ** 2))
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        center_x, center_y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (center_x, center_y)




