import math
import pygame
from settings import *
from debug import debug


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
            #brake will be here
            pass
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.trun(-3)
        elif keys[pygame.K_LEFT]:
            self.trun(3)
        else:
            self.direction.x = 0

    def trun(self,turn):
        self.angle += turn
        if 360 < self.angle or self.angle < 0:
            self.angle = self.angle % 360

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.direction.x += speed * math.cos(math.radians(self.angle+90))
            self.direction.y -=  speed * math.sin(math.radians(self.angle+90))

        self.hitbox.x += self.direction.x
        self.collision('horizontal')
        self.hitbox.y += self.direction.y
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

    def rotate_car(self):
        rotated_car = pygame.transform.rotate(self.image , self.angle)
        new_rect = self.image.get_rect(center= self.image.get_rect(topleft = self.rect.topleft).center)
        self.display_surface.blit(rotated_car,new_rect.topleft)
    def update(self):
        self.input()
        self.move(self.speed)
        debug(self.angle)
        self.rotate_car()


