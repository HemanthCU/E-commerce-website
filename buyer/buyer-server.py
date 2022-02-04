#!/usr/bin/env python

from socket import * 
import threading

SERVERHOST = ''
SERVERPORT = 8807
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
    shoppingCart = {}
    while 1:
        print('Waiting for user command')
        data = clientsock.recv(1024).decode()
        print(data)
        cmd = data.split(' ')
        print(cmd)
        if cmd[0]=='1111':
            break
        if cmd[0] == '0011':
           #search items for sale
           index = 1
           items = ''
           while(index<len(cmd)):
              items = items+'\n'
              index += 1
			  #fetch details from productDB
           clientsock.send(items.encode())
		   
        if cmd[0]=='0100':
			#add item to shopping cart
           if cmd[1] in shoppingCart.keys():
              shoppingCart[cmd[1]] = int(cmd[2])
           else:
              shoppingCart[cmd[1]] += int(cmd[2])
           clientsock.send("Successfully done ".encode())
        if cmd[0]=='0111':
			#Display shopping cart
            currentCart = ''
            for key in shoppingCart.keys():
               if shoppingCart[key]>0:
                  currentCart = currentCart +" item id : " +str(key)+", quantity: "+str(shoppingCart[key])+"\n"
            clientsock.send(currentCart.encode())
        if cmd[0]=='0101':
           # remove an item from cart
            if cmd[1] in shoppingCart.keys():
              shoppingCart[cmd[1]] -= int(cmd[2])
              clientsock.send("Successfully done ".encode()) 
        if cmd[0]=="0110":
			#clear the cart
            shoppingCart.clear()
            clientsock.send("Successfully done ".encode())
          
          
if __name__ == '__main__':
    tcpsocket = socket(AF_INET, SOCK_STREAM)
    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    tcpsocket.bind(('', SERVERPORT))
    tcpsocket.listen(5)

while 1:
	(clientsock, addr) = tcpsocket.accept()
	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()
    