import pygame
import sys
from debug import debug
from  settings import *
from level import *
from network import Network

class Game:
    def __init__(self):
        #general setup
        pygame.init()
        self.network = Network() #the network
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption('Just Drift')
        self.clock = pygame.time.Clock()

        self.level = Level(self.network)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.network.send_disconnect()
                    pygame.quit()
                    sys.exit()

            try:
                start_new_thread(self.network.get_info, (self.screen, self.level))
            except:
                pass
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
