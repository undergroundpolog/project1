'''
Created on 3 sept. 2017

@author: alejandro
'''
import sys

class StateMachine(object):

    def __init__(self):
        self.turtleAsDict = {}
        self.index = 0
        self.lastSeen = None
        self.subject = None
    
    def initState(self,turtleAsList):
        try:
            self.turtleAsDict = {}
            self.index = 0
            key = turtleAsList[self.index]
            key = key.replace('.','\uff0E')
            self.turtleAsDict['source'] = key
            self.turtleAsDict['semantic'] = {}
            self.lastSeen = key
            self.subject = key
            self.index += 1
            
            #state transition
            self.predicateState(turtleAsList)
        except:
            print("Error creating dictionary for object "+self.subject, sys.exc_info()[0])
            raise
            sys.exit()
        
        return self.turtleAsDict
        
    def predicateState(self,turtleAsList):
        self.lastSeen = turtleAsList[self.index]
        self.turtleAsDict['semantic'][self.lastSeen] = None
        self.index += 1
        
        #state transition
        self.objectState(turtleAsList)
        
    def objectState(self, turtleAsList):
        while True:
            self.__token = turtleAsList[self.index + 1]
            if self.__token == ',':
                if self.turtleAsDict['semantic'][self.lastSeen] == None:
                    self.turtleAsDict['semantic'][self.lastSeen] = [turtleAsList[self.index]]
                else:
                    self.turtleAsDict['semantic'][self.lastSeen].append(turtleAsList[self.index])
                    
                self.index += 2
                
                #state transition
                #self.objectState(turtleAsList)
                continue
                
            else:
                if self.turtleAsDict['semantic'][self.lastSeen] == None:
                    self.turtleAsDict['semantic'][self.lastSeen] = turtleAsList[self.index]
                else:
                    self.turtleAsDict['semantic'][self.lastSeen].append(turtleAsList[self.index])
                self.index += 2
                
            if self.__token == ';':
                self.predicateState(turtleAsList)
                
            break

        
        
        
        
        
        