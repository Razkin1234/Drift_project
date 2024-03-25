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

        #for the moving:
        self.forward_acceleration = 1.0
        self.backward_acceleration = 1.0
        self.froward_acceleration_const = 1.0  # the speed while off road
        self.backward_acceleration_const = 1.0 # the speed while off road
        self.max_velocity = 8
        self.max_velocity_const = 1
        self.drift_acceleration = 0.1
        self.friction = 1.08
        self.velocity_friction = 5

        #input buttons:
        self.button_forward = pygame.K_UP
        self.button_backward = pygame.K_DOWN
        self.button_right = pygame.K_RIGHT
        self.button_left = pygame.K_LEFT

        #for the car image:

        self.original_image = pygame.image.load('../graphics/car.png').convert_alpha() #the car image
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)
        self.real_x = pos[0]
        self.real_y = pos[1]


        self.angle = 0
        self.speed = 0 #speed
        
        self.moving_vector = pygame.Vector2() #the vector of moving

        self.moving_vector.x = 0 #the chage of angle
        self.moving_vector.y = 0 #the change if angle

        self.mask = pygame.mask.from_surface(self.image) #for the collision
        self.on_grass = False
        self.on_finish = False


    def input(self):

        pressed = keys = pygame.key.get_pressed()

        #forward and backwards:
        if pressed[self.button_forward]:
            self.speed += 0.85 / (self.speed + self.forward_acceleration) #the origin
            #self.speed += 0.5
        if pressed[self.button_backward]:
            self.speed -= 0.85 / (abs(self.speed) + self.backward_acceleration)

        #sideways:
        if pressed[self.button_left]:  # left turn
            self.turn_left(self.moving_vector.x, self.moving_vector.y)
        if pressed[self.button_right]:  # right turn
            self.turn_right(self.moving_vector.x, self.moving_vector.y)


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
        angle = int(+(self.drift_acceleration + self.speed / 3) * math.sqrt(x ** 2 + y ** 2))
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        center_x, center_y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (center_x, center_y)

    def turn_right(self, x, y):  # adjusting the object's angle of rotation based on its current movement direction
        angle = int(-(self.drift_acceleration + self.speed / 3) * math.sqrt(x ** 2 + y ** 2))
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        center_x, center_y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (center_x, center_y)

    def collision(self):
        # Iterate through each obstacle tile
        for obstacle in self.obstacle_sprites:
            if pygame.sprite.collide_mask(self, obstacle):
                self.rect.x -= int(self.moving_vector.x)+2 # Move back based on the change in x
                self.rect.y -= int(self.moving_vector.y)+2  # Move back based on the change in y
                self.real_x -= int(self.moving_vector.x)+2  # Update the real x position
                self.real_y -= int(self.moving_vector.y)+2  # Update the real y position

                self.speed = 0 #for
                self.moving_vector.x = -int(self.moving_vector.x)
                self.moving_vector.y = -int(self.moving_vector.y)

    def update(self):

        self.input()  # for the inputs
        if self.speed != 0: #you can collide only when you are moving
            self.collision() #for the collisions
        self.acceleration()  # for the car to gain speed

        self.traction()  # for the traction of the car

        #debug(str(self.moving_vector.x) + '  ,  ' + str(self.moving_vector.y) )
        debug(self.drift_acceleration)
        



