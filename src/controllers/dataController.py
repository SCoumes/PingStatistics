from typing import List
import os
import os.path as path

from src.reader import readMainFile, readPingData
from src.writer import writeMainFile, writePingData
from src import PingData

class DataController:
    mainFilePath : str
    pingDataFilePaths : List[str] # This is a list complete paths, not just file names.
    pingDatas : List[PingData]

    def __init__(self) -> None:
        self.mainFilePath = "test/testFiles/main.json"
        readMainFile(self.mainFilePath, self) # This has side effects and will define the pingDataFilePaths attribute.
        self.pingDatas = [readPingData(FilePath) for FilePath in self.pingDataFilePaths]

    def getPingDatas(self):
        return self.pingDatas
    
    def writeAllData(self):
        self.writeMainFile()
        self.writePingDatas()

    def writeMainFile(self):
        writeMainFile(self.mainFilePath, self.pingDataFilePaths)
    
    def writePingDatas(self):
        for pingData in self.pingDatas:
            writePingData(pingData)

    def addNewPingStater(self):
        FilePath = path.join(path.dirname(self.mainFilePath), "pingData" + str(len(self.pingDatas)+1) + ".json")
        newPingData = PingData.getNew(FilePath)
        self.pingDatas.append(newPingData)
        writePingData(newPingData)
        self.pingDataFilePaths.append(FilePath)
        self.writeMainFile()

    def removePingStater(self, pingData : PingData):
        self.pingDatas.remove(pingData)
        self.pingDataFilePaths.remove(pingData.filePath)
        self.writeMainFile()
        os.remove(pingData.filePath)