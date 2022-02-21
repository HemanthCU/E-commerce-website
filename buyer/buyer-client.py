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
# Exit 1111

#CMD ARG1 ARG2 ARG3 ARG4 ARG5

def threadrunner(addr):
    while 1:
        print("MENU")
        print("0011 - Search based on keywords")
        print("0100 - Add item to cart")
        print("0101 - Remove item from cart")
        print("0111 - Display cart")
        print("0110 - Clear cart")
        print("exit - Close the program")
        val = input("Enter your command: ")
        print("cmd "+val)
        if val== "exit":
            print("exiting")
            #s.send('1111'.encode())
            break
        if val=='0011':
            #search item
            inputstr = input("Enter your item category and keywords with spaced for searching: ")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/searchItems"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("fetching items for sale")
            print(json.loads(response.text)['result'])
            print(response)
        if val=='0100':
            #Add item
            inputstr = input("Enter item ID and quantity: ")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/addItem"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)
        if val=="0101":
            #remove item
            inputstr = input("Enter item ID and quantity: ")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/removeItem"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)
        if val=="0111":
            #display cart
            values = {
                'inputstr' : 'dummy'
            }
            url = addr + "/api/displayCart"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)
        if val=="0110":
            #clear cart
            values = {
                'inputstr' : 'dummy'
            }
            url = addr + "/api/clearCart"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)

port = 8808
host = '127.0.0.1'

addr = f"http://{host}:8808"

threadrunner(addr)