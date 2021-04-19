from os import path

class FilePublisher:
    def __init__(self, inputPath:str, outputPath:str):
        self.inputPath = self.pathCheck(inputPath)
        self.outputPath = self.pathCheck(outputPath)
        self.inputFile= open(self.inputPath,"a")
        self.outputFile= open(self.outputPath,"a")

    def append(self, inputLog:str, outputTag:str):
        self.inputFile.write(inputLog.strip("\n") + "\n")
        self.inputFile.flush()
        self.outputFile.write(outputTag.strip("\n") + "\n")
        self.outputFile.flush()

    def pathCheck(self, strPath:str) -> bool:
        if path.exists(strPath):
            return strPath
        else:
            raise FileNotFoundError("The path passed or the directory does not exists: " + path +
                                    "\nPlease check if the path is correct.") 
