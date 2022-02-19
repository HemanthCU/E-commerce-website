from ast import keyword
import socket
import threading
import sys

from __future__ import print_function
import requests
import json
import time
import base64
import jsonpickle
import random

# Create an account: sets up username and password 0000
# Login: provide username and password 0001
# Logout 0010
# Get seller rating 0011 
# Put an item for sale: provide all item characteristics and quantity 0100
# Change the sale price of an item: provide item id and new sale price 0101
# Remove an item from sale: provide item id and quantity 0110
# Display items currently on sale put up by this seller 0111
# Exit 1111

#CMD ARG1 ARG2 ARG3 ARG4 ARG5

def threadrunner(addr):
    while 1:
        print("MENU")
        print("0100 - Put an item for sale")
        print("0101 - Change the sale price of an item")
        print("0111 - Display items currently on sale put up by this seller")
        print("0110 - Remove an item from sale")
        print("exit - Close the program")
        val = input("Enter your command: ")
        print("cmd "+val)
        if val== "exit":
            print("exiting")
            #s.send('1111'.encode())
            break
        if val=='0100':
            headers = {'content-type': 'application/json'}
            url = addr + "/api/put"
            #Put an item for sale
            #seller id, quantity
            inputstr = input("Enter your Item name, category, condition, sale price, quantity and key words with space: ")
            values = {
                'inputstr' : inputstr
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            
            #s.send((val + " "+keywords).encode())
            print("Checking whether success")
            #print (s.recv(1024).decode())#recv has to be a blocking call
        if val=='0101':
            headers = {'content-type': 'application/json'}
            url = addr + "/api/change"
            #Change the sale price of an item
            ItemId_price = input("Enter item ID and new sale price: ")
            values = {
                'inputstr' : ItemId_price
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            #s.send((val+' '+ItemId_price).encode())
            print("Checking whether success !!")
            #print (s.recv(1024).decode())#recv has to be a blocking call
        if val=="0110":
            headers = {'content-type': 'application/json'}
            url = addr + "/api/remove"
            #Remove an item from sale
            ItemId_quantity = input("Enter item ID and quantity: ")
            values = {
                'inputstr' : ItemId_quantity
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            #s.send((val+' '+ItemId_quantity).encode())
            #print("Checking whether success !!")
            #data = s.recv(1024).decode()
            #if not data.split(' ', 1) == 'GETFAILURE':
            #    print (data)#recv has to be a blocking call
        if val=="0111":
            headers = {'content-type': 'application/json'}
            url = addr + "/api/display"
            #Display items currently on sale put up by this seller
            seller_id = input("Enter seller id: ")
            values = {
                'inputstr' : seller_id
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            #s.send((val+" "+seller_id).encode())
            print("Checking whether success !!")
            #print (s.recv(1024).decode())#recv has to be a blocking call

port = 8807
host = '127.0.0.1'

addr = f"http://{host}:8807"
try:
    host_ip = socket.gethostbyname('127.0.0.1')
except socket.gaierror:
    print ("there was an error resolving the host")
    sys.exit()
while 1:
    val = input("Do you want to use buyer-client interface: ")
    if val=='yes':
    #threading.Thread(target = threadrunner, args = (host_ip, port,)).start()
        threadrunner(addr)
    elif val=='exit':
        break



