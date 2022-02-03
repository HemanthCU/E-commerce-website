#!/usr/bin/env python

from socket import * 
import thread

serverPort = 8886

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
            iquant = int(data)
        elif cmd in ['ADD']:
            iname, data = data.split(' ', 1)
            icat, data = data.split(' ', 1)
            iid, data = data.split(' ', 1)
            icond, data = data.split(' ', 1)
            iprice, data = data.split(' ', 1)
            iquant, data = data.split(' ', 1)
            iquant = int(iquant)
            klist = data.split()
        elif cmd in ['UPDATE']:
            iid, data = data.split(' ', 1)
            iprice = data
        elif cmd in ['REMOVE']:
            iid, data = data.split(' ', 1)
            iquant = int(data)
        #elif cmd in ['']:
        #TODO: Search based on keywords

if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind(('', serverPort))
    tcpsocket.listen(5)

while 1:
	(clientsock, addr) = tcpsocket.accept()
	thread.start_new_thread(threadrunner, (clientsock, addr))