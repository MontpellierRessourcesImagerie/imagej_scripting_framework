from ij import IJ
import re

class IJCP(object):
    instance = None
    
    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance
    
    def __getattr__(self, name):
            def method(*args, **kwargs):  
                newName = name
                if name.startswith('_'):
                    newName = name[1:]
                newName = newName.replace('__', '-')
                parts = re.findall('[\-0-9a-zA-Z][^A-Z]*', newName)           
                parts[0] = parts[0].capitalize()
                command = ' '.join(parts)
                if len(kwargs)>0:
                    if not (len(kwargs)==1 and list(kwargs.keys())[0]=="stack") and not command=="Convert To Mask":
                        command = command + "..."   
                command = command.replace(" To ", " to ")                      
                image = args[0]
                options = ""
                for key, value in kwargs.items():
                    if isinstance(value, bool):
                        if value:
                            options = options + key + " "
                        continue
                    options = options + key + "=" + str(value) + " "
                print('IJ.run(imp, ' + '"' + command + '", ' + '"' + options + '")')
                IJ.run(image, command, options)
            return method

def test():
    image = IJ.openImage("http://imagej.nih.gov/ij/images/blobs.gif");
    ij = IJCP.getInstance()                        
    ij.invert(image)
    ij.invert(image, stack = True)
    ij._8__bit(image)
    ij.gaussianBlur(image, sigma=2)
    IJ.setAutoThreshold(image, "Default");
    ij.analyzeParticles(image, show="Overlay", include = True, add = True)
    

