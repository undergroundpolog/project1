'''
Created on 27 ago. 2017

@author: alejandro
'''

from MongoLoader import MongoLoader
from Parser import Parser

class RDFLoader(object):
    
    def __init__(self):
        parser = Parser();
        mongoLoader = MongoLoader();
        batchCount = 1
        threads = []
        prefixs = parser.getPrefixs()
        mongoLoader.savePrefixs(prefixs)
        while True:
            rdfLoader = parser.getDictionaries()
            
            if rdfLoader == None:
                break
            
            batchCount += 1
            thread = mongoLoader.loadTuplesToMongo(rdfLoader)
            threads.append(thread)
            
        for thread in threads:
            thread.join() 
    
        