import socket
from _thread import *
from other_cars import Other_cars
import pickle

server = "10.0.0.33"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


cars = [Other_cars('car_1',(2176, 1344),180,'tank.png'),Other_cars('car_1',(2176, 1344),180,'tank.png')] #all of the cars

def threaded_client(conn, player):
    conn.send(pickle.dumps(cars[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            cars[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = cars[0]
                else:
                    reply = cars[1]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1