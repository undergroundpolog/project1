'''
Created on 27 ago. 2017

@author: alejandro
'''

from fileutils.TurtleReader import TurtleReader

class Parser(object):

    def __init__(self):
        print 'inside Parser'
        turtleReader = TurtleReader()
        print turtleReader.getPrefixs()
        print turtleReader.getNextTupleSet()
    
    def getDictionary(self):
        """
        A B C
        A X 1
        A X 2
        C F H
        H K 1
        """
        
        dictRdf = {
            'A' : {
                'B' : 'C',
                'X' : [1,2]
            },
            'C' : {
                'F' : 'H'
            },
            'H' : {
                'K' : 1    
            }
        }

        return dictRdf