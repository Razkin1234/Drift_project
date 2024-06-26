import socket
from _thread import *
from other_cars import Other_cars
from YsortCameraGroup import *
import pickle
import traceback
from pygame import time

server = "10.0.0.33"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

cars = {'0': {'object': Other_cars('1',(2170, 1344),180,'tank.png'),'round': 0 ,'played': False , 'lap': 0 , 'time': 0, 'name': 'player_1', 'gap': 0,'left': False},
        '1': {'object': Other_cars('2',(2120, 1344),180,'taxi.png'),'round': 0 , 'played': False, 'lap': 0 , 'time': 0, 'name': 'player_2', 'gap': 0,'left': False},
        '2': {'object': Other_cars('3',(2070, 1344),180,'batmobile.png'),'round': 0 , 'played': False, 'lap': 0 , 'time': 0, 'name': 'player_3', 'gap': 0,'left': False},
        '3': {'object': Other_cars('4',(2020, 1344),180,'orange_car.png'),'round': 0 , 'played': False, 'lap': 0 , 'time': 0, 'name': 'player_4', 'gap': 0,'left': False}} #all of the cars


#'type':   ,'pos':  ,'havesendto': (the players that got the item in an array),'angle'(for turtle type only):

#'example':{'type': 'turtle','pos': (1180,789,40,40),'angle': (1.12,-0.98) ,'havesendto':[1],'create_time': pygame.time.getticks()}
items = {}
delete_items = {}
start_send = {}
lap_send = {}



boxes = {   '1': {'location': (1872, 730) , 'is_on': True , 'time_off': 0.0},
			'2': {'location': (1872, 782), 'is_on': True, 'time_off': 0.0},
			'3': {'location': (1872, 834), 'is_on': True, 'time_off': 0.0},
			'4': {'location': (1872, 886), 'is_on': True, 'time_off': 0.0},
			'5': {'location': (1050, 1222), 'is_on': True, 'time_off': 0.0},
			'6': {'location': (1095, 1222), 'is_on': True, 'time_off': 0.0},
			'7': {'location': (1518, 1178), 'is_on': True, 'time_off': 0.0},
			'8': {'location': (1518, 1223), 'is_on': True, 'time_off': 0.0},}

def threaded_client(conn, player):
    print('player: '+ str(player))
    #conn.send(pickle.dumps(cars[str(player)]['object'])) #sending back the object

    to_send = f"kirmul~{player}~{pickle.dumps(cars[str(player)]['object']).decode('latin1')}"
    conn.send(to_send.encode())  # the car send


    cars[str(player)]['played'] = True #updating that there is a player for this car
    reply = ""
    item_num = 0 #for the items naming
    while True:

        current_time = pygame.time.get_ticks()#the current time
        c_items = items.copy()
        if len(start_send) > 0:
            if current_time - start_send['time'] >= 100 and start_send['send']:
                start_send['send'] = False

        if len(lap_send) > 0:
            if current_time - lap_send['time'] >= 100 and lap_send['send']:
                lap_send['send'] = False

        for item_name , item_dict in c_items.items():
            if current_time - item_dict['create_time'] >= 100:
                del items[item_name]
        c_items = delete_items.copy()
        for item_name , item_dict in c_items.items():
            if current_time - item_dict['create_time'] >= 100:
                del delete_items[item_name]
        for box_name, box_dict in boxes.items():
            if box_dict['is_on'] == False:
                if current_time - box_dict['time_off'] >= box_retime:
                    box_dict['is_on'] = True
                    new_dict = {'type': 'box','pos':box_dict['location'],'havesendto': [],'create_time': pygame.time.get_ticks()}
                    items[box_name] = new_dict


        try:
            received = conn.recv(2048).decode()
            parts = received.split("~",1)  # Split at the first occurrence of "-"
            if parts[0] == 'kirmul':
                parts = parts[1].split("~",1)

                #the data:
                if parts[0] == 'car_send': #for car location update
                    pickled_obj = parts[1].encode('latin1')
                    data = pickle.loads(pickled_obj)

                    cars[str(player)]['object'] = data

                    if not data:
                        print("Disconnected")
                        break
                    else:
                         #print("Received: ", str(data))
                        pass
                elif parts[0] == 'item_send':
                    #print(parts[1])
                    #type;{dict_inside['type']}^pos;{dict_inside['pos']}
                    parts = parts[1].split("^")             #type;{dict_inside['type']}   ,     pos;{dict_inside['pos']}    ,    angle; the angle
                    item_info = parts[0].split(";",1)         #type   ,   the type
                    if item_info[0] == 'type':
                        if item_info[1] == 'banana': #for banana items
                            item_info = parts[1].split(";",1)             #pos    ,     the pos
                            if item_info[0] == 'pos':
                                new_dict = {'type': 'banana','pos': item_info[1],'havesendto':[player], 'create_time': pygame.time.get_ticks()}
                                items[f'p{player}i{item_num}'] = new_dict
                        elif item_info[1] == 'turtle':
                            item_info = parts[1].split(";", 1)  # pos    ,     the pos
                            if item_info[0] == 'pos':
                                pos = item_info[1]
                            item_info = parts[2].split(";", 1)  # pos    ,     the pos
                            if item_info[0] == 'angle':
                                new_dict = {'type': 'turtle', 'pos': pos,'angle': item_info[1] , 'havesendto': [player] , 'create_time': pygame.time.get_ticks()}
                                items[f'p{player}i{item_num}'] = new_dict
                    item_num +=1 #for the names on the dict

                elif parts[0] == 'disconnect':
                    cars[str(player)]['played'] = False
                    cars[str(player)]['left'] = True
                    print(f'player {player} has disconnected')
                    no_one = True
                    for key , dict in cars.items():
                        if dict['played']:
                            no_one = False
                    if no_one:
                        restart()

                    break
                elif parts[0] == 'item_delete':    #"kirmul~item_delete~name;{item_name}"
                    item_info = parts[1].split(';')
                    name = item_info[1]
                    if name in items:#removing the item
                        del items[name]
                    new_dict = {'create_time': pygame.time.get_ticks(),'havesendto':[player]}
                    delete_items[name] = new_dict

                elif parts[0] == 'box_delete':    #"kirmul~box_delete~name;{box_name}"
                    item_info = parts[1].split(';')
                    name = item_info[1]
                    if name in boxes:#removing the item
                        boxes[name]['is_on'] = False
                        boxes[name]['time_off'] = pygame.time.get_ticks()
                        new_dict = {'create_time': pygame.time.get_ticks(), 'havesendto': [player]}
                        delete_items[name] = new_dict
                elif parts[0] == 'game_start': #game_start~bullshit;gimel
                    start_send['send'] = True
                    start_send['time'] = pygame.time.get_ticks()

                elif parts[0] == 'lap_update': #lap_update~lap;{lap}^time;{time}
                    parts = parts[1].split('^')
                    item_info = parts[0].split(';')
                    if item_info[0] == 'lap':
                        cars[str(player)]['lap'] = int(item_info[1])
                        item_info = parts[1].split(';')
                        if item_info[0] == 'time':
                            cars[str(player)]['time'] = int(item_info[1])
                            cars[str(player)]['gap'] = item_info[1]
                            lap_send['send'] = True
                            lap_send['time'] = pygame.time.get_ticks()


        except pickle.UnpicklingError as e:
            print("Error while unpickling:", e)
            traceback.print_exc()  # Print traceback for debugging
            break

        try: #for the sending
            #start sending
            if len(start_send) > 0:
                if start_send['send']:
                    number_of_players = 0
                    for name , dict_info in cars.items():
                        if dict_info['played']:
                            number_of_players += 1

                    to_send = f"kirmul~game_start~players_num;{number_of_players}*nothing"
                    conn.sendall(to_send.encode())

            #lap update sending   [{'name':'player_1','time': 20549, 'lap':0},{'name':'player_2','time': 21579, 'lap':0},{'name':'player_3','time': 24549, 'lap':0}]
            if len(lap_send) > 0:
                if lap_send['send']:
                    list = []
                    for name , dict_info in cars.items():
                        if dict_info['played'] or dict_info['left']:
                            new_dict = {'name': dict_info['name'],'time': dict_info['time'], 'lap':dict_info['lap']}
                            list.append(new_dict)
                    list = sorted(list, key=lambda x: (-x['lap'], x['time']))
                    print(f'lap_send: {list}')
                    to_send = f"kirmul~lap_update~{pickle.dumps(list).decode('latin1')}*nothing"
                    conn.sendall(to_send.encode())



            ###item sending
            #new_dict = {'type': 'banana','pos': data.rect,'havesendto':[player]}
            c_items = items.copy()
            for name , dict_inside in c_items.items():
                if player not in dict_inside['havesendto']:
                    if dict_inside['type'] == 'banana':
                        to_send = f"kirmul~item_send~name;{name}^type;{dict_inside['type']}^pos;{dict_inside['pos']}*nothing"
                        conn.sendall(to_send.encode())
                    elif dict_inside['type'] == 'turtle':
                        to_send = f"kirmul~item_send~name;{name}^type;{dict_inside['type']}^pos;{dict_inside['pos']}^angle;{dict_inside['angle']}*nothing"
                        conn.sendall(to_send.encode())
                    elif dict_inside['type'] == 'box':
                        to_send = f"kirmul~item_send~name;{name}^type;box^pos;{dict_inside['pos']}*nothing"
                        conn.sendall(to_send.encode())

            #to delete items:
            c_items = delete_items.copy()
            for name, dict_inside in c_items.items():
                if player not in dict_inside['havesendto']:
                    to_send = f"kirmul~delete_item~name;{name}*nothing"
                    conn.sendall(to_send.encode())  # the car send

            ###cars update sending
            cars_to_send = []
            for key, dict_inside in cars.items():
                if dict_inside['played'] and player != int(key):
                    cars_to_send.append(dict_inside['object'])
            # print(f"Sending {player}: ", str(cars_to_send))
            to_send = f"kirmul~car_send~{pickle.dumps(cars_to_send).decode('latin1')}*nothing"
            conn.sendall(to_send.encode())  # the car send


        except pickle.UnpicklingError as e:
            print("Error while unpickling:", e)
            traceback.print_exc()  # Print traceback for debugging
            break

    print(f"Lost connection with {player}")
    conn.close()


def restart():
    global cars, boxes, items, delete_items, start_send, lap_send , currentPlayer
    currentPlayer = 0
    cars = MAPS['1']['cars']
    boxes = MAPS['1']['boxes']
    items ={}
    delete_items = {}
    start_send = {}
    lap_send = {}




currentPlayer = 0
while True:
    print(f'start_send: {start_send}')
    conn, addr = s.accept()
    if len(start_send) == 0:
        if currentPlayer < 4:
            print("Connected to:", addr)
            start_new_thread(threaded_client, (conn, currentPlayer))
            currentPlayer += 1
        else:
            conn.close()
    else:
        conn.close()