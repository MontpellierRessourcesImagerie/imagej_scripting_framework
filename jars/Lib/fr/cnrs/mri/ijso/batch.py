import os
from ij import IJ
from fr.cnrs.mri.ijso.operations import Operation


class BatchProcessor(Operation):

    def __init__(self):
        Operation.__init__(self)
        self.operations = []
        self.inputImages = []
        self.fileExtensions = []
        self.saveInInputFolder = False
        self.outputFolders = [] 
        self.saveResultsTablePerImage = False
        self.saveResultsTable = False
        
    def setSaveResultsTablePerImage(self):
        self.saveResultsTablePerImage = True
    
    def resetSaveResultsTablePerImage(self):
        self.saveResultsTablePerImage = False
    
    def setSaveResultsTable(self):
        self.saveResultsTable = True
    
    def resetSaveResultsTable(self):
        self.saveResultsTable = False
                
    def setSaveResultsTable(self):
        self.saveResultsTable = True
        
    def addOutputFolder(self, folder):
        self.outputFolders.append(folder)
    
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
            if not os.path.isfile(aFile):
                continue
            filteredImages.append(aFile) 
        return filteredImages
    
    def filterByExtension(self, images):
        if len(self.fileExtensions)<1:
            return images
        filteredImages = []
        for aFile in images:
            ext = os.path.splitext(aFile)[1]
            if not ext in self.fileExtensions:
                continue
            filteredImages.append(aFile) 
        return filteredImages        
    
    def addImagesInFolder(self, aFolder):
        files = [os.path.join(aFolder, aFile) for aFile in os.listdir(aFolder)]
        images = self.filterImages(files)
        self.inputImages.extend(images)
    
    def addExtension(self, ext):
        self.fileExtensions.append(ext)

    def execute(self):
        number = len(self.inputImages)
        for count, path in enumerate(self.inputImages, start=1):
            image = IJ.openImage(path)
            for operation in self.operations:
                operation.setInputImage(image)
                self.setStatus("Processing image {} of {}".format(count, number))
                self.operation.run()
                image = operation.getResultImage()
            self.save(image, os.path.dirname(path), os.path.basename(path))
            if self.saveResultsTablePerImage:
                self.saveResults(self.operations[-1].getMeasurements(), os.path.dirname(path), os.path.basename(path))
        if self.saveResultsTable:
            self.saveResults(self.operations[-1].getMeasurements(), os.path.dirname(path), "Results.csv")              
            
    def save(self, image, folder, filename):
        outName = os.path.splitext(filename)[0] + ".tif"
        outputPath = self.getOutputFolderFor(folder)
        IJ.saveAsTiff(image, os.path.join(outPath, outName))
    
    def saveResults(self, measurements, folder, filename):
        outName = os.path.splitext(filename)[0] + ".csv"
        outputPath = self.getOutputFolderFor(folder)
        measurements.save(os.path.join(outPath, outName))
    
    def getOutputFolderFor(self, folder):
        outPath = ""
        if self.saveInInputFolder and len(self.outputFolders) < 1:
            outPath = folder
        if self.saveInInputFolder and len(self.outputFolders) >= 1:
            outPath = os.path.join(folder, self.outputFolders)
        if not self.saveInInputFolder:
            outPath = self.outputFolders[0]
        return outputPath
        