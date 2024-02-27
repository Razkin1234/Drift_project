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
        self.direction = pygame.math.Vector2() #the car movement
        self.speed = 0
        self.angle = 0
        self.gas = False
        self.max_speed = 10
        self.reverse = False #for the slowing down while reversing
        self.max_reverse_speed = -6

        #the screen:
        self.display_surface = display_surface

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_UP]: #for the gas cancelation
            self.gas = False
        if not keys[pygame.K_DOWN]: #for the reverse cancelation
            self.reverse = False
        if keys[pygame.K_UP]:
            self.gas = True
        elif keys[pygame.K_DOWN]:
            if self.speed > 0:
                self.brake()
            else:
                self.reverse = True #reverse mehod here

        if keys[pygame.K_RIGHT]:
            self.trun(-3)
        elif keys[pygame.K_LEFT]:
            self.trun(3)


    def brake(self):   #making the car stop
        if self.speed != 0:
            self.speed = self.speed * 0.95
        if self.speed < 0:
            self.speed = 0
    def trun(self,turn):
        if self.speed != 0:
            turn = (self.speed/10)*turn
            self.angle += turn
            if 360 < self.angle or self.angle < 0:
                self.angle = self.angle % 360

    def acceleraion(self): #for the moving (forward or backwards)
        if self.gas:
            if self.speed != self.max_speed: #for not passing the max speed
                if self.speed < 0:
                    self.speed += 0.1
                else:
                    self.speed += 0.05
            if self.speed > self.max_speed: #for not passing the max speed
                self.speed = self.max_speed
        elif self.reverse: #for the reversing
            if self.speed != self.max_reverse_speed:
                self.speed -= 0.025
                print(self.speed)
            if self.speed < self.max_reverse_speed:
                self.speed = self.max_reverse_speed
        else:
            if self.speed > 0: #making the car slower if gas isnt pressed
                self.speed -= 0.05
            if self.speed < 0: #to wlow down whilel reversing
                self.speed += 0.05
            if -0.05 < self.speed < 0.05: #to fix a bug
                if not self.reverse and not self.gas:
                    self.speed = 0


    def move(self):
        self.direction.x += self.speed * math.cos(math.radians(self.angle + 90))
        self.direction.y -= self.speed * math.sin(math.radians(self.angle + 90))

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.direction.x += self.speed * math.cos(math.radians(self.angle+90))
            self.direction.y -=  self.speed * math.sin(math.radians(self.angle+90))

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

    def draw_img(self):
        offset = pygame.math.Vector2()
        offset.x = self.rect.centerx - 640
        offset.y = self.rect.centery - 360
        offset_pos = self.rect.topleft - offset
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.display_surface.blit(rotated_image, rotated_image.get_rect(center=self.image.get_rect(topleft=(offset_pos.x, offset_pos.y)).center).topleft)
        self.rect = self.image.get_rect(center=self.rect.center)
    def update(self):
        self.input() #gets an input from keybord
        self.move() #making the car move
        self.draw_img() #draws the car
        self.acceleraion() #for the car speed


        if self.speed == 0 : #if the speed=0 i wont move.
            self.direction = pygame.math.Vector2(0, 0)

        debug(self.speed)



