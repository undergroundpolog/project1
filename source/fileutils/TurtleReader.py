'''
Created on 29 ago. 2017

@author: alejandro
'''

from StateMachine import StateMachine
from Config import Config
import re, sys

class TurtleReader(object):

    def __init__(self):
        #initializing state machine
        self.stateMachine = StateMachine()
        
        config = Config()
        try:
            self.ttlFile = config.get('basic', 'ttl_file')
            self.batchSize = int(config.get('basic','batch_size'))
        except:
            print("Error reading property from configuration file:", sys.exc_info())
            sys.exit()
        
        #class vars
        # TODO check how to do it better
        self.prefix = {}
        self.index = 0
        self.prefixPattern = re.compile(r'^@.+\.$')
        self.endOfEntryPattern = re.compile(r'\.\s*$')
        self.entryParser = re.compile(r'".+"@?\w{2} |".+" |\S+')
        
        #preparations
        self.__exploreFile()
        self.__retrievePrefixs()

    """
    Explore the whole file and store the offset for each line
    """
    def __exploreFile(self):
        self.file = open(self.ttlFile,"r",0)
        self.line_offset = []
        offset = 0
        for line in self.file:
            self.line_offset.append(offset)
            offset += len(line)
        
        self.file.seek(0)
        
    """
    Read the prefixs from the TTL file
    """
    def __retrievePrefixs(self):
        aliasPattern = re.compile(r' .+: ')
        iriPattern = re.compile(r'<.+>')
        
        for line in self.file:
            if self.prefixPattern.match(line) != None:
                alias = aliasPattern.search(line).group().strip()
                alias = alias.replace(':','')
                iri = iriPattern.search(line).group().strip()
                self.prefix[alias] = iri
                self.index += 1
            else:
                break
                    
    """
    Returns the prefix used in the turtle set
    """
    def getPrefixs(self):
        return self.prefix
    
    """
    Returns the next set of RDF tuples read from the file
    """
    def getNextTupleSet(self):
        tuples = []
        sourceIds = []
        
        if self.index >= len(self.line_offset):
            return None
        
        self.file.seek(
            self.line_offset[self.index])
        
        # TODO : parse in batch!!!
        entrySoFar = ''
        batchIndex = 0
        for line in self.file:
            if batchIndex >= self.batchSize:
                break
            
            entrySoFar += line
            self.index += 1
            if self.endOfEntryPattern.search(line) != None:
                entrySoFarAsList = self.entryParser.findall(entrySoFar) 
                
                entrySoFarAsDict = self.stateMachine.initState(entrySoFarAsList)
                if entrySoFarAsDict['source'].startswith('ns2'):
                    sourceIds.append(entrySoFarAsDict['source'])
                
                
                tuples.append(entrySoFarAsDict)
                
                entrySoFar = ''
                batchIndex += 1
                
        dictInfo = {}
        dictInfo['tuples'] = tuples
        dictInfo['source_ids'] = sourceIds
        return dictInfo
    