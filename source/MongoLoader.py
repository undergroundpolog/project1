'''
Created on 27 ago. 2017

@author: alejandro
'''

from pymongo import MongoClient
from fileutils.Config import Config
import threading
import sys
from time import sleep

'''
# MongoWriterThread
#
# Writes several documents in a thread. The documents will be stored in a collection called turtle
#
'''
class MongoWriterThread(threading.Thread):
    def __init__(self,db,dictionaries):
        threading.Thread.__init__(self)
        self.db = db
        self.dictionaries = dictionaries
        self.cache = {}
        
    def run(self):
        try:
            self.db.turtle.insert_many(self.dictionaries)
            pass
        except:
            print("Error trying to save the document to MongoDB:", sys.exc_info()[0])
            sys.exit()
 
'''
# MongoWriterHugeDocumentThread
#
# Build huge documents avoiding circular relations. The documents will be stored in a collection called turtlehu
#
'''        
class MongoWriterHugeDocumentThread(threading.Thread):
    def __init__(self,db,sourceIds):
        self.db = db
        self.sourceIds = sourceIds
        threading.Thread.__init__(self)
        
    def buildHugeDocument(self,document,objectsSeen):
        if type(document) is dict:
            for key in document:
                if key <> 'source':
                    document[key] = self.buildHugeDocument(document[key],objectsSeen)
                
        elif type(document) is list:
            for i in range(0,len(document)):
                document[i] = self.buildHugeDocument(document[i],objectsSeen)
        else:
            if type(document) is unicode:
                document = document.encode('utf-8')

            if document not in objectsSeen and not str(document).startswith('ns2') :
                sourceInfo = self.db.turtle.find_one({'source' : document})
                if sourceInfo != None:
                    objectsSeen
                    x = objectsSeen
                    x.append(document)
                    tmpDocument = document
                    document = self.buildHugeDocument(sourceInfo['semantic'],x)
                    x.remove(tmpDocument)
        return document
    
    def run(self):
        for sourceId in self.sourceIds:
            sourceInfo = self.db.turtle.find_one({'source' : sourceId})
            del sourceInfo['_id']
            hugeDocument = self.buildHugeDocument(sourceInfo,[])
            self.db.turtlehu.insert_one(hugeDocument)

    
'''
# MongoLoader
#
# Main class. Play as father at the moment of thread creation for writing to mongo
#
'''  
class MongoLoader(object):
    STRATEGY_MONGOWRITER = 1
    STRATEGY_MONGOWRITERHUGEDOCUMENT = 2
    
    def __init__(self):
        self.config = Config()
        try:
            dbName = self.config.get('mongo','name')
        except:
            print("Error reading property from configuration file: ", sys.exc_info()[0])
            sys.exit()
        
        mongo_host = self.config.get('mongo','host')
        mongo_port = int(self.config.get('mongo','port'))
        client = MongoClient(host=mongo_host, port=mongo_port)
        self.db = client[dbName]
        self.db.turtle.create_index('source')
        
    def savePrefixs(self,prefixs):
        self.db.prefix.insert_one(prefixs)
        pass
    
    def loadTuplesToMongo(self,rdfDict,strategy):
        sys.stdout.write("Number of threads: " + str(threading.active_count())+"\r")
        sys.stdout.flush()
        if strategy == self.STRATEGY_MONGOWRITER:
            thread = MongoWriterThread(self.db,rdfDict)
        elif strategy == self.STRATEGY_MONGOWRITERHUGEDOCUMENT:
            thread = MongoWriterHugeDocumentThread(self.db,rdfDict)
        else:
            raise
        try:
            thread.start()
        except threading.ThreadError as e:
            if str(e) == "can't start new thread":
                actualThreadActiveCount = threading.activeCount()
                while threading.activeCount() >= actualThreadActiveCount:
                    print "Waiting a few seconds before trying again"
                    sleep(7)
                
                return self.loadTuplesToMongo(rdfDict,strategy)
            else:
                raise
        return thread
    
    def createHugeDocuments(self,sourceIds):
        batchSourceIds = []
        batchSize = int(self.config.get('basic','batch_size'))
        i = 0
        for sourceId in sourceIds:
            batchSourceIds.append(sourceId)
            if i >= batchSize:
                self.loadTuplesToMongo(batchSourceIds, self.STRATEGY_MONGOWRITERHUGEDOCUMENT)
                i = 0
            i += 1
                
        self.loadTuplesToMongo(batchSourceIds, self.STRATEGY_MONGOWRITERHUGEDOCUMENT)
        
            
