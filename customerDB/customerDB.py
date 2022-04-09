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
import pyuv
import signal

memberId = 0
memberId = input('Enter memberId = ')
memberId = int(memberId)
noOfMems = 5
GSeqNo = -1
msgBuf = {}
ip = ['0.0.0.0', '0.0.0.0', '0.0.0.0', '0.0.0.0', '0.0.0.0']
port = [9000, 9001, 9002, 9003, 9004]

sellerLogIn = {} #userName -> PSW
sellerReview = {} #userName -> REVIEW[PosCOUNT_NegCOUNT]
sellerItems = {} #userName -> ItemIds space separated

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
            return "Account is existing"
        sellerLogIn[userName] = data
        sellerReview[userName] = '0_0'
        return "Account created with username : "+userName


    elif cmd == 'SIGN_IN_B':#buyer create acc
        name, data = data.split(' ',1)
        userName = name +'_'+str(buyerIdGen)
        buyerIdGen += 1
        if userName in buyerLogIn.keys():
            return "Account is existing"
        buyerLogIn[userName] = data
        buyerHistory[userName] = '0'
        return "Account created with username : "+userName
    
    elif cmd == 'LOG_IN_B':#buyer
        userName, data = data.split(' ',1)
        if userName in buyerLogIn.keys():
            if data == buyerLogIn[userName]:
                return "LoggedIn "+userName
            else:
                return "PSW wrong for : "+userName
        else:
            return "Account does not exist with username : "+userName

    elif cmd == 'LOG_IN_S':#seller
        userName, data = data.split(' ',1)
        if userName in sellerLogIn.keys():
            if data == sellerLogIn[userName]:
                return "LoggedIn "+userName
            else:
                return "PSW wrong for : "+userName
        else:
            return "Account does not exist with username : "+userName

    elif cmd == 'PUT_ITEM_IN_S':#seller
        userName, data = data.split(' ',1)
        if userName in sellerItems.keys():
            sellerItems[userName] = sellerItems[userName] +' '+data
        else:
            sellerItems[userName] = data 
        return "Added item with username : "+userName

    elif cmd == 'GET_ITEM_IN_S':#seller
        userName = data
        outputStr = ''
        if userName in sellerItems.keys():
            outputStr = sellerItems[userName]
        else:
            outputStr = 'NO_ITEM'
        return outputStr

    
    elif cmd == 'UPDATE_SELLER_REVIEW':
        userName, data = data.split(' ',1)
        if userName not in sellerReview.keys():
            return "No seller with username: "+userName
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
        return "Review Updated for seller: "+userName

    elif cmd == 'GET_SELLER_REVIEW':
        userName = data        
        if userName not in sellerReview.keys():
            return "No seller with username: "+userName
        review = sellerReview[userName]
        return review
    
    elif cmd == 'UPDATE_BUYER_HISTORY':
        userName, data = data.split(' ',1)
        if userName not in buyerHistory.keys():
            return "No buyer with username: "+userName
        purchaseCount =  buyerHistory[userName]
        purchaseCount = int(purchaseCount) + int(data)
        buyerHistory[userName] = str(purchaseCount)
        return "Purchase history update for buyer: "+userName

    elif cmd == 'GET_BUYER_HISTORY':
        userName = data        
        if userName not in buyerHistory.keys():
            return "No buyer with username: "+userName
        count = buyerHistory[userName]
        return "Purchase history : "+count
    else:
        return "No proper cmd found"

def sendToAllReq(data):
    msg = 'REQ ' + data
    s = socket(AF_INET, SOCK_DGRAM, 0)
    for i in range(5):
        if i is not memberId:
            s.sendto(msg.encode('utf-8'), (ip[i], port[i]))

def sendToAllSeq(SeqNo, data):
    msg = 'SEQ ' + str(SeqNo) + ' ' + data
    s = socket(AF_INET, SOCK_DGRAM, 0)
    for i in range(5):
        if i is not memberId:
            s.sendto(msg.encode('utf-8'), (ip[i], port[i]))

def handleReqMsg(data):
    #Handle request message
    global GSeqNo
    retstr = ""
    if (GSeqNo+1) % noOfMems == memberId:
        #GSeqNo = GSeqNo + 1
        sendToAllSeq(GSeqNo, data)
        retstr = handleSeqMsg(str(GSeqNo) + ' ' + data)
    return retstr

def handleSeqMsg(data):
    #Handle Sequence message
    global GSeqNo
    SeqNo, data = data.split(' ',1)
    SeqNo = int(SeqNo)
    msgBuf[SeqNo] = data
    retstr = ""
    if GSeqNo % noOfMems == memberId or GSeqNo + 1 == SeqNo:
        GSeqNo = SeqNo
        retstr = threadrunner(data)
        while GSeqNo + 1 in msgBuf:
            #GSeqNo = GSeqNo + 1
            threadrunner(msgBuf[GSeqNo])
    return retstr

def onRecvUDP(handle, ip_port, flags, data, error):
    #Receive request message
    global GSeqNo
    if data is not None:
        data = str(data)
        cmd, data = data.split(' ',1)
        if cmd == 'REQ':
            handleReqMsg(data)
        elif cmd == 'SEQ':
            handleSeqMsg(data)


class customerApi(customer_pb2_grpc.customerApiServicer):

    def sendCustomerDB(self, request, context):
        print(request.input1)
        # Send request message to all group members to determine who will sequence this message
        sendToAllReq(request.input1)
        # Receive sequencing message, check if sequence sender is self
        retstr = handleReqMsg(request.input1)
        # After sequencing message, add to buffer and perform action
        # When action is performed, initial receiver of message returns to requester
        #retstr = threadrunner(request.input1)
        return customer_pb2.outputMsg1(output1=retstr)
        #return customer_pb2.outputMsg1(output1="return to servers")


if __name__ == '__main__':
    #global ip
    #global port
    loop = pyuv.Loop.default_loop()
    udpserver = pyuv.UDP(loop)
    udpserver.bind((ip[memberId], port[memberId]))
    udpserver.start_recv(onRecvUDP)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customer_pb2_grpc.add_customerApiServicer_to_server(customerApi(),server)
    server.add_insecure_port('[::]:50055')
    server.start()
    #server.wait_for_termination()

    loop.run()
