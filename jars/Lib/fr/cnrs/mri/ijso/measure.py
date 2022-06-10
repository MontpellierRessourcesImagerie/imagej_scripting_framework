from ij.measure import ResultsTable

class Measurements(object):
    
    def __init__(self):
        self.headings = []
        self.labels = []
        self.values = {}
        
    @classmethod
    def fromResultsTable(cls, name):
        measurements = Measurements()
        table = ResultsTable.getResultsTable(name)
        if not table:
            return
        measurements.headings = list(table.getHeadings())
        for heading in measurements.headings:
            if heading=="Label":
                measurements.labels = list(table.getColumnAsStrings(heading))
                continue
            measurements.values[heading] = list(table.getColumn(heading))
        if len(measurements.labels)>0:
            measurements.headings = measurements.headings[1:]
        return measurements
        
    @classmethod
    def fromSystemResultsTable(cls):
        return Measurements.fromResultsTable("Results")
        
    def numberOfValues(self):
        return len(self.values)
        
    def numberOfVariables(self):
        return len(self.headings)
   
    def getLabels(self):
        return self.labels
        
    def getHeadings(self):
        return self.headings
        
    def getVariable(self, name):
        return self.values["name"]
        
    def save(self, path):
        with open(path, 'w') as f:
            f.write(self.asString(separator=","))
    
    def isEmpty(self):
        return len(self.values)==0 
       
    def asString(self, separator="\t"):
        text = ""
        matrix = []
        keys = self.values.keys()
        for key in keys:
            matrix.append(self.values[key])
        matrix = zip(*matrix)
        matrix = [keys] + matrix
        text = text + separator + separator.join(matrix[0]) + "\n"
        for count, row in enumerate(matrix[1:], start=1):
            textRow = [str(elem) for elem in row]
            text = text + str(count) + separator + separator.join(textRow) + "\n"
        return text