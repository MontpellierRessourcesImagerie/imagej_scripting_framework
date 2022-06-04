import time
from java.awt.event import ItemListener
from ij import IJ
from ij.gui import GenericDialog
from ij.plugin.tool import MacroToolRunner
from java.beans import PropertyChangeListener
from fr.cnrs.mri.ijso.operations import Operation

class GenericTool(PropertyChangeListener, MacroToolRunner, ItemListener):
    
    def __init__(self):
        MacroToolRunner.__init__(self, None)
        self.progress = 0
        self.dialog = None
        self.dialogsRead = 0
         
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
            self.dialogsRead = 0
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
        self.dialog = dialog
        self.addOptionsToDialog(options, dialog)
        choices = dialog.getChoices()
        if choices:
            for choice in choices:
                choice.addItemListener(self)
        dialog.showDialog()
        if dialog.wasCanceled() or self.dialogsRead > 0:
            return
        self.dialogsRead = 1
        self.getOptionValuesFromDialog(options, dialog)
        self.dialog = None
        
    def addOptionsToDialog(self, options, dialog):
        for option in options:
            if option.isChoiceType() and issubclass(option.getValue().__class__, Operation):
                self.addOptionToDialog(option, dialog)
                self.addOptionsToDialog(option.getValue().getOptions(), dialog)
                if option.getValue().getOptions().length > 0:
                    dialog.addMessage(" ")
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
            
    def getOptionValuesFromDialog(self, options, dialog):
        for option in options:
            if option.isChoiceType() and issubclass(option.getValue().__class__, Operation):
                self.getOptionFromDialog(option, dialog)
                if option.getValue().getOptions().length() > 0:
                    self.getOptionValuesFromDialog(option.getValue().getOptions(), dialog)
                continue
            self.getOptionFromDialog(option, dialog)
                        
    def getOptionFromDialog(self, option, dialog):
        if option.isStringType():
            option.setValue(dialog.getNextString())
        if option.isIntType() or option.isFloatType():
            option.setValue(dialog.getNextNumber())
        if option.isBoolType():
            option.setValue(dialog.getNextBoolean())
        if option.isChoiceType():
            index = dialog.getNextChoiceIndex()
            option.setValue(option.getItems()[index])
        
    def itemStateChanged(self, e):
        choice = e.getSource()
        choices = self.dialog.getChoices()
        choiceIndex = 0
        for aChoice in choices:
            if aChoice is choice:
                break
            choiceIndex = choiceIndex + 1
        options = self.operation.getOptions()
        optionIndex = 0
        for option in options:
            if option.isChoiceType() and optionIndex == choiceIndex:
                option.setValue(option.getItems()[choice.getSelectedIndex()])
                break
            optionIndex = optionIndex + 1
        self.dialog.dispose()
        self.showOptionsDialog()
    
    def runTool(self):
        pass

