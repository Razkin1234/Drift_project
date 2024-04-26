import socket
import pickle
import traceback


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client.settimeout(4)  # Set timeout to 10 seconds (adjust as needed)
        self.server = "10.0.0.33"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send_car(self, data):
        """
         for sending the car info to the server
        :param data (the car we want to send):
        :return: all the other cars from the server in a list
        """
        try:
            to_send = f"kirmul~car_send~{pickle.dumps(data).decode('latin1')}"
            self.client.send(to_send.encode())
        except socket.error as e:
            traceback.print_exc()  # Print traceback for debugging
            print(e)

    def send_disconnect(self):
        try:
            to_send = f"kirmul~disconnect~cushvuthksntusani"
            self.client.send(to_send.encode())
        except socket.error as e:
            traceback.print_exc()  # Print traceback for debugging
            print(e)
    def send_item(self,item_data):
        #to_send = f"kirmul~item_send~type;{dict_inside['type']}>pos;{dict_inside['pos']}"
        if item_data.sprite_type == 'turtle':
            to_send = f"kirmul~item_send~type;{item_data.sprite_type}^pos;{item_data.rect.center}^angle;{item_data.angle}"
            self.client.send(to_send.encode())
        else:
            to_send = f"kirmul~item_send~type;{item_data.sprite_type}^pos;{item_data.rect.center}"
            self.client.send(to_send.encode())


    def get_info(self,display_surface,level):
        try:
            received = self.client.recv(2048).decode()
            received = received.split("*",1)  # Split at the first occurrence of "~"
            parts = received[0].split("~",1)  # Split at the first occurrence of "~"
            if parts[0] == 'kirmul':
                parts = parts[1].split("~",1)
                if parts[0] == 'car_send':  #for car location update
                    pickled_obj = parts[1].encode('latin1')
                    cars = pickle.loads(pickled_obj)
                    if cars != None: #for printing the cars
                        if len(cars) != 0:
                            if len(level.other_cars) != 0: #the number of cars on the players screen
                                for i,new_thing in enumerate(cars):
                                    in_list = False
                                    for j , thing in enumerate(level.other_cars):
                                        if thing.name == new_thing.name:
                                            level.other_cars[j] = new_thing #if the car is existed, update it
                                            in_list = True #if it is false at the end it will be added
                                    if not in_list:
                                        level.other_cars.append(new_thing)
                            else:
                                for new_car in cars:
                                    level.other_cars.append(new_car)
                elif parts[0] == 'item_send':
                    print(f"got item: {received[0]}")
                    parts = parts[1].split("^")  # name;{name}    ,  type;{dict_inside['type']}   ,     pos;{dict_inside['pos']}    ,    angle; the angle
                    if len(parts) <= 4:
                        item_info = parts[0].split(";", 1)
                        if item_info[0] == 'name':
                            item_name = item_info[1]  #for the dict update
                            if item_name in level.car.items: #if i already added the item
                                pass
                            else:
                                item_info = parts[1].split(";", 1)  # type   ,   the type
                                if item_info[0] == 'type':
                                    if item_info[1] == 'banana':  # for banana items
                                        item_info = parts[2].split(";", 1)  # pos    ,     the pos
                                        if item_info[0] == 'pos':
                                            level.car.create_banana(item_info[1]) #create a banana
                                            new_dict = {'type': 'banana', 'pos': item_info[1]}
                                            level.car.items[str(item_name)] = new_dict

                                    elif item_info[1] == 'turtle':
                                        pos = (2176, 1344) #just for warning, means nothing
                                        item_info = parts[2].split(";", 1)  # pos    ,     the pos
                                        if item_info[0] == 'pos':
                                            pos = item_info[1]
                                        item_info = parts[3].split(";", 1)  # pos    ,     the pos
                                        if item_info[0] == 'angle':
                                            new_dict = {'type': 'turtle' , 'pos': pos}
                                            level.car.items[str(item_name)] = new_dict
                                            level.car.create_turtle(pos,int(item_info[1])) #adding the item to the dict
                else:
                    print(received)
            else:
                print(received)





        except pickle.UnpicklingError as e:
            print("Error while unpickling:", e)
            traceback.print_exc()  # Print traceback for debugging
