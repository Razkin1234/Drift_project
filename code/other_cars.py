import pygame

class Other_cars(pygame.sprite.Sprite):
    def __init__(self,name,pos,angle,car_skin):
        self.name = name
        self.car_skin = car_skin
        self.original_image = None #can load it only after pygame was on
        self.pos = pos #the position of the car
        self.angle = angle #the angle of the car

    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self.name}, pos={self.pos}, angle={self.angle}, car_skin={self.car_skin})>"

    def load_image(self):
        self.original_image = pygame.image.load(f'../graphics/cars/{self.car_skin}').convert_alpha() #the car image

    def update_own_data(self,pos,angle):
        self.pos = pos
        self.angle = angle

    def blit_other_car(self, rect , screen):

        self.original_image = pygame.image.load(f'../graphics/cars/{self.car_skin}').convert_alpha()  # the car image
        # Rotate the original image based on the angle
        rotated_image = pygame.transform.rotate(self.original_image,
                                                self.angle)  # that the car will start facing its angle
        # Get the rect of the rotated image
        car_rect = rotated_image.get_rect(topleft=self.pos[:2])


        offset = pygame.math.Vector2()
        # getting the offset
        offset.x = rect.centerx - screen.get_size()[0] // 2
        offset.y = rect.centery - screen.get_size()[1] // 2

        # for sprite in self.sprites():
        # if sprite is not car:
        # 	offset_pos = sprite.rect.topleft - self.offset
        # 	self.display_surface.blit(sprite.image,offset_pos)
        offset_pos = car_rect.topleft - offset
        screen.blit(rotated_image, offset_pos)


    def blit_try(self,screen):
        # the box
        bg_rect = pygame.Rect(self.pos[0], self.pos[1], 64, 32)
        pygame.draw.rect(screen, 'blue', bg_rect)
        pygame.draw.rect(screen, 'yellow', bg_rect, 3)
        bg_rect = pygame.Rect(1000, 620, 80, 80)
        pygame.draw.rect(screen, 'blue', bg_rect)
        pygame.draw.rect(screen, 'yellow', bg_rect, 3)
