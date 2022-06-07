class History(object):

    def __init__(self):
        self.items = []
        self.image = None

    @classmethod
    def fromImage(cls, image):
        history = History()
        history.image = image 
        i = 1
        key = "history{0:4}".format(i)
        item = image.getProp(key)
        while item:
            history.add(item)
            i = i + 1
            key = "history{0:4}".format(i)
            item = image.getProp(key)
        return history
    
    def add(self, item):
        if not self.image:
            return
        key = "history{0:4}".format(len(self.items)+1)
        self.image.setProp(key, item)           
        self.items.append(item)
        
    def addAll(self, items):
        for item in items:
            self.add(item)
    
    def asText(self):
        return '\n'.join(str(i) + ' ' + j for i, j in enumerate(self.items, 1))
        

        