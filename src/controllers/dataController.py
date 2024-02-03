from typing import List
import os, sys
import os.path as path

from src.reader import readMainFile, readPingData
from src.writer import writeMainFile, writePingData
from src import PingData

class DataController:
    mainFilePath : str
    pingDataFilePaths : List[str] # This is a list complete paths, not just file names.
    pingDatas : List[PingData]

    def __init__(self) -> None:
        self.mainFilePath = DataController._getMainFileLocation()
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
        count = len(self.pingDatas)+1
        filePath = path.join(path.dirname(self.mainFilePath), "pingData" + str(len(self.pingDatas)+1) + ".json")
        while filePath in self.pingDataFilePaths:
            count += 1
            filePath = path.join(path.dirname(self.mainFilePath), "pingData" + str(count) + ".json")
        filePath = path.join(path.dirname(self.mainFilePath), "pingData" + str(len(self.pingDatas)+1) + ".json")
        newPingData = PingData.getNew(filePath)
        self.pingDatas.append(newPingData)
        writePingData(newPingData)
        self.pingDataFilePaths.append(filePath)
        self.writeMainFile()

    def removePingStater(self, pingData : PingData):
        self.pingDatas.remove(pingData)
        self.pingDataFilePaths.remove(pingData.filePath)
        self.writeMainFile()
        os.remove(pingData.filePath)

    def changePingDataOrder(self, pingDataFilePaths : List[str]):
        self.pingDataFilePaths = pingDataFilePaths
        self.writeMainFile()

    @classmethod
    def _getMainFileLocation(self):
        """
        This is not a getter but instead is used to generate the default location for the main file during initialization.
        """
        if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader extends the sys module by a flag frozen=True and sets the app path into variable _MEIPASS'. (Taken from stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741)
            dir_path = sys._MEIPASS
        else:
            dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        return os.path.join(dir_path, "saves", "main.json")