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

cars = {'0': {'object': Other_cars('1',(2176, 1344),180,'tank.png'), 'played': False},
        '1': {'object': Other_cars('2',(2176, 1344),180,'taxi.png'), 'played': False},
        '2': {'object': Other_cars('3',(2176, 1344),180,'batmobile.png'), 'played': False},
        '3': {'object': Other_cars('4',(2176, 1344),180,'orange_car.png'), 'played': False}} #all of the cars

def threaded_client(conn, player):
    print('player: '+ str(player))
    conn.send(pickle.dumps(cars[str(player)]['object'])) #sending back the object
    cars[str(player)]['played'] = True #updating that there is a player for this car
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
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
        except pickle.UnpicklingError as e:
            print("Error while unpickling:", e)
            #traceback.print_exc()  # Print traceback for debugging
            break


    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1