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

        self.checkBoxes : List[OptionStatCheckbox] = []
        self.checkbox1 = OptionStatCheckbox("Ping number","pingNumber")
        self.checkBoxes.append(self.checkbox1)

        self.checkbox2 = OptionStatCheckbox("Time since last ping","timeSinceLastPing")
        self.checkBoxes.append(self.checkbox2)

        self.checkbox3 = OptionStatCheckbox("Average ping per day","averagePing")
        self.checkBoxes.append(self.checkbox3)
        self.checkboxLayout = QVBoxLayout()
        for checkbox in self.checkBoxes:
            checkbox.setChecked(checkbox.option in self.pingStatWidget.pingData.getStatsToShow())
            self.checkboxLayout.addWidget(checkbox)
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.updateOptionSet(checkbox))

        self.orderChoice = OrderChoice(self.statsToShow, self.readOrderChoice)
        self.twoColumnsLayout = QHBoxLayout()
        self.twoColumnsLayout.addLayout(self.checkboxLayout)
        self.twoColumnsLayout.addWidget(self.orderChoice)

        self.buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save)
        self.buttonLayout.addWidget(self.saveButton)
        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.buttonLayout.addWidget(self.closeButton)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.twoColumnsLayout)
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)
        self.setTitle("Settings")
        self.setStyleSheet("StaterSetting { border: 1px solid black; }")

    def save(self):
        self.pingStatWidget.setStatsToShow(self.statsToShow)

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

    def readOrderChoice(self):
        self.statsToShow = self.orderChoice.getOrderedOptions()

class OptionStatCheckbox(QCheckBox):
    option : str
    def __init__(self, text : str, option : str):
        super().__init__(text)
        self.option = option

class OrderChoice(QGroupBox):
    optionToDisplayText = {"pingNumber" : "Ping number", "timeSinceLastPing" : "Time since last ping", "averagePing" : "Average ping per day"}

    def __init__(self, statsToShow, updateFunction) -> None:
        super().__init__()

        self.setTitle("Order (drag and drop)")
        self.setStyleSheet("border: 1px solid black;")  # Add black border
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
            super().__init__(updateFunction)
            self.quickOptions(statsToShow)

        def quickOptions(self, statsToShow):
            for option in statsToShow:
                button = OrderChoice.OptionKnowingDisplay(OrderChoice.optionToDisplayText[option], option)
                self.addWidgetOption(button)

        def updateOptionSet(self, statsToShow):
            self.clear()
            self.quickOptions(statsToShow)

        def getOrderedOptions(self):
            buttons : List[OrderChoice.OptionKnowingDisplay] = self.getOptions()
            return [button.option for button in buttons]
    
    class OptionKnowingDisplay(QLabel):
        option : str
        def __init__(self, text : str, option : str):
            super().__init__(text)
            self.option = option
            self.setStyleSheet("background-color: white; border: 1px solid black;")
