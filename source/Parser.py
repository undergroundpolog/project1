'''
Created on 27 ago. 2017

@author: alejandro
'''

from fileutils.TurtleReader import TurtleReader


class Parser(object):

    def __init__(self):
        self.turtleReader = TurtleReader()
        
        #just for testing
        self.turtleReader.getPrefixs()
        
    def getDictionaries(self):
        dictInfo = self.turtleReader.getNextTupleSet()
        return dictInfo
    
    def getPrefixs(self):
        return self.turtleReader.getPrefixs()
    