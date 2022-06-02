import time
from ij import IJ
from ij.gui import GenericDialog
from ij.plugin.tool import MacroToolRunner
from java.beans import PropertyChangeListener
from fr.cnrs.mri.ijso.operations import Operation

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
        options = self.operation.getOptions()
        name = self.getToolName()
        name = name.replace("Action Tool", "Options")
        dialog = GenericDialog(name)
        self.addOptionsToDialog(options, dialog)
        dialog.showDialog()
        if dialog.wasCanceled():
            return

    def addOptionsToDialog(self, options, dialog):
        for option in options:
            if option.isChoiceType() and issubclass(option.getValue().__class__, Operation):
                self.addOptionToDialog(option, dialog)
                self.addOptionsToDialog(option.getValue().getOptions(), dialog)
                continue
            self.addOptionToDialog(option, dialog)
    
    def addOptionToDialog(self, option, dialog):
        label = option.getName() + ": "
        value = option.getValue()
        if option.isStringType():
            dialog.addStringField(label, value)
        if option.isIntType() or option.isFloatType():
            dialog.addNumericField(label, value)
        if option.isBoolType():
            dialog.addCheckbox(label, value)
        if option.isChoiceType():
            if issubclass(value.__class__, Operation):
                value = value.getOpName()         
            dialog.addChoice(label, option.getItemsAsStrings(), value)     
            
                    
    def runTool(self):
        pass

        