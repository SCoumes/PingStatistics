from typing import List

from src.controllers import DataController  
from src import MainWindow
from src.widgets.pingWidgetsPresenter import PingWidgetPresenter
from src import PingData

class MainController:
    def __init__(self, window : MainWindow) -> None:
        self.mainWindow = window
        self.dataController = DataController()

    def initApp(self):
        """Performs various operations related to the initialization of the application. Should be called once right after the controller is created."""
        self.redraw()
        self.connectAddPingStater()

    def getDataController(self) -> DataController:
        return self.dataController
    
    def redraw(self):
        self.mainWindow.pingPresenter = PingWidgetPresenter(self.getDataController().getPingDatas(), self)
        self.mainWindow.redrawLayout()

    def addPingStater(self):
        """Add a new ping stater to the list of ping staters."""
        self.dataController.addNewPingStater()
        self.redraw()

    def connectAddPingStater(self):
        self.mainWindow.addPingStater.clicked.connect(self.addPingStater)

    def removePingStater(self, pingData : PingData):
        self.dataController.removePingStater(pingData)
        self.redraw()

    def deactivateMainWindow(self):
        self.mainWindow.setEnabled(False)

    def activateMainWindow(self):
        self.mainWindow.setEnabled(True)