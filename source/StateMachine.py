'''
Created on 3 sept. 2017

@author: alejandro
'''

class StateMachine(object):

    def __init__(self):
        self.__turtleAsDict = {}
        self.__index = 0
        self.__lastSeen = None
        self.__subject = None
    
    def initState(self,turtleAsList):
        self.__turtleAsDict = {}
        self.__index = 0
        key = turtleAsList[self.__index]
        key = key.replace('.','\uff0E')
        self.__turtleAsDict[key] = {}
        self.__lastSeen = key
        self.__subject = key
        self.__index += 1
        
        
        #state transition
        self.predicateState(turtleAsList)
        
        return self.__turtleAsDict
        
    def predicateState(self,turtleAsList):
        self.__lastSeen = turtleAsList[self.__index]
        self.__turtleAsDict[self.__subject][self.__lastSeen] = None
        self.__index += 1
        
        #state transition
        self.objectState(turtleAsList)
        
    def objectState(self, turtleAsList):
        self.__token = turtleAsList[self.__index + 1]
        if self.__token == ',':
            if self.__turtleAsDict[self.__subject][self.__lastSeen] == None:
                self.__turtleAsDict[self.__subject][self.__lastSeen] = [turtleAsList[self.__index]]
            else:
                self.__turtleAsDict[self.__subject][self.__lastSeen].append(turtleAsList[self.__index])
                
            self.__index += 2
            
            #state transition
            self.objectState(turtleAsList)
            
        else:
            if self.__turtleAsDict[self.__subject][self.__lastSeen] == None:
                self.__turtleAsDict[self.__subject][self.__lastSeen] = turtleAsList[self.__index]
            else:
                self.__turtleAsDict[self.__subject][self.__lastSeen].append(turtleAsList[self.__index])
            self.__index += 2
            
        if self.__token == ';':
            self.predicateState(turtleAsList)

        
        
        
        
        
        