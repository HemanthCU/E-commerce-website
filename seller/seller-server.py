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

@app.route('/api/createAccount', methods=['POST'])
def createAccount():
    r = request
    global stub
    json_data = r.get_json()
    #inputstr = 'UPDATE ' + json_data['inputstr']
    #responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
    # Code me
    response = {
        'result': responseFromDB.output
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/logIn', methods=['POST'])
def logIn():
    r = request
    global stub
    json_data = r.get_json()
    #inputstr = 'UPDATE ' + json_data['inputstr']
    #responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
    # Code me
    response = {
        'result': responseFromDB.output
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/logOut', methods=['POST'])
def logOut():
    r = request
    global stub
    json_data = r.get_json()
    #inputstr = 'UPDATE ' + json_data['inputstr']
    #responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
    # Code me
    response = {
        'result': responseFromDB.output
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/getSellerRating', methods=['POST'])
def getSellerRating():
    r = request
    global stub
    json_data = r.get_json()
    #inputstr = 'UPDATE ' + json_data['inputstr']
    #responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
    # Code me
    response = {
        'result': responseFromDB.output
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Put an item for sale: provide all item characteristics and quantity 0100
@app.route('/api/addItem', methods=['POST'])
def put():
    global unique_item_id
    global unique_seller_id
    global sellerDB
    global stub
    r = request
    json_data = r.get_json()
    itemId = str(unique_seller_id)+'_'+str(unique_item_id)
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

    
# start flask app
app.run(host="0.0.0.0", port=8807)