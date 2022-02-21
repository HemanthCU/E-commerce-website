from ast import keyword
import socket
import threading
import sys

#from __future__ import print_function
import requests
import json
import time
import base64
import jsonpickle
import random
import requests
import json

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
        print("0000 - Create an account: sets up username and password")
        print("0001 - Login: provide username and password")
        print("0010 - Logout")
        print("0011 - Get seller rating")
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
        if val == '0000':
            inputstr = input(" enter username and password to Create Account")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/createAccount"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success")
            print(json.loads(response.text)['result'])
            print(response)
        if val == '0001':
            inputstr = input(" enter username and password to Log in")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/logIn"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success")
            print(json.loads(response.text)['result'])
            print(response)
        if val == '0010':
            url = addr + "/api/logOut"
            inputstr = input(" enter username  to Log out")
            values = {
                'inputstr' : inputstr
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success")
            print(json.loads(response.text)['result'])
            print(response)
        if val == '0011':
            url = addr + "/api/getSellerRating"
            inputstr = input(" enter username  to get seller rating")
            values = {
                'inputstr' : inputstr
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success")
            print(json.loads(response.text)['result'])
            print(response)
        if val=='0100':
            headers = {'content-type': 'application/json'}
            url = addr + "/api/addItem"
            #Put an item for sale
            #seller id, quantity
            inputstr = input("Enter your username, Item name, category, condition, sale price, quantity and key words with space: ")
            values = {
                'inputstr' : inputstr
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            
            #s.send((val + " "+keywords).encode())
            print("Checking whether success")
            #dict_data = json.loads(response.get_json())
            print(json.loads(response.text)['result'])
            print(response)
            #print (s.recv(1024).decode())#recv has to be a blocking call
        if val=='0101':
            headers = {'content-type': 'application/json'}
            url = addr + "/api/changeSalesPrice"
            #Change the sale price of an item
            ItemId_price = input("Enter username, item ID and new sale price: ")
            values = {
                'inputstr' : ItemId_price
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            #s.send((val+' '+ItemId_price).encode())
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)
            
            #print (s.recv(1024).decode())#recv has to be a blocking call
        if val=="0110":
            headers = {'content-type': 'application/json'}
            url = addr + "/api/removeItem"
            #Remove an item from sale
            ItemId_quantity = input("Enter username, item ID and quantity: ")
            values = {
                'inputstr' : ItemId_quantity
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print(json.loads(response.text)['result'])
            print(response)
            
        if val=="0111":
            headers = {'content-type': 'application/json'}
            url = addr + "/api/display"
            #Display items currently on sale put up by this seller
            seller_id = input("Enter username , seller id: ")
            values = {
                'inputstr' : seller_id
            }
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            #s.send((val+" "+seller_id).encode())
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)
            

port = 8807
host = '127.0.0.1'

addr = f"http://{host}:8807"


threadrunner(addr)