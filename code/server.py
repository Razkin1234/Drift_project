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

s.listen(4)
print("Waiting for a connection, Server Started")

cars = {'0': {'object': Other_cars('1',(2176, 1344),180,'tank.png'),'round': 0 ,'played': False},
        '1': {'object': Other_cars('2',(2176, 1344),180,'taxi.png'),'round': 0 , 'played': False},
        '2': {'object': Other_cars('3',(2176, 1344),180,'batmobile.png'),'round': 0 , 'played': False},
        '3': {'object': Other_cars('4',(2176, 1344),180,'orange_car.png'),'round': 0 , 'played': False}} #all of the cars
#'type':   ,'pos':  ,'havesendto': (the players that got the item in an array),'angle'(for turtle type only):

#'example':{'type': 'turtle','pos': (1180,789,40,40),'angle': (1.12,-0.98) ,'havesendto':[1]}
items = {}

def threaded_client(conn, player):
    print('player: '+ str(player))
    conn.send(pickle.dumps(cars[str(player)]['object'])) #sending back the object
    cars[str(player)]['played'] = True #updating that there is a player for this car
    reply = ""
    item_num = 0 #for the items naming
    while True:
        c_items = items.copy()
        current_time = pygame.time.get_ticks()
        for item_name , item_dict in c_items.items():
            if current_time - item_dict['create_time'] >= 100:
                del items[item_name]


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
                    #type;{dict_inside['type']}^pos;{dict_inside['pos']}
                    parts = parts[1].split("^")             #type;{dict_inside['type']}   ,     pos;{dict_inside['pos']}    ,    angle; the angle
                    item_info = parts[0].split(";",1)         #type   ,   the type
                    if item_info[0] == 'type':
                        if item_info[1] == 'banana': #for banana items
                            print('got banana')
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
                    print(f'player {player} has disconnected')
                    break
        except pickle.UnpicklingError as e:
            print("Error while unpickling:", e)
            traceback.print_exc()  # Print traceback for debugging
            break

        try: #for the sending
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
                        print(f"sending {player}:  {to_send}")
                        conn.sendall(to_send.encode())

            ###cars update sending
            cars_to_send = []
            for name, dict_inside in cars.items():
                if dict_inside['played'] and player != int(name):
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




currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1