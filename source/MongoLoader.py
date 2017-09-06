'''
Created on 27 ago. 2017

@author: alejandro
'''

from pymongo import MongoClient
from fileutils.Config import Config

class MongoLoader(object):
    '''
    classdocs
    '''

    def __init__(self):
        config = Config()
        dbName = config.get('mongo','name')
        
        client = MongoClient()
        self.__db = client[dbName]
    
    def loadTuplesToMongo(self,rdfDict):
        for rdfDoc in rdfDict:
            self.__db.turtle.insert_one(rdfDoc) 