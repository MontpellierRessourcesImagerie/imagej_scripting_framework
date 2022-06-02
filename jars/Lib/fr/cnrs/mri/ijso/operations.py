import time
import re
from java.beans import PropertyChangeSupport
from java.lang import Thread

class Operation(Thread):

    def __init__(self):
        self.support = PropertyChangeSupport(self)
        self.status = ""
        self.progress = 0
        self.startTime = 0
        self.endTime = 0
        self.opName = None
        self.inputImage = None
        self.options = Options()
             
    def setInputImage(self, image):
        self.inputImage = image
    
    def run(self):
        self.setStartTime(time.time())
        self.execute()
        self.setEndTime(time.time())
        
    def execute(self):
        pass
    
    def getOptions(self):
        return self.options
        
    def getOption(self, name):
        return self.getOptions().get(name)        
    
    def addOption(self, anOption):
        self.getOptions().add(anOption)
        
    def getOpName(self):
        if not self.opName:
            self.opName = self.constructOpNameFromClassName()
        return self.opName
                    
    def constructOpNameFromClassName(self):
        classname = type(self).__name__
        name = re.sub(r"(\w)([A-Z])", r"\1 \2", classname)
        return name
        
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
        
    def setStatusAndProgress(self, status, progress):
        self.setStatus(status)
        self.setProgress(progress)
    
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
        
    def isBoolType(self):
        return False
        
    def setValue(self, value):
        self.value = value
        
        
class StringOption(Option):

    def __init__(self, name, value):
        Option.__init__(self, name, str(value))
        
    def isStringType(self):
        return True


class IntOption(Option):

    def __init__(self, name, value):
        Option.__init__(self, name, int(value))
        
    def isIntType(self):
        return True
              

class FloatOption(Option):

    def __init__(self, name, value):
        Option.__init__(self, name, float(value))
        
    def isFloatType(self):
        return True

class BoolOption(Option):
    
    def __init__(self, name, value):
        Option.__init__(self, name, bool(value))
      
    def isBoolType(self):
        return True

class ChoiceOption(Option):

    def __init__(self, name, value, items):
        Option.__init__(self, name, value)
        self.items = items

                
class Options(object):
    
    def __init__(self):
        self.options = {}
        
    def add(self, anOption):
        self.options[anOption.getName()] = anOption
        
    def get(self, name):
        return self.options[name]
        
    def getOptionNames(self):
        return self.options.keys()
        
    def getOptionNumber(self, i):
        return self.options[self.getOptionNames()[i]]
    
    def length(self):
        return len(self.options)
    
    def __iter__(self):
       return OptionsIterator(self)
       
       
class OptionsIterator:

   def __init__(self, options):
       self.options = options
       self.index = 0
   
   def __next__(self):
       if self._index < options.length():
           result = self.options.getOptionNumber(index)
           self.index = self.index + 1
           return result
       raise StopIteration