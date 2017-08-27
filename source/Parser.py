'''
Created on 27 ago. 2017

@author: alejandro
'''

class Parser(object):
    '''
    classdocs
    '''

    def __init__(self):
        print 'inside Parser'
        '''
        Constructor
        '''
    
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