from typing import List, TYPE_CHECKING, Dict

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src import PingData, Date
from src.widgets import OrderList
from src.widgets.pingStatsWidget import PingStatsWidget, QSizePolicy

if TYPE_CHECKING:
    from src.controllers import MainController

class PingWidgetPresenter(OrderList):
    pingsWidgets : Dict[str, PingStatsWidget]
    mainController : 'MainController'

    def __init__(self, pingDatas : List[PingData], mainController : 'MainController'):
        super().__init__(lambda : mainController.getDataController().changePingDataOrder(self.getFilepathOrder())) # The only bookeeping to do when changing order is to write to mainfile
        self.mainController = mainController
        self.pingsWidgets = {}
        self.pingDatas : List[PingData] = pingDatas
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.MinimumExpanding)

        for pingData in self.pingDatas:
            pingWidget = PingStatsWidget(pingData, mainController)
            self.pingsWidgets[pingData.fileName] = pingWidget
            self.addWidgetOption(pingWidget)

        self.setStyleSheet("color: black;")

        self.vlayout.addStretch()

    def getFilepathOrder(self):
        pingWidgets : List[PingStatsWidget] = self.getOptions()
        return [pingWidget.pingData.fileName for pingWidget in pingWidgets]
    
    def getPingsWidgets(self) -> Dict[PingData, PingStatsWidget]:
        return self.pingsWidgets

    @classmethod
    def getPlaceHolder(cls):
        return cls([], None)