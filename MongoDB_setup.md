# MongoDB Setup and Introduction 

## SET DIRECTORY IN WINDOWS and create a Bin in desired folder 
```
C:\>cd Windows
```
```
C:\Windows>d:
```
```
D:\>cd mongoDB_DCMME
```
```
D:\mongoDB_DCMME>cd bin
```
This sets the bin folder for MonogDB inside the "MongoDB_DCMME" file which I created within the D drive 

## Setup the necessary folders (data,log,db)
Create 2 folders named "data" and "log" with your MongoDB folder (mine is "MongoDB_DCMME"). Also create a folder named "db" inside the data folder that will contain your unstructured databases 

## Install mongoDB with this data and log folders
```
D:\mongoDB_DCMME\bin>mongod --directoryperdb --dbpath D:\mongoDB_DCMME\data\db --logpath D:\mongoDB_DCMME\log\mongo.log --logappend  --install
```
Once mongoDB is setup with the log, data and db folders. It's now time to start MongoDB from your bin folder that you setup
```
D:\mongoDB_DCMME\bin>net start MongoDB
```

## Access mongo environment from cmd 
Type in "mongo" into the bin folder to get into the mongo environemnt and use it's commands 
```
D:\mongoDB_DCMME\bin>mongo
```

You might get some output 
```
MongoDB shell version v4.0.0
connecting to: mongodb://127.0.0.1:27017
MongoDB server version: 4.0.0
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
        http://docs.mongodb.org/
Questions? Try the support group
        http://groups.google.com/group/mongodb-user
Server has startup warnings:
2018-07-05T00:07:26.976-0400 I CONTROL  [initandlisten]
2018-07-05T00:07:26.976-0400 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2018-07-05T00:07:26.976-0400 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2018-07-05T00:07:26.976-0400 I CONTROL  [initandlisten]
---
Enable MongoDB's free cloud-based monitoring service to collect and display
metrics about your deployment (disk utilization, CPU, operation statistics,
etc).

The monitoring data will be available on a MongoDB website with a unique
URL created for you. Anyone you share the URL with will also be able to
view this page. MongoDB may use this information to make product
improvements and to suggest MongoDB products and deployment options to you.

To enable free monitoring, run the following command:
db.enableFreeMonitoring()
---
```

## Databases and Collections 
```
> show dbs
```
Since no datbases have been setup we get the following output:
```
admin   0.000GB
config  0.000GB
local   0.000GB
```

### Creating a database
```
> use mycustomers
```

### Check the databases 
This command will show the list of databases that are present in the directory you are working within 
```
> db
```

### Create a user for the Database 

> db.createUser({user:"Mihir", pwd:"12345", roles:["readWrite","dbAdmin"]})
Successfully added user: { "user" : "Mihir", "roles" : [ "readWrite", "dbAdmin" ] }

### Create a collection 
MongoDB stores documents in collections. Collections are analogous to tables in relational databases.

```
> db.createCollection('customers');
{ "ok" : 1 }
```
```
> show collections
customers
```
```
> db
mycustomers
```

### Insert Elements into the Collection 
```
> db.customers.insert({first_name:"John", last_name:"DOE"})
```

### View the customers using find()
```
> db.customers.find();
```
OUTPUT:
```
{ "_id" : ObjectId("5b3da003a832f048a9e7571a"), "first_name" : "John", "last_name" : "DOE" }
```

### Insert entries into collection using insert()
```
> db.customers.insert([{first_name: "Steven",last_name:"Prast"},{first_name:"Someguy"}])
```

To print the new customers collection using the command below 
Note : If this doesn't work - set pretty to the Default way to print (instructions below)
```
> db.customer.find().pretty
```


### print the objects inside a colleciton 
```
> db.customers.find()
{ "_id" : ObjectId("5b3da003a832f048a9e7571a"), "first_name" : "John", "last_name" : "DOE" }
{ "_id" : ObjectId("5b3da06ca832f048a9e7571b"), "first_name" : "Steven", "last_name" : "Prast" }
{ "_id" : ObjectId("5b3da06ca832f048a9e7571c"), "first_name" : "Someguy" }
```


### set the default print option to "Pretty"
Pretty allows you to clearly view your objects inside the collection you wish to print 
```
> DBQuery.prototype._prettyShell = true
true
```
Now when you print the colleciton 
```
> db.customers.find()
```

A clearer output is obtained. This is especially useful as unstructured databases tend to get messy with increasing number of keys and entries. 
```
{
        "_id" : ObjectId("5b3da003a832f048a9e7571a"),
        "first_name" : "John",
        "last_name" : "DOE"
}
{
        "_id" : ObjectId("5b3da06ca832f048a9e7571b"),
        "first_name" : "Steven",
        "last_name" : "Prast"
}
{ "_id" : ObjectId("5b3da06ca832f048a9e7571c"), "first_name" : "Someguy" }
```

Author 
Mihir Bhatia
https://www.mihirbhatia.com
