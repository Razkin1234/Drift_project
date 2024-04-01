from support import *
#game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

#for all of the maps
MAPS = {
    '1': {'checkpoints_num': '9', 'floor': import_csv_layout('../maps/2/map1_floor.csv') ,'checkpoints' : import_csv_layout('../maps/2/map1_checkpoints.csv') , 'lap_num': '8'}
}

#for the map printing
ROW_LOAD_TILE_DISTANCE = 8  #8 is the good one
COL_LOAD_TILE_DISTANCE = 12  #12 is the good one
ROW_TILES = 38
COL_TILES = 46

#ui
UI_FONT = '../graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
ITEM_BOX_SIZE = 80


#items:
item_data = {
	'box' : {'graphic' : '../graphics/items/box64.png'},
	'banana' : {'graphic': '../graphics/items/banana.png' },
	'turtle': {'graphic': '../graphics/items/turtle.png'}
}

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'