import math
import pygame
from settings import *


class Car(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites,display_surface):
        super().__init__(groups)
        #sprite things
        self.image = pygame.image.load('../graphics/car.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, 0)

        #moving things
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.angle = 0

        #the screen:
        self.display_surface = display_surface

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.x += self.speed * math.cos(math.radians(self.angle + 90))
            self.direction.y -= self.speed * math.sin(math.radians(self.angle + 90))
        elif keys[pygame.K_DOWN]:
            self.direction.x -= self.speed * math.cos(math.radians(self.angle + 90))
            self.direction.y += self.speed * math.sin(math.radians(self.angle + 90))
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.turn(-3)
        elif keys[pygame.K_LEFT]:
            self.turn(3)
        else:
            self.direction.x = 0

    def turn(self, angle_change):
        self.angle += angle_change
        if 0 <= self.angle >= 360:
            self.angle = self.angle % 360
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)
        rotated_car = pygame.transform.rotate(self.image, self.angle)
        rotated_car_rect = rotated_car.get_rect(center=(self.direction.x,self.direction.y))
        self.display_surface.blit(rotated_car,rotated_car_rect)

