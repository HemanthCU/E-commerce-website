#!/usr/bin/env python

from socket import * 
import thread

serverPort = 8888

def threadrunner(clientsock, addr):
	while 1:
		data = clientsock.recv(1024)
		if not data: break
		# Code to be written here

if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind(('', serverPort))
    tcpsocket.listen(5)

while 1:
	(clientsock, addr) = tcpsocket.accept()
	thread.start_new_thread(threadrunner, (clientsock, addr))