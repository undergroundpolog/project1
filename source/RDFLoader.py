'''
Created on 27 ago. 2017

@author: alejandro
'''

from MongoLoader import MongoLoader
from Parser import Parser

class RDFLoader(object):
    '''
    classdocs
    '''

    def __init__(self):
        parser = Parser();
        mongoLoader = MongoLoader();
        batchCount = 1
        while True:
            rdfLoader = parser.getDictionary()
            
            if rdfLoader == None:
                break
            
            batchCount += 1
            mongoLoader.loadTuplesToMongo(rdfLoader)
            
    
        