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
ipList= []
raftDB_port = 8886

try:
    raftDB_socket = socket(AF_INET, SOCK_STREAM)
    print ("Socket is successfully created")
except error as err:
    print ("Socket creation is failed with error %s" %(err))

def connectRaftDB(dbName, cmd = '', arg = '',arg2 = ''):
    try:
      raftDB_socket = socket(AF_INET, SOCK_STREAM)
      print ("Socket is successfully created")
    except error as err:
      print ("Socket creation is failed with error %s" %(err))
    for i in range(0,5):
        try:
          raftDB_socket.connect((ipList[i], raftDB_port))
          if cmd =='getKeys':
              raftDB_socket.send((dbName + " "+cmd).encode())
              return raftDB_socket.recv(1024).decode().split(' ')
          if cmd =='getValue':
              raftDB_socket.send((dbName +" " +cmd+" "+arg).encode())
              return raftDB_socket.recv(1024).decode()
          if cmd == 'pop':
              raftDB_socket.send((dbName +" " +cmd+" "+arg).encode())
              return raftDB_socket.recv(1024).decode()
          if cmd == "add":
              raftDB_socket.send((dbName +" " +cmd+" "+arg+" "+arg2).encode())
          raftDB_socket.close()
          return

        except OSError as msg:
          #raftDB_socket.close()
          print("Raft sever "+str(i)+" ip "+str(ipList[i])+" is down")
          continue
    
    print(" All the raft db servers are down")


        


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
            keys = connectRaftDB(dbName='productdb',cmd= 'getKeys')
            chachedKeys = productdb.keys()
            for i in range(len(keys)):
                if keys[i] != chachedKeys[i]:
                     chachedKeys = keys
                     break
            if iid in chachedKeys:
                cachedVal = productdb[iid]
                value =  connectRaftDB(dbName='productdb',cmd= 'getValue',arg=iid)
                if value!=cachedVal:
                    cachedVal = value
                return backend_pb2.outputMsg(output=iid + ' ' + cachedVal)
                #clientsock.send((iid + ' ' + productdb[iid]).encode())
            else:
                return backend_pb2.outputMsg(output="GETFAILURE  -  item does not exist")
                #clientsock.send("GETFAILURE  -  item does not exist".encode())     

        if cmd == 'GETIIDS':
            keys = connectRaftDB(dbName='keywordDB',cmd= 'getKeys')
            chachedKeys = keywordDB.keys()
            for i in range(len(keys)):
                if keys[i] != chachedKeys[i]:
                     chachedKeys = keys
                     break
            if data in chachedKeys:
                retstr = ''
                cachedVal = keywordDB[data]
                value =  connectRaftDB(dbName='keywordDB',cmd= 'getValue',arg=data)
                if value!=cachedVal:
                    cachedVal = value
                for item in cachedVal:
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
                connectRaftDB(dbName='itemsellerDB',cmd= 'add',arg=iid,arg2=sellerUserName)
                itemsellerDB[iid] = sellerUserName
                connectRaftDB(dbName='productdb',cmd= 'add',arg=iid,arg2=data)
                productdb[iid] = data
                
                characteristics = data.split(' ')
                i = 5
                while i<len(characteristics):
                    keys = connectRaftDB(dbName='keywordDB',cmd= 'getKeys')
                    chachedKeys = keywordDB.keys()
                    for i in range(len(keys)):
                       if keys[i] != chachedKeys[i]:
                         chachedKeys = keys
                         break
                    if characteristics[i] in chachedKeys:
                        cachedVal = keywordDB[characteristics[i]]
                        value =  connectRaftDB(dbName='keywordDB',cmd= 'getValue',arg=characteristics[i])
                        if value!=cachedVal:
                           cachedVal = value
                        list1 = cachedVal
                        list1.append(iid)
                        keywordDB[characteristics[i]] = list1
                        str2 = ""
                        connectRaftDB(dbName='keywordDB',cmd= 'add',arg=characteristics[i],arg2=str(str2.join(list1)))
                    else:
                        connectRaftDB(dbName='keywordDB',cmd= 'add',arg=characteristics[i],arg2=iid)
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
            keys = connectRaftDB(dbName='productdb',cmd= 'getKeys')
            chachedKeys = productdb.keys()
            for i in range(len(keys)):
                if keys[i] != chachedKeys[i]:
                    chachedKeys = keys
                    break
            if iid in chachedKeys:
                cachedVal = productdb[iid]
                value =  connectRaftDB(dbName='productdb',cmd= 'getValue',arg=iid)
                if value!=cachedVal:
                    cachedVal = value
                itemDetails = cachedVal.split(' ')
                itemDetails[3] = newprice
                newDetails = ''
                for details in itemDetails:
                    newDetails += details+' '
                connectRaftDB(dbName='productdb',cmd= 'add',arg=iid,arg2=newDetails)    
                productdb[iid] = newDetails
                return backend_pb2.outputMsg(output="UPDATE SUCCESS ")
                #clientsock.send("UPDATE SUCCESS ".encode()) 
            else:
                return backend_pb2.outputMsg(output="UPDATE FAILURE  -  item does not exist")
                #clientsock.send("UPDATE FAILURE  -  item does not exist".encode())      
    
        elif cmd in ['REMOVE']:
            iid, data = data.split(' ', 1)
            remquant = int(data)
            keys = connectRaftDB(dbName='productdb',cmd= 'getKeys')
            chachedKeys = productdb.keys()
            for i in range(len(keys)):
                if keys[i] != chachedKeys[i]:
                    chachedKeys = keys
                    break
            if iid in chachedKeys:
                cachedVal = productdb[iid]
                value =  connectRaftDB(dbName='productdb',cmd= 'getValue',arg=iid)
                if value!=cachedVal:
                    cachedVal = value
                itemDetails = cachedVal.split(' ')
                newQuant = int(itemDetails[4]) - remquant
                if newQuant<=0:
                    newQuant=0
                    poppeddata = connectRaftDB(dbName='productdb',cmd= 'pop',arg=iid)   
                    poppeddataCached = productdb.pop(iid)
                    if(poppeddata != poppeddataCached):
                        poppeddataCached = poppeddata
                    connectRaftDB(dbName='itemsellerDB',cmd= 'pop',arg=iid)   
                    itemsellerDB.pop(iid)
                    characteristics = poppeddataCached.split(' ')
                    i = 5
                    while i<len(characteristics):
                        keys = connectRaftDB(dbName='keywordDB',cmd= 'getKeys')
                        chachedKeys = keywordDB.keys()
                        for i in range(len(keys)):
                            if keys[i] != chachedKeys[i]:
                               chachedKeys = keys
                               break
                        if characteristics[i] in chachedKeys:
                            cachedVal = keywordDB[characteristics[i]]
                            value =  connectRaftDB(dbName='keywordDB',cmd= 'getValue',arg=characteristics[i]).split(' ')
                            if value!=cachedVal:
                                cachedVal = value
                            list1 = cachedVal
                            list1.remove(iid)
                            keywordDB[characteristics[i]] = list1
                            str2 = ""
                            connectRaftDB(dbName='keywordDB',cmd= 'add',arg=characteristics[i],arg2=str(str2.join(list1)))
                        i = i + 1
                else:
                    itemDetails[4] = str(int(itemDetails[4]) - remquant)
                    newDetails = ''
                    for details in itemDetails:
                        newDetails += details+' '
                    connectRaftDB(dbName='productdb',cmd= 'add',arg=iid,arg2=newDetails)
                    productdb[iid] = newDetails
                return backend_pb2.outputMsg(output="REMOVE SUCCESS ")
                #clientsock.send("REMOVE SUCCESS ".encode()) 
            else:
                return backend_pb2.outputMsg(output="REMOVEFAILURE  -  item does not exist")
                #clientsock.send("REMOVEFAILURE  -  item does not exist".encode()) 
        elif cmd in ['GETSID']:
            keys = connectRaftDB(dbName='itemsellerDB',cmd= 'getKeys')
            chachedKeys = itemsellerDB.keys()
            for i in range(len(keys)):
                if keys[i] != chachedKeys[i]:
                    chachedKeys = keys
                    break
            if data in chachedKeys:
                cachedVal = itemsellerDB[data]
                value =  connectRaftDB(dbName='itemsellerDB',cmd= 'getValue',arg=data)
                if value!=cachedVal:
                    cachedVal = value
                retstr = cachedVal
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
    if len(sys.argv) < 5:
       print('Please provide 5 IP:port of raft cluster')
    else:
       for i in range(5):
           ipList.append(sys.argv[i+1])

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2_grpc.add_backendApiServicer_to_server(backendApi(),server)
    server.add_insecure_port('[::]:50054')
    server.start()
    server.wait_for_termination()

