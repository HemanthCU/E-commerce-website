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
    loggedIn = False
    while 1:
        print("MENU")
        print("0000 - Create an account: sets up username and password")
        print("0001 - Login: provide username and password")
        print("0010 - Logout")
        print("0011 - Search based on keywords")
        print("0100 - Add item to cart")
        print("0101 - Remove item from cart")
        print("0111 - Display cart")
        print("0110 - Clear cart")
        print("1000 - Make purchase")
        print("1001 - Provide feedback")
        print("1010 - Get Seller Rating")
        print("1011 - Get Buyer history")
        print("exit - Close the program")
        val = input("Enter your command: ")
        print("cmd "+val)
        if val== "exit":
            print("exiting")
            #s.send('1111'.encode())
            break
        elif val=='0000':
            #Create account
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter username and password to Create Account \n")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/createAccount"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("fetching items for sale")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=='0001':
            #Login
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter username and password to Log in \n")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/login"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("fetching items for sale")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=='0010' and loggedIn==True:
            #Log out
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter username to Log out \n")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/logout"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("fetching items for sale")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=='0011' and loggedIn==True:
            #search item
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter your item category and keywords with spaced for searching: ")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/searchItems"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("fetching items for sale")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=='0100' and loggedIn==True:
            #Add item
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter item ID and quantity: ")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/addItem"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=="0101" and loggedIn==True:
            #remove item
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter item ID and quantity: ")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/removeItem"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=="0111" and loggedIn==True:
            #display cart
            headers = {'content-type': 'application/json'}
            values = {
                'inputstr' : 'dummy'
            }
            url = addr + "/api/displayCart"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=="0110" and loggedIn==True:
            #clear cart
            headers = {'content-type': 'application/json'}
            values = {
                'inputstr' : 'dummy'
            }
            url = addr + "/api/clearCart"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("Checking whether success !!")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=='1000' and loggedIn==True:
            #Make purchase
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter username and password to Create Account \n")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/makePurchase"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("fetching items for sale")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=='1001' and loggedIn==True:
            #Provide feedback
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter username and password to Create Account \n")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/provideFeedback"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("fetching items for sale")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=='1010' and loggedIn==True:
            #Get Seller rating
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter username and password to Create Account \n")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/getSellerRating"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("fetching items for sale")
            print(json.loads(response.text)['result'])
            print(response)
        elif val=='1011' and loggedIn==True:
            #Get Buyer history
            headers = {'content-type': 'application/json'}
            inputstr = input("Enter username and password to Create Account \n")
            values = {
                'inputstr' : inputstr
            }
            url = addr + "/api/getBuyerHistory"
            response = requests.post(url, data=jsonpickle.encode(values), headers=headers)
            print("fetching items for sale")
            print(json.loads(response.text)['result'])
            print(response)
        elif loggedIn==False:
            print("Not logged in, please login and try again")
        else:
            print("Enter a valid option")
port = 8808
host = '127.0.0.1'

addr = f"http://{host}:8808"

threadrunner(addr)