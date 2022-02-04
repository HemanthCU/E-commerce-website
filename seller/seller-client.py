import socket
import threading
import sys

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

#CMD ARG1 ARG2 ARG3

def threadrunner(host_ip, port):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket is successfully created")
  except socket.error as err:
    print ("Socket creation is failed with error %s" %(err))
  
  
  s.connect((host_ip, port))
  
  
  
  s.send('Let me connect'.encode())
  print (s.recv(1024).decode())



print("Buyer client is ready")  
port = 8898
try:
    host_ip = socket.gethostbyname('127.0.0.1')
except socket.gaierror:
    print ("there was an error resolving the host")
    sys.exit()
#while 1:
threading.Thread(target = threadrunner, args = (host_ip, port,)).start()

