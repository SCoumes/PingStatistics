from typing import List, Optional
import os, sys
import os.path as path

from PyQt6.QtWidgets import QMessageBox
from src.reader import readMainFile, readPingData, readSettingsFile
from src.writer import writeMainFile, writePingData, writeSettingsFile
from src import PingData

class DataController:
    settingPath : str
    width : int
    height : int
    mainFilePath : Optional[str] # None when a mainfile was never selected.
    pingDataFilePaths : List[str] # This is a list complete paths, not just file names.
    pingDatas : List[PingData]

    def __init__(self) -> None:
        self.settingPath = DataController._getSettingFileLocation()
        readSettingsFile(self.settingPath, self)
        self.initValues()

    def initValues(self):
        readMainFile(self.mainFilePath, self) # This has side effects and will define the pingDataFilePaths attribute.
        self.pingDatas = [readPingData(FilePath) for FilePath in self.pingDataFilePaths]

    def changeSaveLocation(self, newLocation : str):
        self.mainFilePath = newLocation
        self.initValues()
        self.writeAllData()

    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height

    def getPingDatas(self):
        return self.pingDatas
    
    def writeAllData(self):
        self.writeSettingsFile()
        self.writeMainFile()
        self.writePingDatas()

    def writeSettingsFile(self):
        writeSettingsFile(self.settingPath, self.mainFilePath, self.width, self.height)

    def writeMainFile(self):
        writeMainFile(self.mainFilePath, self.pingDataFilePaths)
    
    def writePingDatas(self):
        for pingData in self.pingDatas:
            writePingData(pingData)

    def addNewPingStater(self):
        if self.mainFilePath == None:
            QMessageBox.critical(None, "Error", "No save location selected. Please select a save location before adding a ping stater.")
            return
        count = len(self.pingDatas)+1
        filePath = path.join(path.dirname(self.mainFilePath), "pingData" + str(len(self.pingDatas)+1) + ".json")
        while filePath in self.pingDataFilePaths:
            count += 1
            filePath = path.join(path.dirname(self.mainFilePath), "pingData" + str(count) + ".json")

        newPingData = PingData.getNew(filePath)
        self.pingDatas.append(newPingData)
        self.pingDataFilePaths.append(filePath)
        writePingData(newPingData)
        self.writeMainFile()

    def removePingStater(self, pingData : PingData):
        self.pingDatas.remove(pingData)
        self.pingDataFilePaths.remove(pingData.filePath)
        self.writeMainFile()
        # os.remove(pingData.filePath)

    def changePingDataOrder(self, pingDataFilePaths : List[str]):
        self.pingDataFilePaths = pingDataFilePaths
        pingDatas = []
        for filePath in pingDataFilePaths:
            for pingData in self.pingDatas:
                if pingData.filePath == filePath:
                    pingDatas.append(pingData)
                    break
        self.pingDatas = pingDatas
        self.writeMainFile()

    @classmethod
    def _getSettingFileLocation(self):
        """
        This is not a getter but instead is used to generate the default location for the main file during initialization.
        """
        if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader extends the sys module by a flag frozen=True. (Taken from stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741)
            dir_path = os.path.dirname(os.path.abspath(sys.executable))
            
        else:
            dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        return os.path.join(dir_path, "settings.json")