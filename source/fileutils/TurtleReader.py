'''
Created on 29 ago. 2017

@author: alejandro
'''

from StateMachine import StateMachine
from Config import Config
import re

class TurtleReader(object):

    def __init__(self):
        #initializing state machine
        self.__stateMachine = StateMachine()
        
        config = Config()
        self.__ttlFile = config.get('basic', 'ttl_file')
        self.__batchSize = int(config.get('basic','batch_size'))
        
        #class vars
        # TODO check how to do it better
        self.__prefix = {}
        self.__index = 0
        self.__prefixPattern = re.compile(r'^@.+\.$')
        self.__endOfEntryPattern = re.compile(r'\.\s*$')
        self.__entryParser = re.compile(r'".+"@?\w{2} |".+" |\S+')
        
        #preparations
        self.__exploreFile()
        self.__retrievePrefixs()

    """
    Explore the whole file and store the offset for each line
    """
    def __exploreFile(self):
        self.__file = open(self.__ttlFile,"r",0)
        self.__line_offset = []
        offset = 0
        for line in self.__file:
            self.__line_offset.append(offset)
            offset += len(line)
        
        self.__file.seek(0)
        
    """
    Read the prefixs from the TTL file
    """
    def __retrievePrefixs(self):
        aliasPattern = re.compile(r' .+: ')
        iriPattern = re.compile(r'<.+>')
        
        for line in self.__file:
            if self.__prefixPattern.match(line) != None:
                alias = aliasPattern.search(line).group().strip()
                iri = iriPattern.search(line).group().strip()
                self.__prefix[alias] = iri
                self.__index += 1
            else:
                break
                    
    """
    Returns the prefix used in the turtle set
    """
    def getPrefixs(self):
        return self.__prefix
    
    """
    Returns the next set of RDF tuples read from the file
    """
    def getNextTupleSet(self):
        tuples = []
        
        if self.__index >= len(self.__line_offset):
            return None
        
        self.__file.seek(
            self.__line_offset[self.__index])
        
        # TODO : parse in batch!!!
        entrySoFar = ''
        batchIndex = 0
        for line in self.__file:
            if batchIndex >= self.__batchSize:
                break
            
            entrySoFar += line
            self.__index += 1
            if self.__endOfEntryPattern.search(line) != None:
                entrySoFarAsList = self.__entryParser.findall(entrySoFar) 
                
                print entrySoFarAsList
                entrySoFarAsDict = self.__stateMachine.initState(entrySoFarAsList)
                print entrySoFarAsDict
                
                
                tuples.append(entrySoFarAsDict)
                
                entrySoFar = ''
                batchIndex += 1
                
        return tuples