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
    cmd = data.split(' ',1)
    
    if cmd == 'SIGN_IN_S':
        name = data.split(' ',1)
        userName = name +'_'+str(sellerIdGen)
        sellerIdGen += 1
        if userName in sellerLogIn.keys():
            return customer_pb2.outputMsg(output="Account is exsisting")
        else:    
        sellerLogIn[userName] = data
        sellerReview[userName] = '0_0'
        return customer_pb2.outputMsg(output="Account created with username : "+userName)

    if cmd == 'SIGN_IN_B':
        name = data.split(' ',1)
        userName = name +'_'+str(buyerIdGen)
        buyerIdGen += 1
        if userName in buyerLogIn.keys():
            return customer_pb2.outputMsg(output="Account is exsisting")
        else:    
        buyerLogIn[userName] = data
        buyerHistory[userName] = '0'
        return customer_pb2.outputMsg(output="Account created with username : "+userName)

    if cmd == 'LOG_IN_B':
        userName = data.split(' ',1)
        if userName in buyerLogIn.keys():
            if data == buyerLogIn[userName]:
                return customer_pb2.outputMsg(output="LoggedIn with : "+userName)
            else:
                return customer_pb2.outputMsg(output="PSW wrong for : "+userName)
        else:
            return customer_pb2.outputMsg(output="Account doesnot exist with username : "+userName)  

    if cmd == 'LOG_IN_S':
        userName = data.split(' ',1)
        if userName in sellerLogIn.keys():
            if data == sellerLogIn[userName]:
                return customer_pb2.outputMsg(output="LoggedIn with : "+userName)
            else:
                return customer_pb2.outputMsg(output="PSW wrong for : "+userName)
        else:
            return customer_pb2.outputMsg(output="Account doesnot exist with username : "+userName)  

    if cmd == 'UPDATE_SELLER_REVIEW':
        userName = data.split(' ',1)
        if userName not in sellerReview.keys():
            return customer_pb2.outputMsg(output="No seller with username: "+userName)  
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
        return customer_pb2.outputMsg(output="Review Updated for seller: "+userName)  

    if cmd == 'GET_SELLER_REVIEW':
        userName = data        
        if userName not in sellerReview.keys():
            return customer_pb2.outputMsg(output="No seller with username: "+userName)  
        review = sellerReview[userName]
        return customer_pb2.outputMsg(output="Review : "+review)  
    
    if cmd == 'UPDATE_BUYER_HISTORY':
        userName = data.split(' ',1)
        if userName not in buyerHistory.keys():
            return customer_pb2.outputMsg(output="No buyer with username: "+userName) 
        purchaseCount =  buyerHistory[userName]
        purchaseCount = int(purchaseCount) + int(data)
        buyerHistory[userName] = str(purchaseCount)
        return customer_pb2.outputMsg(output="Purchase history update for buyer: "+userName)

    if cmd == 'GET_BUYER_HISTORY':
        userName = data        
        if userName not in buyerHistory.keys():
            return customer_pb2.outputMsg(output="No buyer with username: "+userName)  
        count = buyerHistory[userName]
        return customer_pb2.outputMsg(output="Purchase history : "+count)
    
    return customer_pb2.outputMsg(output="No proper cmd found")

               
class customerApi(customer_pb2_grpc.customerApiServicer):

    def sendCustomerDB(self, request, context):
        print(request.input)
        return threadrunner(request.input)
        #return customer_pb2.outputMsg(output="return to servers")


if __name__ == '__main__':

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customer_pb2_grpc.add_customerApiServicer_to_server(customerApi(),server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

