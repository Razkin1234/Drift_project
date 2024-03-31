from support import *
#game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

#for all of the maps
MAPS = {
    '1':{'checkpoints_num': '9', 'floor': import_csv_layout('../maps/1/map1_floor.csv') ,'checkpoints' : import_csv_layout('../maps/1/map1_checkpoints.csv')}
}


#ui
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18