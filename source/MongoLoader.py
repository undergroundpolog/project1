'''
Created on 27 ago. 2017

@author: alejandro
'''

from pymongo import MongoClient
from fileutils.Config import Config
import threading
import sys
from time import sleep


class MongoWriterThread(threading.Thread):
    
    def __init__(self,db,dictionaries):
        threading.Thread.__init__(self)
        self.db = db
        self.dictionaries = dictionaries
        
    def run(self):
        try:
            sleep(10)
            self.db.turtle.insert_many(self.dictionaries)
        except:
            print("Error trying to save the document to MongoDB:", sys.exc_info()[0])
            sys.exit()
            
class MongoLoader(object):
    
    def __init__(self):
        config = Config()
        try:
            dbName = config.get('mongo','name')
        except:
            print("Error reading property from configuration file: ", sys.exc_info()[0])
            sys.exit()
        
        mongo_host = config.get('mongo','host')
        mongo_port = int(config.get('mongo','port'))
        client = MongoClient(host=mongo_host, port=mongo_port)
        self.db = client[dbName]
        
    def savePrefixs(self,prefixs):
        self.db.prefix.insert_one(prefixs)
    
    def loadTuplesToMongo(self,rdfDict):
        sys.stdout.write("Number of threads: " + str(threading.active_count())+"\r")
        sys.stdout.flush()
        thread = MongoWriterThread(self.db,rdfDict)
        try:
            thread.start()
        except threading.ThreadError as e:
            if str(e) == "can't start new thread":
                actualThreadActiveCount = threading.activeCount()
                while threading.activeCount() >= actualThreadActiveCount:
                    print "Waiting a few seconds before trying again"
                    sleep(7)
                
                return self.loadTuplesToMongo(rdfDict)
            else:
                raise
        return thread