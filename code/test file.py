import pygame
import sys
import math
from debug import debug

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Movement")

# Define colors
WHITE = (255, 255, 255)

# Load car image
car_image = pygame.image.load('../graphics/car.png').convert_alpha()  # replace 'car.png' with your car image file path
car_rect = car_image.get_rect()
car_rect.center = (screen_width // 2, screen_height // 2)

# Define Car class
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        print(self.angle)

    def move(self, speed):
        self.x += speed * math.cos(math.radians(self.angle+90))
        self.y -= speed * math.sin(math.radians(self.angle+90))

    def turn(self, angle_change):
        self.angle += angle_change
        if 0 <= self.angle >= 360:
            self.angle = self.angle % 360

# Main game loop
car = Car(screen_width // 2, screen_height // 2)
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle key presses for car movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.move(1)
    if keys[pygame.K_DOWN]:
        car.move(-1)
    if keys[pygame.K_LEFT]:
        car.turn(3)
    if keys[pygame.K_RIGHT]:
        car.turn(-3)

    # Rotate car image
    rotated_car = pygame.transform.rotate(car_image, car.angle)
    rotated_car_rect = rotated_car.get_rect(center=(car.x, car.y))

    # Draw rotated car on screen
    screen.blit(rotated_car, rotated_car_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
