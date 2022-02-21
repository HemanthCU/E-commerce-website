#!/usr/bin/env python

from flask import Flask, request, Response
from PIL import Image
from socket import * 
import jsonpickle
import base64
import io
import threading
import sys
import grpc
import requests
import json
sys.path.append('../')
import backend_pb2
import backend_pb2_grpc
import customer_pb2
import customer_pb2_grpc
# Initialize the Flask application
app = Flask(__name__)



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


if len(sys.argv) < 2:
    print('please give ip of 2 db')

ip1 = sys.argv[1]
ip2 = sys.argv[2]
unique_item_id = 1
loggedInSellerList = {}
host1 = ip1 + ':50054'
channel = grpc.insecure_channel(host1)
stub = backend_pb2_grpc.backendApiStub(channel)

host2 = ip2 + ':50055'
channel1 = grpc.insecure_channel(host2)
stub1 = customer_pb2_grpc.customerApiStub(channel1)

@app.route('/api/createAccount', methods=['POST'])
def createAccount():
    r = request
    global stub1
    json_data = r.get_json()
    inputCmd = 'SIGN_IN_S ' + json_data['inputstr']
    responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = inputCmd))
    response = {
        'result': responseFromCustomerDB.output1
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/logIn', methods=['POST'])
def logIn():
    r = request
    global stub1
    json_data = r.get_json()
    inputCmd = 'LOG_IN_S ' + json_data['inputstr']
    responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = inputCmd))
    outputStr = responseFromCustomerDB.output1
    login1, outputStr = outputStr.split(' ',1)
    if login1 == 'LoggedIn':
        loggedInSellerList[outputStr] = 1
        response = {
            'result': 'Log in successful'
        }
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")
    else:
        response = {
            'result': 'Log in unsuccessful'
        }
        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/logOut', methods=['POST'])
def logOut():
    r = request
    json_data = r.get_json()
    inputCmd = json_data['inputstr']
    if inputCmd in loggedInSellerList.keys():
        loggedInSellerList[inputCmd] = 0
    response = {
        'result': 'logged out'
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/getSellerRating', methods=['POST'])
def getSellerRating():
    r = request
    global stub1
    json_data = r.get_json()
    username = json_data['inputstr']
    outputStr = ''
    if username not in loggedInSellerList.keys():
        outputStr = 'please log in first'
    elif loggedInSellerList[username] != 1:
        outputStr = 'please log in first'
    else:
        inputCmd = 'GET_SELLER_REVIEW ' + username
        responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = inputCmd))
        outputStr = responseFromCustomerDB.output1
    
    response = {
        'result': outputStr
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
    global stub1
    r = request
    json_data = r.get_json()
    inputCmd = json_data['inputstr']
    username, inputCmd = inputCmd.split(' ',1)
    outputStr = ''
    if username not in loggedInSellerList.keys():
        outputStr = 'please log in first'
    elif loggedInSellerList[username] != 1:
        outputStr = 'please log in first'
    else:
        unameSplit = username.split('_')
        sellerId = unameSplit[1]
        itemId = sellerId+'_'+str(unique_item_id)
        cmd1 = 'PUT_ITEM_IN_S ' + username +' '+itemId
        responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = cmd1))
        unique_item_id = unique_item_id + 1
        inputstr = 'ADD '+itemId+' '+username+' '+inputCmd
        print(inputstr)
        responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
        print(responseFromDB.output)
        outputStr = responseFromDB.output
        
    response = {
        'result':outputStr
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

    
# Change the sale price of an item: provide item id and new sale price 0101
@app.route('/api/changeSalesPrice', methods=['POST'])
def change():
    r = request
    global stub
    json_data = r.get_json()
    inputCmd = json_data['inputstr']
    username, inputCmd = inputCmd.split(' ',1)
    outputStr = ''
    if username not in loggedInSellerList.keys():
        outputStr = 'please log in first'
    elif loggedInSellerList[username] != 1:
        outputStr = 'please log in first'
    else:
        inputstr = 'UPDATE ' + inputCmd
        responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
        outputStr = responseFromDB.output
    
    response = {
        'result': outputStr
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/api/display', methods=['POST'])
def display():
    r = request
    global stub
    global stub1
    json_data = r.get_json()
    username = json_data['inputstr']
    outputStr = ''
    if username not in loggedInSellerList.keys():
        outputStr = 'please log in first'
    elif loggedInSellerList[username] != 1:
        outputStr = 'please log in first'
    else:
        cmd1 = 'GET_ITEM_IN_S ' + username
        responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = cmd1))
        outputStr1 = responseFromCustomerDB.output1
        if outputStr1 == 'NO_ITEM':
            outputStr = 'Seller doesnt have any item in customer DB'
        else:
            itemList = outputStr1.split(' ')
            resultItemList = ''
            for iid in itemList:
                responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = 'GET '+iid))
                res = responseFromDB.output
                print(res)
                resSplit = res.split(' ')
                if not resSplit[0] in ['GETFAILURE']:
                    resultItemList += res +'\n'
            if resultItemList == '':
                outputStr = 'Nothing added to product DB'
            else:
                outputStr = resultItemList
    response = {
        'result': outputStr
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
    inputCmd = json_data['inputstr']
    username, inputCmd = inputCmd.split(' ', 1)
    outputStr = ''
    if username not in loggedInSellerList.keys():
        outputStr = 'please log in first'
    elif loggedInSellerList[username] != 1:
        outputStr = 'please log in first'
    else:
        inputstr = 'REMOVE ' + inputCmd
        responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputstr))
        outputStr = responseFromDB.output
    
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