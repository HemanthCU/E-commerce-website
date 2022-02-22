# Distributed Systems Programming Assignments - E-commerce Website

Group Member Names:
1) Soumyadeb Maity
2) Hemanth Chenna

Our system has the following components and they perform the functions as follows:
1) Product DB - Maintains the details of all the items in an in-memory DB. Connected over GRPC to both the servers
2) Seller Server - Acts as the intermediate between the seller and the DB. Connected over GRPC to both the DBs and over REST to the client
3) Seller Client - UI for the seller to perform the necessary functions. Connected over REST to the server
4) Buyer Server - Maintains the shopping cart for each buyer. Acts as the intermediate between the buyer and the DB. Connected over GRPC to both the DBs, over WSDL to the financial transaction service and over REST to the client
5) Buyer Client - UI for the buyer to perform the necessary functions. Connected over REST to the server
6) Customer DB - Maintains the list of sellers and the corresponding items those sellers are selling. Maintains the details of all the buyers and sellers along with their login details in an in-memory DB. Maintains review scores for all the sellers and buyer purchase history for all the buyers. Connected over GRPC to both the servers
7) Financial transaction service - Returns success of the transaction with 95% chance of success at random. Connected over WSDL/SOAP to Buyer server

All servers, the Customer DB and the Product DB are multithreaded and can handle multiple requests at the same time.
However, buffer is not persistent for all the servers and product DB

The response times for the actions are as follows:
1) Seller operations: Avg time is around 17.010 ms local and 14.234 ms for machines connected over GCP cloud
2) Buyer operations: Avg time is around 14.931 ms local and 12.391 ms for machines connected over GCP cloud
