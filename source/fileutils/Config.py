'''
Created on 29 ago. 2017

@author: alejandro
'''

import ConfigParser

class Config(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('project1.cfg')
        
    def get(self,section,key):
        return self.config.get(section, key)
        