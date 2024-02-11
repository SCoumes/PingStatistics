from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QListWidget, QVBoxLayout, QWidget, QListWidgetItem, QPushButton

from src import PingData

if TYPE_CHECKING:
    from src.controllers import MainController
    from src.widgets import PingStatsWidget
        
class _PingDataItem(QListWidgetItem):
    def __init__(self, pingData : PingData | None):
        self.pingData = pingData
        name = pingData.name if pingData else "No transitivity"
        super().__init__(name)

class _InnerTransitivitySelector(QListWidget):
    mainController : 'MainController'
    parentWidget : 'PingStatsWidget'

    def __init__(self, mainController : 'MainController', parentWidget : 'PingStatsWidget') -> None:
        super().__init__()
        self.mainController = mainController
        self.parentWidget = parentWidget
        defaultItem = _PingDataItem(None)
        self.addItem(defaultItem)
        currentTransitivity = defaultItem
        for pingData in mainController.getDataController().getPingDatas():
            item = _PingDataItem(pingData)
            self.addItem(item)
            if item.pingData.fileName == parentWidget.pingData.transitivity:
                currentTransitivity = item
        self.setCurrentItem(currentTransitivity)

class TransitivitySelector(QWidget):
    innerSelector : _InnerTransitivitySelector
    mainController : 'MainController'
    parentWidget : 'PingStatsWidget'

    def __init__(self, mainController : 'MainController', parentWidget : 'PingStatsWidget') -> None:
        super().__init__()
        self.mainController = mainController
        self.parentWidget = parentWidget
        self.innerSelector = _InnerTransitivitySelector(mainController, parentWidget)
        self.button = QPushButton("Change transitivity")
        self.button.clicked.connect(self.handlePingDataSelection)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.innerSelector)
        self.layout.addWidget(self.button)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def handlePingDataSelection(self):
        item : _PingDataItem = self.innerSelector.currentItem()
        transitivity = item.pingData.fileName if item.pingData else None
        self.mainController.getDataController().changePingDataTransitivity(self.parentWidget.pingData, transitivity)
