from typing import List, TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src import PingData, Date
from src.pingStatsWidget import PingStatsWidget

if TYPE_CHECKING:
    from src.controllers import MainController

class PingWidgetPresenter(QWidget):
    def __init__(self, pingDatas : List[PingData], mainController : 'MainController'):
        super().__init__()
        self.pingDatas : List[PingData] = pingDatas

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.pingWidgets = []
        for pingData in self.pingDatas:
            pingWidget = PingStatsWidget(pingData, mainController)
            self.pingWidgets.append(pingWidget)
            self.layout.addWidget(pingWidget)

    @classmethod
    def getPlaceHolder(cls):
        return cls([], None)