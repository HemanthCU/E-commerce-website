#!/usr/bin/env python

from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import base64
import io
import threading
import sys
from socket import * 
import grpc
import requests
import json
import sys
sys.path.append('../')
import backend_pb2
import backend_pb2_grpc
# Initialize the Flask application
app = Flask(__name__)


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

host1 = 'localhost:50054'
channel = grpc.insecure_channel(host1)
stub = backend_pb2_grpc.backendApiStub(channel)

# Put an item for sale: provide all item characteristics and quantity 0100
@app.route('/api/addItem', methods=['POST'])
def put():
    global unique_item_id
    global unique_seller_id
    global sellerDB
    global stub
    r = request
    json_data = r.get_json()
    itemId = str(unique_seller_id)+str(unique_item_id)
    if str(unique_seller_id) in sellerDB.keys():
        list1 = sellerDB[str(unique_seller_id)]
        list1.append(itemId)
        sellerDB[str(unique_seller_id)] = list1
    else:
        sellerDB[str(unique_seller_id)] = [itemId]
    #unique_seller_id = unique_seller_id + 1 // To code
    unique_item_id = unique_item_id + 1
    inputstr = 'ADD '+itemId+' '+json_data['inputstr']
    print(inputstr)
    responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
    print(responseFromDB.output)
    response = {
        'result': responseFromDB.output
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
    
    
# Change the sale price of an item: provide item id and new sale price 0101
@app.route('/api/changeSalesPrice', methods=['POST'])
def change():
    r = request
    global stub
    json_data = r.get_json()
    inputstr = 'UPDATE ' + json_data['inputstr']
    responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
    
    response = {
        'result': responseFromDB.output
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/display', methods=['POST'])
def display():
    r = request
    global stub
    json_data = r.get_json()
    arg = json_data['inputstr']
    itemList = sellerDB[arg]
    resultItemList = ''
    for iid in itemList:
        responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = 'GET '+iid))
        res = responseFromDB.output
        print(res)
        if not res.split(' ')[0] in ['GETFAILURE']:
            resultItemList += res +'\n'

    response = {
        'result': resultItemList
    }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Remove an item from sale: provide item id and quantity 0110
@app.route('/api/removeItem', methods=['POST'])
def remove():
    r = request
    global stub
    json_data = r.get_json()
    inputstr = 'REMOVE ' + json_data['inputstr']
    responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
    
    response = {
        'result': responseFromDB.output
    }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
    
@app.route('/api/close', methods=['POST'])
def close():
    r = request
    global stub
    json_data = r.get_json()
    
    response = {
        'result': 'Successfully exited'
    }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
    
    
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

#if __name__ == '__main__':
#    tcpsocket = socket(AF_INET, SOCK_STREAM)
#    tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
#    tcpsocket.bind(('', SERVERPORT))
#    tcpsocket.listen(5)


#while 1:
#	(clientsock, addr) = tcpsocket.accept()
#	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()

    
# start flask app
app.run(host="0.0.0.0", port=8807)