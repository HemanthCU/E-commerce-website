#!/usr/bin/env python
from concurrent import futures
from ast import keyword
from socket import * 
import threading
import grpc
import sys
sys.path.append('../')
import backend_pb2
import backend_pb2_grpc

#SERVERHOST = ''
#SERVERPORT = 8886

#Storage format: ID Quantity Name Category Condition Price Keyword1...

productdb = {}
keywordDB = {}
itemsellerDB = {}

def threadrunner(data):
    global productdb
    global keywordDB
    global itemsellerDB
    #print(clientsock)
    #print(addr)
    while 1:
        #data = clientsock.recv(1024).decode()
        if data == 'CLOSE':
            break
        #Input format: CMD   Name, Category ID,  Condition, Price, Quantity,  Keyword1...
        cmd, data = data.split(' ', 1)
        #List of commands: GET(based on ID) ADD UPDATE REMOVE
        
        if cmd == 'GET':
            iid = data
            if iid in productdb.keys():
                return backend_pb2.outputMsg(output=(iid + ' ' + productdb[iid]))
                #clientsock.send((iid + ' ' + productdb[iid]).encode())
            else:
                return backend_pb2.outputMsg(output="GETFAILURE  -  item does not exist")
                #clientsock.send("GETFAILURE  -  item does not exist".encode())     

        if cmd == 'GETIIDS':
            if data in keywordDB.keys():
                retstr = ''
                for item in keywordDB[data]:
                    retstr = retstr + str(item) + ' '
                print(retstr)
                return backend_pb2.outputMsg(output=retstr)
                #clientsock.send(retstr.encode())
            else:
                return backend_pb2.outputMsg(output="GETIIDS FAILURE  -  item does not exist")
                #clientsock.send("GETIIDS FAILURE  -  item does not exist".encode())     

        elif cmd == 'ADD':
            iid, data = data.split(' ', 1)
            sellerUserName, data = data.split(' ', 1)
            if iid not in productdb.keys():
                itemsellerDB[iid] = sellerUserName
                productdb[iid] = data
                characteristics = data.split(' ')
                i = 5
                while i<len(characteristics):
                    if characteristics[i] in keywordDB.keys():
                        list1 = keywordDB[characteristics[i]]
                        list1.append(iid)
                        keywordDB[characteristics[i]] = list1
                    else:
                        keywordDB[characteristics[i]] = [iid]
                    i = i + 1
                return backend_pb2.outputMsg(output="ADDSUCCESS")    
                #clientsock.send("ADDSUCCESS".encode()) 
            else:
                return backend_pb2.outputMsg(output="ADDFAILURE  - already exsisting item")
                #clientsock.send("ADDFAILURE  - already exsisting item".encode())    
   

        elif cmd == 'UPDATE':
            iid, data = data.split(' ', 1)
            newprice = data
            if iid in productdb.keys():
                itemDetails = productdb[iid].split(' ')
                itemDetails[3] = newprice
                newDetails = ''
                for details in itemDetails:
                    newDetails += details+' '
                productdb[iid] = newDetails
                return backend_pb2.outputMsg(output="UPDATE SUCCESS ")
                #clientsock.send("UPDATE SUCCESS ".encode()) 
            else:
                return backend_pb2.outputMsg(output="UPDATE FAILURE  -  item does not exist")
                #clientsock.send("UPDATE FAILURE  -  item does not exist".encode())      
    
        elif cmd in ['REMOVE']:
            iid, data = data.split(' ', 1)
            remquant = int(data)
            if iid in productdb.keys():
                itemDetails = productdb[iid].split(' ')
                newQuant = int(itemDetails[4]) - remquant
                if newQuant<=0:
                    newQuant=0
                    poppeddata = productdb.pop(iid)
                    itemsellerDB.pop(iid)
                    characteristics = poppeddata.split(' ')
                    i = 5
                    while i<len(characteristics):
                        if characteristics[i] in keywordDB.keys():
                            list1 = keywordDB[characteristics[i]]
                            list1.remove(iid)
                            keywordDB[characteristics[i]] = list1
                        i = i + 1
                else:
                    itemDetails[4] = str(int(itemDetails[4]) - remquant)
                    newDetails = ''
                    for details in itemDetails:
                        newDetails += details+' '
                    productdb[iid] = newDetails
                return backend_pb2.outputMsg(output="REMOVE SUCCESS ")
                #clientsock.send("REMOVE SUCCESS ".encode()) 
            else:
                return backend_pb2.outputMsg(output="REMOVEFAILURE  -  item does not exist")
                #clientsock.send("REMOVEFAILURE  -  item does not exist".encode()) 
        elif cmd in ['GETSID']:
            if data in itemsellerDB.keys():
                retstr = itemsellerDB[data]
                return backend_pb2.outputMsg(output=retstr)
                #clientsock.send(retstr.encode())
            else:
                return backend_pb2.outputMsg(output="GETSIDFAILURE")
        print(productdb)
        print(keywordDB)
        


class backendApi(backend_pb2_grpc.backendApiServicer):

    def sendProductDB(self, request, context):
        print(request.input)
        return threadrunner(request.input)
        #return backend_pb2.outputMsg(output="Successfully received command")

if __name__ == '__main__':
    #tcpsocket = socket(AF_INET, SOCK_STREAM)
    #tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    #tcpsocket.bind((SERVERHOST, SERVERPORT))
    #tcpsocket.listen(5)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2_grpc.add_backendApiServicer_to_server(backendApi(),server)
    server.add_insecure_port('[::]:50054')
    server.start()
    server.wait_for_termination()

