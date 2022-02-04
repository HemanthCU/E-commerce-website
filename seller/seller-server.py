#!/usr/bin/env python

from socket import * 
import threading

SERVERHOST = ''
SERVERPORT = 8898

def threadrunner(clientsock, addr):
    print(clientsock)
    print(addr)
	# while 1:
	# 	data = clientsock.recv(1024)
	# 	if not data:
    #         break
	# 	# Code to be written here
    #     cmd, data = data.split(' ', 1)
    #     if cmd in ['GET']:
            
    #     elif cmd in ['ADD']:
            
    #     elif cmd in ['UPDATE']:
            
    #     elif cmd in ['REMOVE']:
            
    #     elif cmd in ['GETSUCCESS']:
            
    #     elif cmd in ['ADDSUCCESS']:
            
    #     elif cmd in ['UPDATESUCCESS']:
            
    #     elif cmd in ['REMOVESUCCESS']:
    print("Server thread running")
    print(clientsock.recv(1024).decode())
    clientsock.send('Thank you for connecting'.encode())

if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind(('', SERVERPORT))
    tcpsocket.listen(5)

while 1:
	(clientsock, addr) = tcpsocket.accept()
	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()
    