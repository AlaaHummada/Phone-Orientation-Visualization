#!/usr/bin/env python

from threading import Thread
import serial
import time
import struct
import numpy as np
import pandas as pd
import socket
import math

class SerialRead:
    def __init__(self):
        self.dataType = None
        self.isRun = True
        self.isReceiving = False
        self.thread = None
    def readSerialStart(self):
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)

    def getSerialData(self):
        UDP_IP = "192.168.136.155"  # set the IP address of the socket to listen on all interfaces
        UDP_PORT = 5555  # set the port number used by the UDP sensor streamer app

        # create a UDP socket and bind it to the specified IP address and port number
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))

        while True:
            message, address = sock.recvfrom(8192)

            print(message.decode())

            var1 = message.decode()
            print(var1)
            var2 = var1.split(',')
            
            try:
       
                ax= float(var2[0].strip(','))
                ay= float(var2[1].strip(','))
                az= float(var2[2].strip(','))  
                bx= float(var2[3].strip(','))
                by= float(var2[4].strip(','))
                bz= float(var2[5].strip(','))
                gx= float(var2[6].strip(','))
                gy= float(var2[7].strip(','))
                gz= float(var2[8].strip(','))  
                                            
                self.data = [gy,gx,-gz,ay,ax,-az,by,bx,-bz]
                
            except IndexError:
                # Handling the exception
                print("Index out of range!")
                
            
            
            # main program logic here
            try:
                pass
            except KeyboardInterrupt:
                # handle keyboard interrupt here
                sock.close()
                break
            return self.data

    def backgroundThread(self):    # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
     
        while (self.isRun):
            
            self.isReceiving = True
            #print(self.rawData)

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')
        # df = pd.DataFrame(self.csvData)
        # df.to_csv('/home/rikisenia/Desktop/data.csv')