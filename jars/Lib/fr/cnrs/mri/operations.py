import time
from java.beans import PropertyChangeSupport
from java.lang import Thread

class Operation(Thread):

    def __init__(self):
        self.support = PropertyChangeSupport(self)
        self.status = ""
        self.progress = 0
        self.startTime = 0
        self.endTime = 0
        self.options = Options()
        
    def run(self):
        self.setStartTime(time.time())
        self.execute()
        self.setEndTime(time.time())
        
    def execute(self):
        pass
    
    def getName(self):
        pass
                    
    def addPropertyChangeListener(self, pcl):
        self.support.addPropertyChangeListener(pcl)

    def removePropertyChangeListener(self, pcl):
        self.support.removePropertyChangeListener(pcl)

    def setStatus(self, status):
        self.support.firePropertyChange("status", self.status, status)
        self.status = status
        
    def getStatus(self):
        return self.status
        
    def setProgress(self, progress):
        self.support.firePropertyChange("progress", self.progress, progress)
        self.progress = progress
        
    def getProgress(self):
        return self.progress
        
    def setStartTime(self, startTime):
        self.support.firePropertyChange("startTime", self.startTime, startTime)
        self.startTime = startTime
        
    def getStartTime(self):
        return self.startTime
    
    def getEndTime(self):
        return self.endTime    
    
    def setEndTime(self, endTime):
        self.support.firePropertyChange("endTime", self.endTime, endTime)
        self.endTime = endTime            

                
class Option(object):
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value
    
    def isStringType(self):
        return False

    def isIntType(self):
        return False                                

    def isFloatType(self):
        return False
        
        
class StringOption(Option):

    def __init__(self, name, value):
        Option.__init__(name, str(value))
        
    def isStringType(self):
        return True


class IntOption(Option):

    def __init__(self, name, value):
        Option.__init__(name, int(value))
        
    def isIntType(self):
        return True
              

class FloatOption(Option):

    def __init__(self, name, value):
        Option.__init__(name, float(value))
        
    def isFloatType(self):
        return True


class ChoiceOption(Option):

    def __init__(self, name, value, items):
        Options__init__(name, value)
        self.items = items

                
class Options(object):
    
    def __init__(self):
        self.options = {}
        
    def add(self, anOption):
        self.options[anOption.getName()] = anOption
        
        