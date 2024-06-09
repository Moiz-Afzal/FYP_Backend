import pymongo

url ='mongodb+srv://i200867:vj617cultus@cluster0.n7ix9pn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client=pymongo.MongoClient(url)

db = client['ForexMiner']