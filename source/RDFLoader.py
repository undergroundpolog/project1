'''
Created on 27 ago. 2017

@author: alejandro
'''

from MongoLoader import MongoLoader
from Parser import Parser
import time

class RDFLoader(object):
    '''
    classdocs
    '''

    def __init__(self):
        print time.strftime("%c")
        parser = Parser();
        mongoLoader = MongoLoader();
        batchCount = 1
        threads = []
        while True:
            rdfLoader = parser.getDictionaries()
            
            if rdfLoader == None:
                break
            
            batchCount += 1
            thread = mongoLoader.loadTuplesToMongo(rdfLoader)
            threads.append(thread)
            
        for thread in threads:
            thread.join()
        print time.strftime("%c")    
    
        