import time
from ij import IJ
from ij.plugin.tool import MacroToolRunner
from java.beans import PropertyChangeListener

class GenericTool(PropertyChangeListener, MacroToolRunner):
    
    def __init__(self):
        MacroToolRunner.__init__(self, None)
        self.progress = 0
    
    def setToolName(self, aName):
        self.name = aName
           
    def setToolIcon(self, anIcon):
        self.icon = anIcon
          
    def getToolIcon(self):
        return self.icon        

    def getToolName(self):
        return self.name    
    
    def runMacroTool(self, name):
        if name.endswith("Options"):
            self.showOptionsDialog()
            return
        self.runTool()
     
    def propertyChange(self, evt): 
        if evt.getPropertyName()=="progress":
            self.progress = evt.getNewValue()
        if evt.getPropertyName()=="status":
            IJ.log(evt.getNewValue() + " (" + str(self.progress) +")")
        if evt.getPropertyName()=="startTime" or evt.getPropertyName()=="endTime":
            IJ.log(time.ctime(evt.getNewValue()))
            
    def showOptionsDialog(self):
        pass
        
    def runTool(self):
        pass

        