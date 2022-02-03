#!/usr/bin/env python

from socket import * 
import thread

SERVERHOST = ''
SERVERPORT = 8886

#Storage format: ID Quantity Name Category Condition Price Keyword1...
productdb = []

def threadrunner(clientsock, addr):
	while 1:
		data = clientsock.recv(1024)
		if not data:
            break
        #Input format: CMD Name Category ID Condition Price Quantity Keyword1...
		cmd, data = data.split(' ', 1)
        #List of commands: GET(based on ID) ADD UPDATE REMOVE
        if cmd in ['GET']:
            iid, data = data.split(' ', 1)
            for item in productdb:
                if item[0] == iid:
                    retmsg = 'GETSUCCESS' + item[2] + ' ' + item[3] + ' ' + item[0] + ' ' + item[4] + ' ' + item[5] + ' ' + str(item[1])
                    for keyword in item[6]:
                        retmsg = retmsg + ' ' + keyword
                    clientsock.send(retmsg)
                    break
        elif cmd in ['ADD']:
            iname, data = data.split(' ', 1)
            icat, data = data.split(' ', 1)
            iid, data = data.split(' ', 1)
            icond, data = data.split(' ', 1)
            iprice, data = data.split(' ', 1)
            iquant, data = data.split(' ', 1)
            iquant = int(iquant)
            klist = data.split()
            productdb.append([iid, iquant, iname, icat, icond, iprice, klist])
            retmsg = 'ADDSUCCESS Item succesfully added to Product DB'
            clientsock.send(retmsg)
        elif cmd in ['UPDATE']:
            iid, data = data.split(' ', 1)
            newprice = data
            for item in productdb:
                if item[0] == iid:
                    item[5] = newprice
                    retmsg = 'UPDATESUCCESS Item price succesfully updated in Product DB'
                    clientsock.send(retmsg)
                    break
        elif cmd in ['REMOVE']:
            iid, data = data.split(' ', 1)
            remquant = int(data)
            for item in productdb:
                if item[0] == iid:
                    if item[1] > remquant:
                        item[1] = item[1] - remquant
                        retmsg = 'REMOVESUCCESS Item quantity succesfully updated in Product DB'
                    else:
                        productdb.remove(item)
                        retmsg = 'REMOVESUCCESS Item succesfully removed from Product DB'
                    clientsock.send(retmsg)
                    break
        #elif cmd in ['']:
        #TODO: Search based on keywords

if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind((SERVERHOST, SERVERPORT))
    tcpsocket.listen(5)

while 1:
	(clientsock, addr) = tcpsocket.accept()
	thread.start_new_thread(threadrunner, (clientsock, addr))