#!/usr/bin/env python

from socket import * 
import threading

SERVERHOST = ''
SERVERPORT = 8898
# Create an account: sets up username and password CMD 0000
# Login: provide username and password CMD 0001
# Logout CMD 0010
# Search items for sale: provide an item category and up to five keywords CMD 0011
# Add item to the shopping cart: provide item id and quantity CMD 0100
# Remove item from the shopping cart: provide item id and quantity CMD 0101
# Clear the shopping cart CMD 0110
# Display shopping cart CMD 0111
# Make purchase CMD 1000
# Provide feedback: thumbs up or down for each item purchased, at most one feedback per purchased item CMD 1001
# Get seller rating: provide buyer id CMD 1010
# Get buyer history CMD 1011
# Exit 1111
def threadrunner(clientsock, addr):
    print(clientsock)
    print(addr)
    while 1:
        data = clientsock.recv(1024).decode()
        cmd = data.split(' ')
        if cmd[0]=='1111':
            break
        if cmd[0]=='0011':
           
        if cmd[0]=='0100':
          
        if cmd[0]=="0101":
        
        if cmd[0]=="0110":
          
        if cmd[0]=="0111":
          
          
if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind(('', SERVERPORT))
    tcpsocket.listen(5)

while 1:
	(clientsock, addr) = tcpsocket.accept()
	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()
    