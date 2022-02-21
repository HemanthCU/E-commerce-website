#!/usr/bin/env python
from concurrent import futures
from ast import keyword
from socket import * 
import threading
import grpc
import sys
sys.path.append('../')
import customer_pb2
import customer_pb2_grpc




sellerLogIn = {} #userName -> PSW
sellerReview = {} #userName -> REVIEW[PosCOUNT_NegCOUNT]
sellerItems = {} #userName -> ItemIds space separated
sellerIDtoUserName = {}
sellerIdGen = 1

buyerLogIn = {} #userName -> PSW
buyerHistory = {} #userName -> Purchase Count
buyerIdGen = 1

def threadrunner(data):
    global sellerLogIn
    global sellerReview
    global buyerLogIn
    global buyerHistory
    global sellerIdGen
    global buyerIdGen
    print('here1 ' + data)
    cmd, data = data.split(' ',1)
    print(cmd)
    if cmd == 'SIGN_IN_S': #seller create acc
        name, data = data.split(' ',1)
        userName = name +'_'+str(sellerIdGen)
        sellerIdGen += 1
        if userName in sellerLogIn.keys():
            return customer_pb2.outputMsg1(output1="Account is existing")
        sellerLogIn[userName] = data
        sellerIDtoUserName[sellerIdGen-1] = userName
        sellerReview[userName] = '0_0'
        return customer_pb2.outputMsg1(output1="Account created with username : "+userName)


    elif cmd == 'SIGN_IN_B':#buyer create acc
        name, data = data.split(' ',1)
        userName = name +'_'+str(buyerIdGen)
        buyerIdGen += 1
        if userName in buyerLogIn.keys():
            return customer_pb2.outputMsg1(output1="Account is existing") 
        buyerLogIn[userName] = data
        buyerHistory[userName] = '0'
        return customer_pb2.outputMsg1(output1="Account created with username : "+userName)
    
    elif cmd == 'LOG_IN_B':#buyer
        userName, data = data.split(' ',1)
        if userName in buyerLogIn.keys():
            if data == buyerLogIn[userName]:
                return customer_pb2.outputMsg1(output1="LoggedIn "+userName)
            else:
                return customer_pb2.outputMsg1(output1="PSW wrong for : "+userName)
        else:
            return customer_pb2.outputMsg1(output1="Account does not exist with username : "+userName)  

    elif cmd == 'LOG_IN_S':#seller
        userName, data = data.split(' ',1)
        if userName in sellerLogIn.keys():
            if data == sellerLogIn[userName]:
                return customer_pb2.outputMsg1(output1="LoggedIn "+userName)
            else:
                return customer_pb2.outputMsg1(output1="PSW wrong for : "+userName)
        else:
            return customer_pb2.outputMsg1(output1="Account does not exist with username : "+userName)

    elif cmd == 'PUT_ITEM_IN_S':#seller
        userName, data = data.split(' ',1)
        if userName in sellerItems.keys():
            sellerItems[userName] = sellerItems[userName] +' '+data
        else:
            sellerItems[userName] = data 
        return customer_pb2.outputMsg1(output1="Added item with username : "+userName)

    elif cmd == 'GET_ITEM_IN_S':#seller
        userName = data
        outputStr = ''
        if userName in sellerItems.keys():
            outputStr = sellerItems[userName]
        else:
            outputStr = 'NO_ITEM'
        return customer_pb2.outputMsg1(output1=outputStr)    

    
    elif cmd == 'UPDATE_SELLER_REVIEW':
        userName, data = data.split(' ',1)
        if userName not in sellerReview.keys():
            return customer_pb2.outputMsg1(output1="No seller with username: "+userName)  
        review = sellerReview[userName]
        pos, neg = review.split('_')
        pos = int(pos)
        neg = int(neg)
        if data == 'P':
            pos += 1
        else:
            neg += 1
        review = str(pos)+'_'+str(neg)
        sellerReview[userName] = review
        return customer_pb2.outputMsg1(output1="Review Updated for seller: "+userName)  

    elif cmd == 'GET_SELLER_REVIEW':
        userName = data        
        if userName not in sellerReview.keys():
            return customer_pb2.outputMsg1(output1="No seller with username: "+userName)  
        review = sellerReview[userName]
        return customer_pb2.outputMsg1(output1=review)  
    
    elif cmd == 'UPDATE_BUYER_HISTORY':
        userName, data = data.split(' ',1)
        if userName not in buyerHistory.keys():
            return customer_pb2.outputMsg1(output1="No buyer with username: "+userName) 
        purchaseCount =  buyerHistory[userName]
        purchaseCount = int(purchaseCount) + int(data)
        buyerHistory[userName] = str(purchaseCount)
        return customer_pb2.outputMsg1(output1="Purchase history update for buyer: "+userName)

    elif cmd == 'GET_BUYER_HISTORY':
        userName = data        
        if userName not in buyerHistory.keys():
            return customer_pb2.outputMsg1(output1="No buyer with username: "+userName)  
        count = buyerHistory[userName]
        return customer_pb2.outputMsg1(output1="Purchase history : "+count)
    else:
        return customer_pb2.outputMsg1(output1="No proper cmd found")

               
class customerApi(customer_pb2_grpc.customerApiServicer):

    def sendCustomerDB(self, request, context):
        print(request.input1)
        return threadrunner(request.input1)
        #return customer_pb2.outputMsg1(output1="return to servers")


if __name__ == '__main__':

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customer_pb2_grpc.add_customerApiServicer_to_server(customerApi(),server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

