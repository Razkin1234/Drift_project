from support import *
#game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64

MAPS = {
    '1':{'checkpoints_num': '9', 'floor': import_csv_layout('../maps/1/map1.csv') ,'checkpoints' : import_csv_layout('../maps/1/map1_checkpoints.csv')}
}
