from support import *
from other_cars import Other_cars
#game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

#for all of the maps
MAPS = {
    '1': {'checkpoints_num': '9', 'floor': import_csv_layout('../maps/2/map1_floor.csv') ,'checkpoints' : import_csv_layout('../maps/2/map1_checkpoints.csv') , 'lap_num': '4',
		  'boxes':{
		    '1': {'location': (1872, 730) , 'is_on': False , 'time_off': 0.0},
			'2': {'location': (1872, 782), 'is_on': False, 'time_off': 0.0},
			'3': {'location': (1872, 834), 'is_on': False, 'time_off': 0.0},
			'4': {'location': (1872, 886), 'is_on': False, 'time_off': 0.0},
			'5': {'location': (1050, 1222), 'is_on': False, 'time_off': 0.0},
			'6': {'location': (1095, 1222), 'is_on': False, 'time_off': 0.0},
			'7': {'location': (1518, 1178), 'is_on': False, 'time_off': 0.0},
			'8': {'location': (1518, 1223), 'is_on': False, 'time_off': 0.0},},
		  'cars' : {
		'0': {'object': Other_cars('1', (2170, 1344), 180, 'tank.png'), 'round': 0, 'played': False, 'lap': 0, 'time': 0,
			  'name': 'player_1', 'gap': 0, 'left': False},
		'1': {'object': Other_cars('2', (2120, 1344), 180, 'taxi.png'), 'round': 0, 'played': False, 'lap': 0, 'time': 0,
			  'name': 'player_2', 'gap': 0, 'left': False},
		'2': {'object': Other_cars('3', (2070, 1344), 180, 'batmobile.png'), 'round': 0, 'played': False, 'lap': 0,
			  'time': 0, 'name': 'player_3', 'gap': 0, 'left': False},
		'3': {'object': Other_cars('4', (2020, 1344), 180, 'orange_car.png'), 'round': 0, 'played': False, 'lap': 0,
			  'time': 0, 'name': 'player_4', 'gap': 0, 'left': False}}
}

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
item_list = ["banana", "turtle"]

item_data = {
	'box' : {'graphic' : '../graphics/items/box32.png'},
	'banana' : {'graphic': '../graphics/items/banana.png','icon':'../graphics/items/banana_icon.png' },
	'turtle': {'graphic': '../graphics/items/turtle.png', 'icon':'../graphics/items/turtle_icon.png'}
}


box_retime = 10000

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'