from typing import TYPE_CHECKING, List
from PyQt6.QtGui import QCloseEvent

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QCheckBox, QMainWindow   

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
        self.layout = QVBoxLayout()

        self.checkBoxes : List[OptionStatCheckbox] = []
        self.checkbox1 = OptionStatCheckbox("Ping number","pingNumber")
        self.checkBoxes.append(self.checkbox1)

        self.checkbox2 = OptionStatCheckbox("Time since last ping","timeSinceLastPing")
        self.checkBoxes.append(self.checkbox2)

        self.checkbox3 = OptionStatCheckbox("Average ping per day","averagePing")
        self.checkBoxes.append(self.checkbox3)
        for checkbox in self.checkBoxes:
            checkbox.setChecked(checkbox.option in self.pingStatWidget.pingData.getStatsToShow())
            self.layout.addWidget(checkbox)
            checkbox.stateChanged.connect(lambda state, checkbox=checkbox: self.updateOptionSet(checkbox))

        self.orderChoice = OrderChoice(self.statsToShow, self.readOrderChoice)
        self.layout.addWidget(self.orderChoice)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save)
        self.layout.addWidget(self.saveButton)

        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)

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

class OrderChoice(OrderList):
    optionToDisplayText = {"pingNumber" : "Ping number", "timeSinceLastPing" : "Time since last ping", "averagePing" : "Average ping per day"}

    def __init__(self, statsToShow, updateFunction) -> None:
        super().__init__(updateFunction)
        self.quickOptions(statsToShow)

    def quickOptions(self, statsToShow):
        for option in statsToShow:
            button = OrderChoice.OptionKnowingButton(OrderChoice.optionToDisplayText[option], option)
            self.addWidgetOption(button)

    def updateOptionSet(self, statsToShow):
        self.clear()
        self.quickOptions(statsToShow)

    def getOrderedOptions(self):
        buttons : List[OrderChoice.OptionKnowingButton] = self.getOptions()
        return [button.option for button in buttons]
    
    class OptionKnowingButton(QPushButton):
        option : str
        def __init__(self, text : str, option : str):
            super().__init__(text)
            self.option = option
