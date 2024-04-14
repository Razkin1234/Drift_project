import pygame
from settings import *
import math

class Turlte(pygame.sprite.Sprite):
    def __init__(self, pos, groups, item_type,angle):
        super().__init__(groups)
        path = item_data[item_type]['graphic']
        self.sprite_type = item_type
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)  # if i want to overlap itemes
        self.angle = angle
        self.vector = pygame.math.Vector2(self.vector_culc()).normalize() * 8 #the vector times the speed


        self.creation_time = pygame.time.get_ticks() #the time of the turtle criation

        self.turtle_die = False #to kill the turtle from outside of this class

        self.rect.x += self.vector.x *8
        self.rect.y += self.vector.y*8
        self.hitbox.x += self.vector.x*8
        self.hitbox.y += self.vector.y*8



    def vector_culc(self):
        # Convert angle from degrees to radians
        angle_rad = math.radians(self.angle)

        # Calculate the x and y components of the vector using trigonometry
        y_component =  math.cos(angle_rad)
        x_component =  math.sin(angle_rad)

        return x_component, y_component

    def move(self):
        self.rect.x += self.vector.x
        self.rect.y += self.vector.y
        self.hitbox.x += self.vector.x
        self.hitbox.y += self.vector.y

    def turtle_kill(self): #if a lot of time has passed there is no need for the turtle
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time >= 20000:
            self.turtle_die = True #i will kill him frim outside of this class


