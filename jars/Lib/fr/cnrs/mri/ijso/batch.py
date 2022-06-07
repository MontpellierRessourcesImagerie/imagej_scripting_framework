import os
from operations import Operation

class BatchProcessor(Operation):

    def __init__(self):
        self.operations = []
        self.inputImages = []
        self.fileExtensions = []
        self.saveInInputFolder = False
        self.outputFolders = [] 
        
    def setSaveInInputFolder(self):
        saveInInputFolder = True
    
    def resetSaveInInputFolder(self):
        saveInInputFolder = False
            
    def addOperation(self, anOperation):
        self.operations.append(anOperation)
        
    def addImages(self, images):
        images = self.filterImages(images)
        self.inputImages.extend(images)
        
    def filterImages(self, images):
        filteredImages = self.filterFiles(images)
        filteredImages = self.filterByExtension(filteredImages)
        return filteredImages
        
    def filterFiles(self, images):
        filteredImages = []
        for aFile in images:
            if not os.path.isfile(aFile)
                continue
            filteredImages.append(aFile) 
        return filteredImages
    
    def filterByExtension(self, images):
        if len(self.fileExtensions)<1:
            return images
        filteredImages = []
        for aFile in images:
            ext = os.path.splitext(aFile)[1]
            if not ext in self.fileExtensions
                continue
            filteredImages.append(aFile) 
        return filteredImages        
    
    def addImagesInFolder(self, aFolder):
        files = os.listdir(aFolder)
        images = self.filterImages(files)
        self.inputImages.extend(images)
    
    def addExtension(self, ext):
        self.fileExtensions.append(ext)

    def execute(self):
        pass