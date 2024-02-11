from typing import List, Dict

from src.controllers import DataController  
from src import MainWindow
from src.widgets import PingStatsWidget
from src.widgets.pingWidgetsPresenter import PingWidgetPresenter
from src import PingData

class MainController:
    def __init__(self, window : MainWindow) -> None:
        self.mainWindow = window
        self.dataController = DataController()

    def initApp(self):
        """Performs various operations related to the initialization of the application. Should be called once right after the controller is created."""
        self.mainWindow.skipRedraw = False
        self.mainWindow.mainController = self
        width, height = self.dataController.getDimensions()
        self.mainWindow.resize(width, height)
        self.redraw()

    def changeSaveLocation(self, newLocation : str):
        """Change the location where the data is saved."""
        self.dataController.changeSaveLocation(newLocation)
        self.redraw()

    def getDataController(self) -> DataController:
        return self.dataController
    
    def redraw(self):
        self.mainWindow.pingPresenter = PingWidgetPresenter(self.getDataController().getPingDatas(), self)
        self.mainWindow.redrawLayout()

    def addPingStater(self):
        """Add a new ping stater to the list of ping staters."""
        self.dataController.addNewPingStater()
        self.redraw()

    def removePingStater(self, pingData : PingData):
        self.dataController.removePingStater(pingData)
        self.redraw()

    def deactivateMainWindow(self):
        self.mainWindow.setEnabled(False)

    def activateMainWindow(self):
        self.mainWindow.setEnabled(True)

    def getMainWindowWidth(self) -> int:
        return self.mainWindow.width()
    
    def ping(self, date, pingData : PingData):
        """
        Register a ping and handles all necessary consequences
        """
        fileNamesToWidget : Dict[str, PingStatsWidget] = self.mainWindow.pingPresenter.getPingsWidgets()
        fileNameToPingData : Dict[str, PingData] = self.dataController.getPingDataDict()
        updated = []
        toUpdate : PingData = pingData
        while toUpdate != None and toUpdate not in updated:
            toUpdate.ping(date)
            fileNamesToWidget[toUpdate.fileName].rightInfo.recalculate()
            updated.append(toUpdate)
            if toUpdate.transitivity in fileNameToPingData:
                toUpdate = fileNameToPingData[toUpdate.transitivity]
            else:
                toUpdate.transitivity = None # We detected a dangling reference to a pingData that does not exist, remove it now
                toUpdate = None
        self.dataController.writePingDatas()