#!/usr/bin/env python

from socket import * 
import threading
import sys

SERVERHOST = ''
SERVERPORT = 8807
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
seller_id = 1
unique_item_id = 1

sellerDB = {}

def threadrunner(clientsock, addr):
    print(clientsock)
    print(addr)
    
    #product DB connection
    productDB_port = 8886
    try:
     productDB_ip = socket.gethostbyname('127.0.0.1')
    except socket.gaierror:
     print ("there was an error resolving the host")
     sys.exit()
    try:
     productDB_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     print ("Socket is successfully created")
    except socket.error as err:
     print ("Socket creation is failed with error %s" %(err))
    productDB_socket.connect((productDB_ip, productDB_port))

    while 1:
        print('Waiting for user command')
        data = clientsock.recv(1024).decode()
        print(data)
        cmd,arg = data.split(' ',1)
        print(cmd)
        if cmd=='1111':
            break
        if cmd == '0100':
           #Put an item for sale:

           #preparing seller DB
           itemId = int(str(seller_id)+str(unique_item_id))
           if seller_id in sellerDB.keys():
              list = sellerDB[seller_id]
              list.append(itemId)
              sellerDB[seller_id] = list
           else:
              sellerDB[seller_id] = [itemId]
           seller_id += 1

           #preparing productDB 
           productDB_socket.send(('ADD '+arg).encode())
           clientsock.send(productDB_socket.recv(1024))
        if cmd=='0101':
			#Change the sale price of an item
            productDB_socket.send(('UPDATE '+arg).encode())
            clientsock.send(productDB_socket.recv(1024))
        if cmd=='0110':
			#Remove an item from sale
            productDB_socket.send(('REMOVE '+arg).encode())
            clientsock.send(productDB_socket.recv(1024))
            
            
        if cmd=='0111':
           # Display items currently on sale put up by this seller
           itemList = sellerDB[arg]
           resultItemList = ''
           for iid in itemList:
              productDB_socket.send(('GET '+iid).encode())
              resultItemList += productDB_socket.recv(1024).decode()+'\n'
           clientsock.send(resultItemList.encode())

           
          
          
if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind(('', SERVERPORT))
    tcpsocket.listen(5)


while 1:
	(clientsock, addr) = tcpsocket.accept()
	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()
    