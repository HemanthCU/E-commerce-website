#!/usr/bin/env python

from socket import * 
import threading
import sys
from unicodedata import category
import grpc
import sys
sys.path.append('../')
import backend_pb2
import backend_pb2_grpc

host1 = '127.0.0.1'+':50052'
channel = grpc.insecure_channel(host1)
stub = backend_pb2_grpc.backendApiStub(channel)
SERVERHOST = ''
SERVERPORT = 8808
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

shoppingCart = {}

# Search items for sale: provide an item category and up to five keywords CMD 0011
@app.route('/api/searchItems', methods=['POST'])
def searchItems():
    r = request
    global stub
    json_data = r.get_json()
    index = 1
    keywords = json_data['inputstr'].split(' ')
    category = keywords[0]
    finalItems = ''
    while(index<len(keywords)):
        responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = "GETIIDS "+keywords[index]))
        itemIDList = responseFromDB.output
        print(itemIDList)
        itemList = itemIDList.split(' ')
        for itemID in itemList:
            itemDetails = stub.sendProductDB(backend_pb2.inputMsg(input = "GET "+itemID))
            if not itemDetails.output.split(' ')[0] in ['GETFAILURE']:
                print(itemDetails)
                itemDetailstTuple = itemDetails.split(' ')
                if itemDetailstTuple[2] in [category] and int(itemDetailstTuple[5])>0:
                    finalItems += itemDetailstTuple[0]+' '+itemDetailstTuple[1]+' '+itemDetailstTuple[2]+' '+itemDetailstTuple[3]+' '+itemDetailstTuple[4]+' '+itemDetailstTuple[5]+'\n'
        index += 1
    response = {
        'result': responseFromDB.output
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Add item to the shopping cart: provide item id and quantity CMD 0100
@app.route('/api/addItem', methods=['POST'])
def addItem():
    r = request
    global stub
    global shoppingCart
    json_data = r.get_json()
    itemDetails = json_data['inputstr'].split(' ')
    responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = "GET "+itemDetails[0]))
    itemDBDetails = responseFromDB.output
    if itemDBDetails.split(' ')[0] in ['GETFAILURE']:
        respstr = "Item is not available currently"
    else:
        respstr = "Item added successfully"
        if itemDetails[0] in shoppingCart.keys():
            shoppingCart[itemDetails[0]] = str(int(shoppingCart[itemDetails[0]]) + int(itemDetails[1]))
        else:
            shoppingCart[itemDetails[0]] = itemDetails[1]
    response = {
        'result': respstr
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Remove item from the shopping cart: provide item id and quantity CMD 0101
@app.route('/api/removeItem', methods=['POST'])
def removeItem():
    r = request
    global stub
    global shoppingCart
    json_data = r.get_json()
    itemDetails = json_data['inputstr'].split(' ')
    if itemDetails[0] in shoppingCart.keys():
        shoppingCart[itemDetails[0]] = str(int(shoppingCart[itemDetails[0]]) - int(itemDetails[1]))
        if int(shoppingCart[itemDetails[0]])<=0:
            shoppingCart.pop(itemDetails[0])
        respstr = "Successfully done "
    else:
        respstr = "Item doesn't exist "
    response = {
        'result': respstr
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Display shopping cart CMD 0111
@app.route('/api/displayCart', methods=['POST'])
def displayCart():
    r = request
    global stub
    global shoppingCart
    json_data = r.get_json()
    dummy = json_data['inputstr']
    currentCart = ''
    for key in shoppingCart.keys():
        if int(shoppingCart[key])>0:
            currentCart = currentCart +" item id : " +str(key)+", quantity: "+str(shoppingCart[key])+"\n"
    if currentCart == '':
        currentCart = 'CART EMPTY'
    response = {
        'result': currentCart
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/clearCart', methods=['POST'])
def clearCart():
    r = request
    global stub
    global shoppingCart
    json_data = r.get_json()
    dummy = json_data['inputstr']
    shoppingCart.clear()
    response = {
        'result': "Successfully cleared cart"
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

def threadrunner(clientsock, addr):
    global stub
    print(clientsock)
    print(addr)
    #product DB connection
    productDB_port = 8886
    try:
        productDB_ip = ''
    except gaierror:
        print ("there was an error resolving the host")
        sys.exit()
    try:
        productDB_socket = socket(AF_INET, SOCK_STREAM)
        print ("Socket is successfully created")
    except error as err:
        print ("Socket creation is failed with error %s" %(err))
    productDB_socket.connect((productDB_ip, productDB_port))

    shoppingCart = {}
    while 1:
        print('Waiting for user command')
        data = clientsock.recv(1024).decode()
        print(data)
        cmd,data = data.split(' ',1)
        print(cmd)
        if cmd=='1111':
            break
        if cmd == '0011':
            #search items for sale
            index = 1
            keywords = data.split(' ')
            catagory = keywords[0]
            finalItems = ''
            while(index<len(keywords)):
                #productDB_socket.send(("GETIIDS "+keywords[index]).encode())
                #itemIDList = productDB_socket.recv(1024).decode()
                responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = "GETIIDS "+keywords[index]))
                itemIDList = responseFromDB
                print(itemIDList)
                itemList = itemIDList.split(' ')
                for itemID in itemList:
                    productDB_socket.send(("GET "+itemID).encode())
                    itemDetails = productDB_socket.recv(1024).decode()
                    if not itemDetails.split(' ')[0] in ['GETFAILURE']:
                        print(itemDetails)
                        itemDetailstTuple = itemDetails.split(' ')
                        if itemDetailstTuple[2] in [catagory] and int(itemDetailstTuple[5])>0:
                            finalItems += itemDetailstTuple[0]+' '+itemDetailstTuple[1]+' '+itemDetailstTuple[2]+' '+itemDetailstTuple[3]+' '+itemDetailstTuple[4]+' '+itemDetailstTuple[5]+'\n'
                index += 1
            clientsock.send(finalItems.encode())
        if cmd=='0100':
			#add item to shopping cart
            itemDetails = data.split(' ')
            #productDB_socket.send(("GET "+itemDetails[0]).encode())
            #itemDBDetails = productDB_socket.recv(1024).decode()
            responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = "GET "+itemDetails[0]))
            itemDBDetails = responseFromDB
            if itemDBDetails.split(' ')[0] in ['GETFAILURE']:
                clientsock.send("Item is not available currently".encode())
            else:    
            if itemDetails[0] in shoppingCart.keys():
                shoppingCart[itemDetails[0]] = str(int(shoppingCart[itemDetails[0]]) + int(itemDetails[1]))
            else:
                shoppingCart[itemDetails[0]] = itemDetails[1]
            clientsock.send("Successfully done ".encode())
        if cmd=='0111':
			#Display shopping cart
            currentCart = ''
            for key in shoppingCart.keys():
                if int(shoppingCart[key])>0:
                    currentCart = currentCart +" item id : " +str(key)+", quantity: "+str(shoppingCart[key])+"\n"
            if currentCart == '':
                currentCart = 'CART EMPTY'
            clientsock.send(currentCart.encode())
        if cmd=='0101':
           # remove an item from cart
            itemDetails = data.split(' ')
            if itemDetails[0] in shoppingCart.keys():
                shoppingCart[itemDetails[0]] = str(int(shoppingCart[itemDetails[0]]) - int(itemDetails[1]))
                if int(shoppingCart[itemDetails[0]])<=0:
                    shoppingCart.pop(itemDetails[0])
                clientsock.send("Successfully done ".encode())
            else:
                clientsock.send("Item doesn't exist ".encode())
        if cmd=='0110':
			#clear the cart
            shoppingCart.clear()
            clientsock.send("Successfully done ".encode())
        print("shopping cart")
        print(shoppingCart)

app.run(host="0.0.0.0", port=8808)
#if __name__ == '__main__':
#    tcpsocket = socket(AF_INET, SOCK_STREAM)
#    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#    tcpsocket.bind(('', SERVERPORT))
#    tcpsocket.listen(5)

#while 1:
#	(clientsock, addr) = tcpsocket.accept()
#	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()
    