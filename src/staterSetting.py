from typing import TYPE_CHECKING, List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QCheckBox, QMainWindow, QSpacerItem, QSizePolicy

if TYPE_CHECKING:
    from src import PingStatsWidget

from src.widgets import OrderList

class StaterSetting(QMainWindow):
    def __init__(self, parent : 'PingStatsWidget'):
        super().__init__()
        self.internalWidget = _internalStater(parent, self)
        self.setCentralWidget(self.internalWidget)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.internalWidget.close()
        return super().closeEvent(a0)

class _internalStater(QGroupBox):
    pingStatWidget : 'PingStatsWidget'
    statsToShow : List[str]

    def __init__(self, pingStatWidget : 'PingStatsWidget', settingWidget : StaterSetting):
        super().__init__()
        self.pingStatWidget = pingStatWidget
        self.statsToShow = pingStatWidget.pingData.getStatsToShow()
        self.settingWidget = settingWidget

        self.pingStatWidget.mainController.deactivateMainWindow()

        self.orderChoice = OrderChoice(self.statsToShow)

        self.buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save)
        self.buttonLayout.addWidget(self.saveButton)
        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.buttonLayout.addWidget(self.closeButton)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.orderChoice)
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)
        self.setTitle("Settings")
        self.setStyleSheet("StaterSetting { border: 1px solid black; }")

    def save(self):
        self.pingStatWidget.setStatsToShow(self.orderChoice.getOrderedOptions())

    def closeEvent(self, event):
        super().closeEvent(event)
        self.settingWidget.close()
        self.pingStatWidget.mainController.activateMainWindow()

    def updateOptionSet(self, checkbox : 'OptionStatCheckbox'):
        if checkbox.isChecked():
            self.statsToShow.append(checkbox.option)
        else:
            self.statsToShow.remove(checkbox.option)
        self.orderChoice.updateOptionSet(self.statsToShow)

class OptionStatCheckbox(QCheckBox):
    option : str
    def __init__(self, text : str, option : str):
        super().__init__(text)
        self.option = option

class OrderChoice(QGroupBox):
    optionToDisplayText = {"pingNumber" : "Ping number", "timeSinceLastPing" : "Time since last ping", "averagePing" : "Average ping per day"}

    def __init__(self, statsToShow) -> None:
        super().__init__()

        self.setTitle("Drag and drop to order")
        self.setStyleSheet("OrderChoice { border: 1px solid black; }") 
        self.innerOrderChoice = OrderChoice.InnerOrderChoice(statsToShow)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.innerOrderChoice)
        self.layout.setContentsMargins(0, 10, 0, 0)
        self.setLayout(self.layout)

    def quickOptions(self, statsToShow):
        return self.innerOrderChoice.quickOptions(statsToShow)
    
    def updateOptionSet(self, statsToShow):
        return self.innerOrderChoice.updateOptionSet(statsToShow)
    
    def getOrderedOptions(self):
        return self.innerOrderChoice.getOrderedOptions()

    class InnerOrderChoice(OrderList):
        allPossibleOptions = ["pingNumber", "timeSinceLastPing", "averagePing"]

        def __init__(self, statsToShow) -> None:
            super().__init__(lambda : None)
            self.quickOptions(statsToShow)

        def quickOptions(self, statsToShow):
            for option in statsToShow:
                checkBox = OrderChoice.OptionKnowingDisplay(OrderChoice.optionToDisplayText[option], option)
                checkBox.setChecked(True)
                self.addWidgetOption(checkBox)

            for option in OrderChoice.InnerOrderChoice.allPossibleOptions:
                if option not in statsToShow:
                    checkBox = OrderChoice.OptionKnowingDisplay(OrderChoice.optionToDisplayText[option], option)
                    self.addWidgetOption(checkBox)

        def updateOptionSet(self, statsToShow):
            self.clear()
            self.quickOptions(statsToShow)

        def getOrderedOptions(self):
            checkBoxes : List[OrderChoice.OptionKnowingDisplay] = self.getOptions()
            return [checkbox.option for checkbox in checkBoxes if checkbox.isChecked()]
    
    class OptionKnowingDisplay(QCheckBox):
        option : str
        def __init__(self, text : str, option : str):
            super().__init__(text)
            self.option = option
            self.setStyleSheet("background-color: white;")
