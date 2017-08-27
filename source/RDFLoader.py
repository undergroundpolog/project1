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
        rdfLoader = parser.getDictionary()
        mongoLoader = MongoLoader();
        mongoLoader.loadTuplesToMongo(rdfLoader)
    
        