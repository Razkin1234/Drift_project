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
        self.ip = ''

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

            PLAY_BUTTON = Button(image=pygame.image.load("../graphics/manu/Quit Rect.png"), pos=(200, 180),
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("../graphics/manu/Quit Rect.png"), pos=(200, 300),
                                    text_input="SKINS", font=self.get_font(75), base_color="#d7fcd4",
                                    hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("../graphics/manu/Quit Rect.png"), pos=(200, 420),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS,self.screen)
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
            for i in range(10,20):
                i = my_button(image=pygame.image.load(f"../graphics/cars/{self.skins_list[i]}"), pos=(300 + 75*(i-10), 400),
                                     text_input="", font=self.get_font(75), base_color="#d7fcd4",
                                     hovering_color="White", surface= self.transparent_surface)
                b_list.append(i)


            self.screen.blit(MENU_TEXT, MENU_RECT)

            skin_text = self.get_font(50).render("Your Skin:", True, "#b68f40")
            skin_text_rect = MENU_TEXT.get_rect(center=(500, 675))
            self.screen.blit(skin_text,skin_text_rect)
            #for your car skin
            self.transparent_surface.fill((0, 0, 0, 0))

            image = pygame.image.load(f"../graphics/cars/{self.car_skin}")
            new_rect = image.get_rect(center= (490,645))
            big_rect = pygame.Rect(new_rect.x, new_rect.y, new_rect[2] + 20, new_rect[3] + 20)
            big_rect.center = new_rect.center

            pygame.draw.rect(self.transparent_surface, (200, 150, 100, 200), big_rect)
            pygame.draw.rect(self.transparent_surface, (100, 100, 100, 200), big_rect, 3)

            self.screen.blit(self.transparent_surface, (0, 0))
            self.screen.blit(image, new_rect)



            a_list = b_list.copy()
            a_list.append(BACK_BUTTON)
            for button in a_list:
                button.changeColor(MENU_MOUSE_POS,self.screen)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        not_to_the_manu = False
                    else:
                        for index , button in enumerate(b_list):
                            if button.checkForInput(MENU_MOUSE_POS):
                                self.car_skin = self.skins_list[index]



            pygame.display.update()


        self.main_menu()

    def ip_screen(self):
        ip_text = "10.0.0.33"

        not_to_play = True
        backround = pygame.image.load("../graphics/manu/skinbackround.png")
        while not_to_play:
            self.screen.blit(backround, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.get_font(100).render("INSERT IP", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 50))
            self.screen.blit(MENU_TEXT, MENU_RECT)

            BACK_BUTTON = Button(image=pygame.image.load("../graphics/manu/Quit Rect.png"), pos=(1075, 650),
                                 text_input="BACK", font=self.get_font(75), base_color="#d7fcd4",
                                 hovering_color="White")

            PLAY_BUTTON = Button(image=pygame.image.load("../graphics/manu/go_play.png"), pos=(880, 376),
                                 text_input="PLAY", font=self.get_font(40), base_color="#d7fcd4",
                                 hovering_color="White")


            user_text = self.get_font(24).render(ip_text, True, "gold")
            user_text_rect = MENU_TEXT.get_rect(topleft=(540, 360))
            box_rect = pygame.rect.Rect(536,356,275,40)
            pygame.draw.rect(self.screen,(100, 100, 100),box_rect)
            pygame.draw.rect(self.screen, (70, 70, 70), box_rect,3)
            self.screen.blit(user_text, user_text_rect)

            user_text = self.get_font(40).render('The IP:', True, "#b68f40")
            user_text_rect = MENU_TEXT.get_rect(topleft=(300, 350))
            self.screen.blit(user_text, user_text_rect)


            a_list = []
            a_list.append(BACK_BUTTON)
            a_list.append(PLAY_BUTTON)
            for button in a_list:
                button.changeColor(MENU_MOUSE_POS,self.screen)
                button.update(self.screen)

            pygame.display.flip()  # Update the display

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.main_menu()
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.ip = ip_text
                        not_to_play = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        ip_text = ip_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.ip = ip_text
                        not_to_play = False
                    else:
                        ip_text += event.unicode




    def run(self):
        self.main_menu() #for the main menu

        self.ip_screen()
        self.network = Network(self.ip)
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
