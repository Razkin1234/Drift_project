import pygame

class Other_cars(pygame.sprite.Sprite):
    def __init__(self,name,pos,angle,car_skin):
        self.name = name
        self.car_skin = car_skin
        #self.original_image = pygame.image.load(f'../graphics/cars/{car_skin}').convert_alpha()  # the car image
        self.pos = pos #the position of the car
        self.angle = angle #the angle of the car




    def update_own_data(self,pos,angle):
        self.pos = pos
        self.angle = angle
