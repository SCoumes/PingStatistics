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
    pingDatasDict : dict[str, PingData] # keys are the filenames of the pingDatas
    pingDataFileNames : List[str] # Decides the order of the corresponding widgets; in two-column mode: left column items first, then right column items
    twoColumns : bool
    leftColumnCount : int # Number of items in the left column when twoColumns is True

    def __init__(self) -> None:
        self.settingPath = DataController._getSettingFileLocation()
        readSettingsFile(self.settingPath, self)
        self.initValues()

    def initValues(self):
        readMainFile(self.mainFilePath, self) # This has side effects and will define the pingDataFilePaths attribute and twoColumns.
        self.pingDatasDict = {}
        if self.mainFilePath is None: return
        dirname = path.dirname(self.mainFilePath)
        for fileName in self.pingDataFileNames:
            self.pingDatasDict[fileName] = readPingData(dirname, fileName)

    def changeSaveLocation(self, newLocation : str):
        self.mainFilePath = newLocation
        self.initValues()
        self.writeAllData()

    def getDimensions(self):
        return self.width, self.height
    
    def getPingDataDict(self):
        return self.pingDatasDict
    
    def changeDimensions(self, width : int, height : int):
        self.width = width
        self.height = height
        self.writeSettingsFile()
    
    def getPingDatas(self):
        return [self.pingDatasDict[f] for f in self.pingDataFileNames if f in self.pingDatasDict]
    
    def writeAllData(self):
        self.writeSettingsFile()
        self.writeMainFile()
        self.writePingDatas()

    def writeSettingsFile(self):
        writeSettingsFile(self.settingPath, self.mainFilePath, self.width, self.height)

    def writeMainFile(self):
        writeMainFile(self.mainFilePath, self.pingDataFileNames, self.twoColumns, self.leftColumnCount)

    def toggleTwoColumns(self):
        self.twoColumns = not self.twoColumns
        if self.mainFilePath is not None:
            self.writeMainFile()
    
    def writePingDatas(self):
        dirName = path.dirname(self.mainFilePath)
        for pingData in self.pingDatasDict.values():
            writePingData(dirName, pingData)

    def addNewPingStater(self):
        if self.mainFilePath == None:
            QMessageBox.critical(None, "Error", "No save location selected. Please select a save location before adding a ping stater.")
            return
        count = len(self.pingDatasDict)+1
        fileName =  "pingData" + str(count) + ".json"
        while fileName in self.pingDataFileNames:
            count += 1
            fileName = "pingData" + str(count) + ".json"

        newPingData = PingData.getNew(fileName)
        self.pingDatasDict[fileName] = newPingData
        self.pingDataFileNames.append(fileName)
        # In two-column mode new items go to the right column (after leftColumnCount items)
        writePingData(path.dirname(self.mainFilePath), newPingData)
        self.writeMainFile()

    def removePingStater(self, pingData : PingData):
        idx = self.pingDataFileNames.index(pingData.fileName)
        self.pingDatasDict.pop(pingData.fileName)
        self.pingDataFileNames.remove(pingData.fileName)
        # If removed item was in the left column, adjust leftColumnCount
        if idx < self.leftColumnCount:
            self.leftColumnCount = max(0, self.leftColumnCount - 1)
        self.writeMainFile()

    def changePingDataOrder(self, pingDataFileNames : List[str]):
        self.pingDataFileNames = pingDataFileNames
        self.writeMainFile()

    def changePingDataOrderTwoCol(self, leftFileNames : List[str], rightFileNames : List[str]):
        self.pingDataFileNames = leftFileNames + rightFileNames
        self.leftColumnCount = len(leftFileNames)
        self.writeMainFile()

    def changePingDataTransitivity(self, pingData : PingData, transitivity : Optional[str]):
        pingData.transitivity = transitivity
        self.writePingDatas()

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