'''
Created on 27 ago. 2017

@author: alejandro
'''

from fileutils.TurtleReader import TurtleReader


class Parser(object):

    def __init__(self):
        self.__turtleReader = TurtleReader()
        
        #just for testing
        self.__turtleReader.getPrefixs()
        
    def getDictionary(self):
        dictRdf = self.__turtleReader.getNextTupleSet()
        return dictRdf
    