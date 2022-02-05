# Distributed Systems Programming Assignments - E-commerce Website

Names:
Soumyadeb Maity
Hemanth Chenna

Our system has the following components and they perform the functions as follows:
1) Product DB - Maintains the details of all the items in an in-memory DB
2) Seller Server - Maintains the list of sellers and the corresponding items those sellers are selling. Acts as the intermediate between the seller and the DB
3) Seller Client - UI for the seller to perform the necessary functions
4) Buyer Server - Maintains the shopping cart for each buyer. Acts as the intermediate between the buyer and the DB
5) Buyer Client - UI for the buyer to perform the necessary functions

All servers and the Product DB are multithreaded and can handle multiple requests at the same time.
However, buffer is not persistent for all the servers and product DB

The response times for the actions are as follows:
1) Seller operations: Avg time is around 3.931 ms local loopback and 24.357 ms for machines connected over LAN
2) Buyer operations: Avg time is around 3.781 ms local loopback and 23.715 ms for machines connected over LAN
