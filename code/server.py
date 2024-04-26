import socket
from _thread import *
from other_cars import Other_cars
from YsortCameraGroup import *
import pickle
import traceback

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
#'type':   ,'pos':  ,'vector'(for turtle type only):  ,'havesendto': (the players that got the item in an array)
items = {}

def threaded_client(conn, player):
    print('player: '+ str(player))
    conn.send(pickle.dumps(cars[str(player)]['object'])) #sending back the object
    cars[str(player)]['played'] = True #updating that there is a player for this car
    reply = ""
    item_num = 0 #for the items naming
    while True:
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
                        reply = []
                        for name , dict_inside in cars.items():
                            if dict_inside['played'] and player != int(name):
                                reply.append(dict_inside['object'])

                        print("Received: ", str(data))
                        print("Sending : ", str(reply))

                    conn.sendall(pickle.dumps(reply))
                elif parts[0] == 'item_send':
                    pickled_obj = parts[1].encode('latin1')
                    data = pickle.loads(pickled_obj)
                    if data.item_type == 'banana':
                        new_dict = {'type': 'banana','pos': data.rect,'havesendto':[player]}
                        items[f"player{player}n{item_num}"] = new_dict
                        item_num += 1
                elif parts[0] == 'disconnect':
                    cars[str(player)]['played'] = False
                    print(f'player {player} has disconnected')
                    break
        except pickle.UnpicklingError as e:
            print("Error while unpickling:", e)
            traceback.print_exc()  # Print traceback for debugging
            break

        # try: #for the items update
        #     for item_name , dict_item in items.items():
        #         if player not in dict_item['havesendto']:





    print(f"Lost connection with {player}")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1