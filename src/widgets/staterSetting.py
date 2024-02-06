from typing import TYPE_CHECKING, List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QCheckBox, QMainWindow, QSpacerItem, QSizePolicy, QColorDialog, QLineEdit, QListWidget, QListWidgetItem

if TYPE_CHECKING:
    from src import PingStatsWidget

from src.widgets import OrderList, TransitivitySelector
from PyQt6.QtWidgets import QMessageBox

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
    settingWidget : StaterSetting

    def __init__(self, pingStatWidget : 'PingStatsWidget', settingWidget : StaterSetting):
        super().__init__()
        self.pingStatWidget = pingStatWidget
        self.statsToShow = pingStatWidget.pingData.getStatsToShow()
        self.settingWidget = settingWidget

        self.pingStatWidget.mainController.deactivateMainWindow()

        self.stateName = QLineEdit()
        self.stateName.setText(self.pingStatWidget.pingData.name)
        self.stateName.textChanged.connect(self.setName)

        self.orderChoice = OrderChoice(self.statsToShow, self.saveStatsToShow)

        self.colorButton = QPushButton("Color")
        self.colorButton.clicked.connect(self.openColorDialog)

        self.transitivitySelector = TransitivitySelector(self.pingStatWidget.mainController, self.pingStatWidget)

        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteWidget)
        self.deleteButton.setStyleSheet("background-color: red;")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stateName)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.orderChoice)
        self.layout.addWidget(self.transitivitySelector)
        self.layout.addWidget(self.colorButton)
        self.layout.addWidget(self.deleteButton)
        self.setLayout(self.layout)
        self.setTitle("Settings")
        self.setStyleSheet("StaterSetting { border: 1px solid black; }")

    def saveStatsToShow(self, statsToShow : List[str]):
        self.pingStatWidget.setStatsToShow(statsToShow)
        self.pingStatWidget.mainController.getDataController().writePingDatas()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.settingWidget.close()
        self.pingStatWidget.mainController.activateMainWindow()

    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pingStatWidget.changeColor(color.name())

    def setName(self):
        self.pingStatWidget.pingData.name = self.stateName.text()
        self.pingStatWidget.setTitle(self.stateName.text())
        self.pingStatWidget.mainController.getDataController().writePingDatas()

    def deleteWidget(self):
        confirm = QMessageBox.question(self, "Confirmation", "Really delete these pings?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.pingStatWidget.mainController.removePingStater(self.pingStatWidget.pingData)
            self.settingWidget.close()

class OrderChoice(QGroupBox):
    optionToDisplayText = {"pingNumber" : "Total number of pings", "timeSinceLastPing" : "Time since last ping", "averagePing" : "Average ping per day", "frequencyInDay" : "Fraction of days with one or more pings", "maxInDay" : "Maximum pings in a day", "medianDay" : "Median pings per day", "last30days" : "Pings in the last 30 days"}
    allPossibleOptions = ["pingNumber", "timeSinceLastPing", "averagePing", "frequencyInDay", "maxInDay", "medianDay", "last30days"]

    def __init__(self, statsToShow, updateFunction) -> None:
        super().__init__()

        self.setTitle("Drag and drop to order")
        self.setStyleSheet("OrderChoice { border: 1px solid black; }") 
        self.innerOrderChoice = OrderChoice.InnerOrderChoice(statsToShow, updateFunction)
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

        def __init__(self, statsToShow, updateFunction) -> None:
            self.updateFunction = lambda : updateFunction(self.getOrderedOptions())
            super().__init__(self.updateFunction)
            self.quickOptions(statsToShow)

        def quickOptions(self, statsToShow):
            for option in statsToShow:
                checkBox = OrderChoice.OptionKnowingDisplay(OrderChoice.optionToDisplayText[option], option)
                checkBox.setChecked(True)
                checkBox.stateChanged.connect(self.updateFunction) # Note that update function was here is not the argument to InnerOrderChoice's constructor, but is the function passed in said constructor to the super constructor
                self.addWidgetOption(checkBox)

            for option in OrderChoice.allPossibleOptions:
                if option not in statsToShow:
                    checkBox = OrderChoice.OptionKnowingDisplay(OrderChoice.optionToDisplayText[option], option)
                    checkBox.stateChanged.connect(self.updateFunction) # Note that update function was here is not the argument to InnerOrderChoice's constructor, but is the function passed in said constructor to the super constructor
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
