import socket
import time
import _thread
import threading
from threading import Thread, Event


BLOCK_SIZE = 1024
PORT = 5005

class Connection :
    def __init__(self,IP):
        self.ip = IP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.e= Event()

    def get_myip(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 53))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def server(self):
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(("",PORT))
        print("wait")

        while True:
            data, addr = self.s.recvfrom(BLOCK_SIZE)
            data = data.decode('utf-8')
            print(data)
            if data == "DETECTED":
                self.e.set()
                print("Detected")

    def client(self):
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(self.s)

    def send(self,string):
        self.s.sendto(bytes(string, 'utf-8'),(self.ip, PORT))


    def threadServer(self):
        threading.Thread(target=self.server).start()
        threading.Thread(target=self.client).start()

def printAZER():
    while True :
        print("a")


if __name__ == "__main__":
    c=Connection("192.168.43.171")

    #c.threadServer()
    threading.Thread(target=c.server).start()
    #threading.Thread(target=c.client).start()
    #c.send("asl")
    a=0
    while True :
        print(a)
        a += 1
        time.sleep(0.1)
        if a ==100:
            c.send("DETECTED")
        if c.e.is_set():
            print('set')
            break
    #threading.Thread(target=c.client).start()
    
    #b = threading.Thread(target=printAZER).start()

    #b = _thread.start_new_thread(c.client)