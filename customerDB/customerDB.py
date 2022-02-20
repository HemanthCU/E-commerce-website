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



sellerDB = {}
buyerDB = {}

def threadrunner(data):
    
     return customer_pb2.outputMsg(output="return to servers")
               
        


class backendApi(customer_pb2_grpc.backendApiServicer):

    def sendProductDB(self, request, context):
        print(request.input)
        return threadrunner(request.input)
        #return customer_pb2.outputMsg(output="return to servers")

if __name__ == '__main__':

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customer_pb2_grpc.add_customerApiServicer_to_server(customerApi(),server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()

