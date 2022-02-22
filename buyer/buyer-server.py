#!/usr/bin/env python

from flask import Flask, request, Response

from socket import * 
from unicodedata import category
import jsonpickle
from zeep import Client
import io
import threading
import sys
import grpc
import requests
import json
import random
sys.path.append('../')
import backend_pb2
import backend_pb2_grpc
import customer_pb2
import customer_pb2_grpc
# Initialize the Flask application
app = Flask(__name__)

if len(sys.argv) < 2:
    print('please give ip of 2 db')

ip1 = sys.argv[1]
ip2 = sys.argv[2]
host1 = ip2 + ':50054'
channel = grpc.insecure_channel(host1)
stub = backend_pb2_grpc.backendApiStub(channel)

host2 = ip2 + ':50055'
channel1 = grpc.insecure_channel(host2)
stub1 = customer_pb2_grpc.customerApiStub(channel1)

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
shoppingCartDB = {}
loggedInBuyerList = {}

@app.route('/api/createAccount', methods=['POST'])
def createAccount():
    r = request
    global stub1
    json_data = r.get_json()
    inputCmd = 'SIGN_IN_B ' + json_data['inputstr']
    responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = inputCmd))
    response = {
        'result': responseFromCustomerDB.output1
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

@app.route('/api/login', methods=['POST'])
def login():
    r = request
    global stub1
    json_data = r.get_json()
    inputCmd = 'LOG_IN_B ' + json_data['inputstr']
    responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = inputCmd))
    outputStr = responseFromCustomerDB.output1
    login1, outputStr = outputStr.split(' ',1)
    if login1 == 'LoggedIn':
        loggedInBuyerList[outputStr] = 1
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

@app.route('/api/logout', methods=['POST'])
def logout():
    global loggedInBuyerList
    r = request
    json_data = r.get_json()
    inputCmd = json_data['inputstr']
    if inputCmd in loggedInBuyerList.keys():
        loggedInBuyerList[inputCmd] = 0
    response = {
        'result': 'logged out'
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

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
            resFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = "GET "+itemID))
            itemDetails = resFromDB.output
            if not itemDetails.split(' ')[0] in ['GETFAILURE']:
                print(itemDetails)
                itemDetailstTuple = itemDetails.split(' ')
                if itemDetailstTuple[2] in [category] and int(itemDetailstTuple[5])>0:
                    finalItems += itemDetailstTuple[0]+' '+itemDetailstTuple[1]+' '+itemDetailstTuple[2]+' '+itemDetailstTuple[3]+' '+itemDetailstTuple[4]+' '+itemDetailstTuple[5]+'\n'
        index += 1
    response = {
        'result': finalItems
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Add item to the shopping cart: provide item id and quantity CMD 0100
@app.route('/api/addItem', methods=['POST'])
def addItem():
    r = request
    global stub
    global shoppingCartDB
    shoppingCart = {}
    json_data = r.get_json()
    inputstr = json_data['inputstr']
    username, inputstr = inputstr.split(' ',1)
    itemDetails = inputstr.split(' ')
    responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = "GET "+itemDetails[0]))
    itemDBDetails = responseFromDB.output
    item_quantity = itemDBDetails.split(' ')[5]
    if itemDBDetails.split(' ')[0] in ['GETFAILURE']:
        respstr = "Item is not available currently"
    else:
        respstr = "Item added successfully"
        if itemDetails[0] in shoppingCart.keys():
            shoppingCart[itemDetails[0]] = str(min(int(shoppingCart[itemDetails[0]]) + int(itemDetails[1]), int(item_quantity)))
        else:
            shoppingCart[itemDetails[0]] = str(min(int(itemDetails[1]), int(item_quantity)))
    shoppingCartDB[username] = shoppingCart
    response = {
        'result': respstr
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Remove item from the shopping cart: provide item id and quantity CMD 0101
@app.route('/api/removeItem', methods=['POST'])
def removeItem():
    r = request
    global shoppingCartDB
    json_data = r.get_json()
    inputstr = json_data['inputstr']
    username, inputstr = inputstr.split(' ',1)
    shoppingCart = shoppingCartDB[username]
    itemDetails = inputstr.split(' ')
    if itemDetails[0] in shoppingCart.keys():
        shoppingCart[itemDetails[0]] = str(int(shoppingCart[itemDetails[0]]) - int(itemDetails[1]))
        if int(shoppingCart[itemDetails[0]])<=0:
            shoppingCart.pop(itemDetails[0])
        shoppingCartDB[username] = shoppingCart
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
    global shoppingCartDB
    json_data = r.get_json()
    username = json_data['inputstr']
    shoppingCart = shoppingCartDB[username]
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

# Clear the shopping cart CMD 0110
@app.route('/api/clearCart', methods=['POST'])
def clearCart():
    r = request
    global shoppingCartDB
    json_data = r.get_json()
    username = json_data['inputstr']
    shoppingCartDB.pop(username)
    response = {
        'result': "Successfully cleared cart"
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Make purchase CMD 1000
@app.route('/api/makePurchase', methods=['POST'])
def makePurchase():
    r = request
    global stub
    global stub1
    global shoppingCartDB
    json_data = r.get_json()
    inputstr = json_data['inputstr']
    username, inputstr = inputstr.split(' ',1)
    creditCardDetails = inputstr
    client = Client(wsdl ='http://localhost:5006/wsdl?wsdl')
    wsdlRes = client.service.MessageSplitter(creditCardDetails,username)
    purchance = int(wsdlRes[0])
    print(purchance)
    if purchance < 95:
        #Decrease amount purchased from ProductDB
        shoppingCart = shoppingCartDB[username]
        shoppingCartDB.pop(username)
        itemcount = 0
        for key in shoppingCart.keys():
            if int(shoppingCart[key])>0:
                inputCmd = 'REMOVE ' + key + ' ' + shoppingCart[key]
                responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = inputCmd))
                itemcount = itemcount + 1
        #Update purchase to buyer history
        inputCmd = 'UPDATE_BUYER_HISTORY ' + username + ' ' + str(itemcount)
        responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = inputCmd))
        respstr = responseFromCustomerDB.output1
        print(respstr)
        outstr = "Successfully made purchase"
    else:
        outstr = "Purchase failed. Please try again later"
    response = {
        'result': outstr
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Provide feedback: thumbs up or down for each item purchased, at most one feedback per purchased item CMD 1001
@app.route('/api/provideFeedback', methods=['POST'])
def provideFeedback():
    r = request
    global stub
    global stub1
    json_data = r.get_json()
    inputstr = json_data['inputstr']
    username, inputstr = inputstr.split(' ',1)
    #Format of inputstr: itemid1 feedback1
    itemid, inputstr = inputstr.split(' ',1)
    responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = "GETSID "+itemid))
    sellerUserName = responseFromDB.output
    if sellerUserName in ['GETSIDFAILURE']:
        respstr = "Seller does not exist"
    else:
        inputCmd = 'UPDATE_SELLER_REVIEW ' + sellerUserName + ' ' + inputstr
        responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = inputCmd))
        respstr = responseFromCustomerDB.output1
    response = {
        'result': respstr
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Get seller rating: provide buyer id CMD 1010
@app.route('/api/getSellerRating', methods=['POST'])
def getSellerRating():
    r = request
    global stub1
    json_data = r.get_json()
    inputstr = json_data['inputstr']
    username, inputstr = inputstr.split(' ',1)
    responseFromDB = stub.sendProductDB(backend_pb2.inputMsg(input = "GETSID "+inputstr))
    sellerUserName = responseFromDB.output
    if sellerUserName in ['GETSIDFAILURE']:
        respstr = "Seller does not exist"
    else:     
        inputCmd = 'GET_SELLER_REVIEW ' + sellerUserName
        responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = inputCmd))
        respstr = responseFromCustomerDB.output1
    response = {
        'result': respstr
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# Get buyer history CMD 1011
@app.route('/api/getBuyerHistory', methods=['POST'])
def getBuyerHistory():
    r = request
    global stub1
    json_data = r.get_json()
    inputstr = json_data['inputstr']
    username = inputstr
    inputCmd = 'GET_BUYER_HISTORY ' + inputstr
    responseFromCustomerDB = stub1.sendCustomerDB(customer_pb2.inputMsg1(input1 = inputCmd))
    respstr = responseFromCustomerDB.output1
    response = {
        'result': respstr
    }
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

app.run(host="0.0.0.0", port=8808)
    