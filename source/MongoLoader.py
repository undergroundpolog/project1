'''
Created on 27 ago. 2017

@author: alejandro
'''

from pymongo import MongoClient
from fileutils.Config import Config
import threading
import sys


class MongoWriterThread(threading.Thread):
    
    def __init__(self,db,dictionaries):
        threading.Thread.__init__(self)
        self.__db = db
        self.__dictionaries = dictionaries
        
    def run(self):
        try:
            self.__db.turtle.insert_many(self.__dictionaries)
        except:
            print("Error trying to save the document to MongoDB:", sys.exc_info()[0])
            sys.exit()
            
class MongoLoader(object):
    '''
    classdocs
    '''

    def __init__(self):
        config = Config()
        try:
            dbName = config.get('mongo','name')
        except:
            print("Error reading property from configuration file: ", sys.exc_info()[0])
            sys.exit()
        
        client = MongoClient()
        self.__db = client[dbName]
    
    def loadTuplesToMongo(self,rdfDict):
        print threading.activeCount()
        thread = MongoWriterThread(self.__db,rdfDict)
        thread.start()
        return thread
#     def loadTuplesToMongo(self,rdfDict):
#         try:
#             self.__db.turtle.insert_many(rdfDict)
#         except:
#             print("Error trying to save the document to MongoDB:", sys.exc_info()[0])
#             sys.exit()