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
        self.delta_x = 0 #the chage of angle
        self.delta_y = 0 #the change if angle
        self.mask = pygame.mask.from_surface(self.image) #for the collision
        self.on_grass = False
        self.on_finish = False


    def input(self):

        pressed = keys = pygame.key.get_pressed()

        #forward and backwards:
        if pressed[self.button_forward]:
            self.speed += 1 / (self.speed + self.forward_acceleration) #the origin
            #self.speed += 0.5
        if pressed[self.button_backward]:
            self.speed -= 1 / (abs(self.speed) + self.backward_acceleration)

        #sideways:
        if pressed[self.button_left]:  # left turn
            self.turn_left(self.delta_x, self.delta_y)
        if pressed[self.button_right]:  # right turn
            self.turn_right(self.delta_x, self.delta_y)


    def acceleration(self):
        self.speed = min(self.max_velocity, self.speed)  # for the valocity not being above max
        self.delta_x += math.sin(math.radians(self.angle)) * self.speed  # for the car rotate of diraction
        self.delta_y += math.cos(math.radians(self.angle)) * self.speed  # for the car rotate of diraction
        self.rect.x += int(self.delta_x)  # for the rect to change
        self.rect.y += int(self.delta_y)  # for the rect to change
        self.real_x += int(self.delta_x)  # for the rect to change
        self.real_y += int(self.delta_y)  # for the rect to change


    def traction(self):
        self.delta_x /= self.friction  # for the turn to be less sharper
        self.delta_y /= self.friction  # for the turn to be less sharper
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
            # Check for collision between the car's mask and the obstacle's mask
            if pygame.sprite.collide_mask(self, obstacle):

                # Handle collision - for example, adjust the car's position
                # Here you can implement how you want to handle the collision,
                # for example, stopping the car or adjusting its position
                self.rect.x -= int(self.delta_x)  # Move back based on the change in x
                self.rect.y -= int(self.delta_y)  # Move back based on the change in y
                self.real_x -= int(self.delta_x)  # Update the real x position
                self.real_y -= int(self.delta_y)  # Update the real y position
                # Reset speed and acceleration to avoid getting stuck
                self.speed = 0
                self.delta_x = 0
                self.delta_y = 0
                # Optionally, you can add additional logic here based on the collision
                # For example, if the obstacle is a finish line, set self.on_finish = True

                # Depending on your game logic, you might want to break out of the loop
                # if you only want to handle one collision at a time
                # break

    def update(self):

        self.input()  # for the inputs
        if self.speed != 0: #you can collide only when you are moving
            self.collision() #for the collisions
        self.acceleration()  # for the car to gain speed

        self.traction()  # for the traction of the car

        debug(str(self.delta_x) + '  ,  ' + str(self.delta_y) )



