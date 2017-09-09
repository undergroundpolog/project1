'''
Created on 27 ago. 2017

@author: alejandro
'''

from pymongo import MongoClient
from fileutils.Config import Config
import sys

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
        for rdfDoc in rdfDict:
            print 'Trying to save data'
            try:
                self.__db.turtle.insert_one(rdfDoc) 
            except:
                print("Error trying to save the document to MongoDB:", sys.exc_info()[0])
                sys.exit()