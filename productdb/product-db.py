#!/usr/bin/env python

from socket import * 
import threading

SERVERHOST = ''
SERVERPORT = 8886

#Storage format: ID Quantity Name Category Condition Price Keyword1...

productdb = {}

def threadrunner(clientsock, addr):
    print(clientsock)
    print(addr)
    while 1:
        data = clientsock.recv(1024).decode()
        if data == 'CLOSE':
           break
        #Input format: CMD   Name, Category ID,  Condition, Price, Quantity,  Keyword1...
        cmd, data = data.split(' ', 1)
        #List of commands: GET(based on ID) ADD UPDATE REMOVE
        
        if cmd == 'GET':
            iid, data = data.split(' ', 1)
            if iid in productdb.keys():
                clientsock.send(productdb(iid).encode())
            else:
                clientsock.send("GETFAILURE  -  item does not exist".encode())     
               
        elif cmd == 'ADD':
            if iid not in productdb.keys():
              productdb[iid] = data
              clientsock.send("ADDSUCCESS".encode()) 
            else:
              clientsock.send("ADDFAILURE  - already exsisting item".encode())    
            
        elif cmd == 'UPDATE':
            iid, data = data.split(' ', 1)
            newprice = data
            if iid in productdb.keys():
                itemDetails = productdb[iid].split(' ')
                itemDetails[3] = newprice
                newDetails = ''
                for details in itemDetails:
                    newDetails += details+' '
                productdb[iid] = newDetails
                clientsock.send("UPDATE SUCCESS ".encode()) 
            else:
                clientsock.send("UPDATE FAILURE  -  item does not exist".encode())      
    
        elif cmd in ['REMOVE']:
            iid, data = data.split(' ', 1)
            remquant = int(data)
            if iid in productdb.keys():
                itemDetails = productdb[iid].split(' ')
                itemDetails[4] = str(int(itemDetails[4]) - remquant)
                newDetails = ''
                for details in itemDetails:
                    newDetails += details+' '
                productdb[iid] = newDetails
                clientsock.send("REMOVE SUCCESS ".encode()) 
            else:
                clientsock.send("REMOVE FAILURE  -  item does not exist".encode()) 
        #elif cmd in ['']:
        #TODO: Search based on keywords

if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind((SERVERHOST, SERVERPORT))
    tcpsocket.listen(5)

while 1:
	(clientsock, addr) = tcpsocket.accept()
	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()