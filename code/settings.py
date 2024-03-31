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

#for the map printing
ROW_LOAD_TILE_DISTANCE = 8  #8 is the good one
COL_LOAD_TILE_DISTANCE = 12  #12 is the good one
ROW_TILES = 22
COL_TILES = 30

#ui
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18