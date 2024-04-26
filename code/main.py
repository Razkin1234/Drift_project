import pygame
import sys
from debug import debug
from  settings import *
from level import *
from network import Network
from button import *

class Game:
    def __init__(self):
        #general setup
        pygame.init()
        self.network = None #the network
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        self.transparent_surface = pygame.Surface((WIDTH,HEIGTH),pygame.SRCALPHA )
        pygame.display.set_caption('Just Drift')
        self.clock = pygame.time.Clock()

        self.level = None
        self.car_skin = 'formula_pink.png'
        self.skins_list = ['formula_pink.png', 'formula_flames.png', 'blackstripes_car.png', 'batmobile.png',
                      'army_track.png', 'orange_formula.png', 'orange_car.png', 'matteblack_car.png', 'green_car.png',
                      'formula_red.png', 'redstripes_car.png', 'red_car.png', 'purplestripes_car.png', 'police.png',
                      'pink_track.png', 'white_track.png', 'white_car.png', 'usa_car.png', 'taxi.png', 'tank.png']

    def get_font(self,size):  # Returns Press-Start-2P in the desired size
        return pygame.font.Font("../graphics/font/joystix.ttf", size)
    def main_menu(self):
        not_to_the_game = True
        backround = pygame.image.load("../graphics/manu/backround.png")
        while not_to_the_game:
            self.screen.blit(backround, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 50))

            PLAY_BUTTON = Button(image=pygame.image.load("../graphics/manu/Play Rect.png"), pos=(200, 180),
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("../graphics/manu/Options Rect.png"), pos=(306, 300),
                                    text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("../graphics/manu/Quit Rect.png"), pos=(190, 420),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        not_to_the_game = False
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.skin_screen()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def skin_screen(self):
        not_to_the_manu = True
        backround = pygame.image.load("../graphics/manu/skinbackround.png")
        while not_to_the_manu:
            self.screen.blit(backround, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("CHOOSE SKIN", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 50))


            BACK_BUTTON = Button(image=pygame.image.load("../graphics/manu/Quit Rect.png"), pos=(1075, 650),
                                 text_input="BACK", font=self.get_font(75), base_color="#d7fcd4",
                                 hovering_color="White")

            b_list = []

            for i in range(10):
                i = my_button(image=pygame.image.load(f"../graphics/cars/{self.skins_list[i]}"), pos=(300 + 75*i, 250),
                                     text_input="", font=self.get_font(75), base_color="#d7fcd4",
                                     hovering_color="White", surface= self.transparent_surface)
                b_list.append(i)
            for i in range(10):
                i = my_button(image=pygame.image.load(f"../graphics/cars/{self.skins_list[i+10]}"), pos=(300 + 75*i, 400),
                                     text_input="", font=self.get_font(75), base_color="#d7fcd4",
                                     hovering_color="White", surface= self.transparent_surface)
                b_list.append(i)


            b_list.append(BACK_BUTTON)
            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in b_list:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        not_to_the_manu = False


            pygame.display.update()


        self.main_menu()


    def run(self):
        self.main_menu() #for the main menu

        self.network = Network()
        self.level = Level(self.network,self.car_skin)
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
