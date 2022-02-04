#!/usr/bin/env python

from socket import * 
import threading

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

unique_item_id = 1
unique_seller_id = 1
sellerDB = {}

def threadrunner(clientsock, addr):
    print(clientsock)
    print(addr)
    while 1:
        print('Waiting for user command')
        data = clientsock.recv(1024).decode()
        print(data)
        cmd = data.split(' ')
        print(cmd)
        if cmd[0]=='1111':
            break
        if cmd[0] == '0100':
           #Put an item for sale:

           #preparing seller DB
           itemId = int(str(unique_seller_id)+str(unique_item_id))
           if unique_seller_id in sellerDB.keys():
              list = sellerDB[unique_seller_id]
              list.append(itemId)
              sellerDB[unique_seller_id] = itemId
           else:
               list = []
               list.append(itemId)
               sellerDB[unique_seller_id] = list

           #preparing productDB
           

           
		   
        if cmd[0]=='0101':
			#Change the sale price of an item
           
        if cmd[0]=='0110':
			#Remove an item from sale
            
        if cmd[0]=='0111':
           # Display items currently on sale put up by this seller
        
          
          
if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind(('', SERVERPORT))
    tcpsocket.listen(5)


while 1:
	(clientsock, addr) = tcpsocket.accept()
	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()
    