from pygtail import Pygtail
import os.path
from os import path

class FilePoller:
    def __init__(self, filePath: str):
        self.filePath = filePath
        if path.exists(self.filePath):
            self.poller = Pygtail(self.filePath)
        else:
            raise FileNotFoundError("The log path passed or the directory does not exists: " + self.getFilePath() +
                                    "\nPlease check if the path is correct")

    def poll(self) -> Pygtail:
        return self.poller
    
    def getFilePath(self) -> str:
        return self.filePath
