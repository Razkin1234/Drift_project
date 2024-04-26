import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            to_send = f"kirmul|car_send|{pickle.dumps(data).decode('latin1')}"
            self.client.send(to_send.encode())
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def work(self):
        data = b'Hello, server!'
        self.client.send(data)