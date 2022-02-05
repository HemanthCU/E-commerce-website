from ast import keyword
import socket
import threading
import sys

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

def threadrunner(host_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("Socket is successfully created")
    except socket.error as err:
        print ("Socket creation is failed with error %s" %(err))
    s.connect((host_ip, port))
    print("Seller client is ready") 
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
            s.send('1111'.encode())
            break
        if val=='0100':
            #Put an item for sale
            #seller id, quantity
            keywords = input("Enter your Item name, category, condition, sale price, quantity and key words with space: ")
            s.send((val + " "+keywords).encode())
            print("Checking whether success")
            print (s.recv(1024).decode())#recv has to be a blocking call
        if val=='0101':
            #Change the sale price of an item
            ItemId_price = input("Enter item ID and new sale price: ")
            s.send((val+' '+ItemId_price).encode())
            print("Checking whether success !!")
            print (s.recv(1024).decode())#recv has to be a blocking call
        if val=="0110":
            #Remove an item from sale
            ItemId_quantity = input("Enter item ID and quantity: ")
            s.send((val+' '+ItemId_quantity).encode())
            print("Checking whether success !!")
            data = s.recv(1024).decode()
            if not data.split(' ', 1) == 'GETFAILURE':
                print (data)#recv has to be a blocking call
        if val=="0111":
            #Display items currently on sale put up by this seller
            seller_id = input("Enter seller id: ")
            s.send((val+" "+seller_id).encode())
            print("Checking whether success !!")
            print (s.recv(1024).decode())#recv has to be a blocking call

port = 8807
try:
    host_ip = socket.gethostbyname('127.0.0.1')
except socket.gaierror:
    print ("there was an error resolving the host")
    sys.exit()
while 1:
    val = input("Do you want to use buyer-client interface: ")
    if val=='yes':
    #threading.Thread(target = threadrunner, args = (host_ip, port,)).start()
        threadrunner(host_ip,port)
    elif val=='exit':
        break



