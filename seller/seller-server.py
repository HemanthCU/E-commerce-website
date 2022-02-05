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

unique_item_id = 1
unique_seller_id = 1
sellerDB = {}

def threadrunner(clientsock, addr):
    global unique_item_id
    global unique_seller_id
    global sellerDB
    print(clientsock)
    print(addr)
    
    #product DB connection
    productDB_ip =  ''
    productDB_port = 8886
    try:
        productDB_socket = socket(AF_INET, SOCK_STREAM)
        print ("Socket is successfully created")
    except error as err:
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
        elif cmd == '0100':
            #Put an item for sale:

            #preparing seller DB
            itemId = str(unique_seller_id)+str(unique_item_id)
            if str(unique_seller_id) in sellerDB.keys():
                list1 = sellerDB[str(unique_seller_id)]
                list1.append(itemId)
                sellerDB[str(unique_seller_id)] = list1
            else:
                sellerDB[str(unique_seller_id)] = [itemId]
            #unique_seller_id = unique_seller_id + 1
            unique_item_id = unique_item_id + 1

           #preparing productDB 
            productDB_socket.send(('ADD '+itemId+' '+arg).encode())
            clientsock.send(productDB_socket.recv(1024))
        elif cmd=='0101':
			#Change the sale price of an item
            productDB_socket.send(('UPDATE '+arg).encode())
            clientsock.send(productDB_socket.recv(1024))
        elif cmd=='0110':
			#Remove an item from sale
            productDB_socket.send(('REMOVE '+arg).encode())
            clientsock.send(productDB_socket.recv(1024))
        elif cmd=='0111':
           # Display items currently on sale put up by this seller
            itemList = sellerDB[arg]
            resultItemList = ''
            for iid in itemList:
                productDB_socket.send(('GET '+iid).encode())
                res = productDB_socket.recv(1024).decode()
                if not res.split(' ')[0] in ['GETFAILURE']:
                    resultItemList += res +'\n'
            clientsock.send(resultItemList.encode())
        print(sellerDB)

if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind(('', SERVERPORT))
    tcpsocket.listen(5)


while 1:
	(clientsock, addr) = tcpsocket.accept()
	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()
    