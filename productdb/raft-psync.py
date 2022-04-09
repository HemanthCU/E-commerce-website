# The MIT License (MIT)
#python3 raft-psync.py 127.0.0.1:9806  127.0.0.1:9806  127.0.0.1:9806  127.0.0.1:9806 127.0.0.1:9806
# Copyright (c) 2016 Filipp Ozinov

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#https://github.com/bakwc/PySyncObj/blob/master/LICENSE.txt 


from socket import * 
import threading
import sys

SERVERHOST = ''
SERVERPORT = 9806
from pysyncobj import SyncObj
from pysyncobj.batteries import ReplCounter, ReplDict
import sys

#dict1 = ReplDict()
productdb = ReplDict()
keywordDB = ReplDict()
itemsellerDB = ReplDict()

ipList = []
if len(sys.argv) < 5:
       print('please provide 5 IP:port  of raft cluster')
else:
    for i in range(5):
        ipList.append(sys.argv[i+1])
syncObj = SyncObj(ipList[0], [ipList[1],ipList[2],ipList[3],ipList[4]], consumers=[productdb, keywordDB, itemsellerDB])


def threadrunner(clientsock, addr):
    global productdb
    global keywordDB
    global itemsellerDB
    print('Waiting for raft-DB command')
    data = clientsock.recv(1024).decode()
    print(data)
    cmds = data.split(':')
    temp = cmds[0]
    cmds[0] = cmds[1]
    cmds[1] = temp
    if cmds[0] =='getKeys':
              if cmds[1] =='productdb':
                str2 =''
                return clientsock.send(str2.join(productdb.keys()).encode())
              if cmds[1] == 'keywordDB':
                str2 =''
                return clientsock.send(str2.join(keywordDB.keys()).encode())
              if cmds[1] == 'itemsellerDB':
                 str2 =''
                 return clientsock.send(str2.join(itemsellerDB.keys()).encode())

    if cmds[0] =='getValue':
              if cmds[1] =='productdb':
                return clientsock.send(productdb.get(cmds[2]).encode())
              if cmds[1] == 'keywordDB':
                return clientsock.send(keywordDB.get(cmds[2]).encode())
              if cmds[1] == 'itemsellerDB':
                return clientsock.send(itemsellerDB.get(cmds[2]).encode())
                 
    if cmds[0] == 'pop':
              if cmds[1] =='productdb':
                return clientsock.send(productdb.pop(cmds[2]).encode())
              if cmds[1] == 'keywordDB':
                return clientsock.send(keywordDB.pop(cmds[2]).encode())
              if cmds[1] == 'itemsellerDB':
                return clientsock.send(itemsellerDB.pop(cmds[2]).encode())
    if cmds[0] == "add":
              if cmds[1] =='productdb':
                productdb.set(cmds[2],cmds[3])  
              if cmds[1] == 'keywordDB':
                keywordDB.set(cmds[2],cmds[3])
              if cmds[1] == 'itemsellerDB':
                itemsellerDB.set(cmds[2],cmds[3])


#dict1.set('testKey1', 'testValue1', sync=True)
#dict1['testKey2'] = 'testValue2' # this is basically the same as previous, but asynchronous (non-blocking)

tcpsocket = socket(AF_INET, SOCK_STREAM)
tcpsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpsocket.bind(('127.0.0.1', SERVERPORT))
tcpsocket.listen(5)

while 1:
	(clientsock, addr) = tcpsocket.accept()
	threading.Thread(target = threadrunner, args = (clientsock, addr,)).start()
    
#print(counter1, counter2, dict1['testKey1'], dict1.get('testKey2'))