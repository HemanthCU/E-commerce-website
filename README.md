# Distributed Systems Programming Assignments - E-commerce Website

Group Member Names:
1) Soumyadeb Maity
2) Hemanth Chenna

Our system has the following components and they perform the functions as follows:
1) Product DB - Maintains the details of all the items in an in-memory DB. Connected over GRPC to all the servers. Uses Raft-based PySyncObject to achieve consensus with all the 5 product DBs.
2) Seller Server - Acts as the stateless intermediate between the seller client and the DBs. Connected over GRPC to all the DB nodes and over REST to the clients
3) Seller Client - UI for the seller to perform the necessary functions. Connected over REST to the servers
4) Buyer Server - Acts as the intermediate between the buyer clients and the DBs. Connected over GRPC to all the DBs, over WSDL to the financial transaction service and over REST to the clients
5) Buyer Client - UI for the buyer to perform the necessary functions. Connected over REST to the servers
6) Customer DB - Maintains the list of sellers and the corresponding items those sellers are selling. Maintains the details of all the buyers and sellers along with their login details in an in-memory DB. Maintains review scores for all the sellers and buyer purchase history for all the buyers. Connected over GRPC to all the servers. Uses Rotating Sequencer Atomic Broadcast to achieve consensus with all the 5 customer DBs.
7) Financial transaction service - Returns success of the transaction with 95% chance of success at random. Connected over WSDL/SOAP to Buyer server

All servers, the Customer DB and the Product DB are multithreaded and can handle multiple requests at the same time.
However, buffer is not persistent for all the servers and product DB

Currently, Rotating Sequencer works for some cases and Raft works for some cases but they are not reliably working. Some edge cases have to be handled properly still. Many of the performance numbers are based on individual separated runs of parts of the code and not as a system as a whole as it is not robust enough to handle all the edge cases.

The avg response times for the actions are as follows:
A) All replicas run normally (no failures)
1) Seller operations:
Create account - 35.23ms
Login - 30.45ms
Logout - 32.86ms
Get Seller Rating - 34.92ms
Put an item for sale - 42.53ms
Remove item - 23.88ms
Display items - 41.78ms

2) Buyer operations: 
Create account - 32.15ms
Login - 29.87ms
Logout - 27.35ms
Search items - 25.14ms
Add to cart - 23.00ms
Remove from cart - 21.78ms
Display cart - 22.36ms
Clear cart - 24.12ms
Make purchase - 40.15ms
Provide feedback - 43.22ms
Get Seller Rating - 39.86ms
Get Buyer History - 33.32ms


B) One server-side sellers interface replica and one server-side buyers interface to which some of the clients are connected fail
1) Seller operations:
Create account - 30.45ms
Login - 31.55ms
Logout - 34.76ms
Get Seller Rating - 31.32ms
Put an item for sale - 45.54ms
Remove item - 21.89ms
Display items - 45.65ms

2) Buyer operations: 
Create account - 29.15ms
Login - 31.88ms
Logout - 27.54ms
Search items - 26.22ms
Add to cart - 23.92ms
Remove from cart - 24.58ms
Display cart - 22.55ms
Clear cart - 21.01ms
Make purchase - 48.15ms
Provide feedback - 46.27ms
Get Seller Rating - 41.76ms
Get Buyer History - 35.32ms


C) One product database replica (not the leader) fails
1) Seller operations:
Create account - 30.45ms
Login - 31.55ms
Logout - 34.76ms
Get Seller Rating - 32.34ms
Put an item for sale - 48.44ms
Remove item - 22.99ms
Display items - 

2) Buyer operations: 
Create account - 27.15ms
Login - 35.88ms
Logout - 29.54ms
Search items - 22.22ms
Add to cart - 24.92ms
Remove from cart - 23.58ms
Display cart - 21.55ms
Clear cart - 25.01ms
Make purchase - 49.15ms
Provide feedback - 
Get Seller Rating - 43.76ms
Get Buyer History - 31.32ms


D) Product database replica acting as leader fails
1) Seller operations:
Create account - 30.45ms
Login - 31.55ms
Logout - 34.76ms
Get Seller Rating - 31.32ms
Put an item for sale - 247.14ms
Remove item - 21.89ms
Display items - 45.65ms

2) Buyer operations: 
Create account - 30.15ms
Login - 28.88ms
Logout - 21.54ms
Search items - 27.22ms
Add to cart - 26.92ms
Remove from cart - 21.58ms
Display cart - 28.55ms
Clear cart - 24.01ms
Make purchase - 44.15ms
Provide feedback - 
Get Seller Rating - 42.76ms
Get Buyer History - 35.32ms
