from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox

from src.utils import cleanDecimals
from src import PingData, Date
from src.widgets.staterSetting import StaterSetting

if TYPE_CHECKING:
    from src.controllers import MainController

class PingStatsWidget(QGroupBox):
    pingData : PingData
    leftButton : '_ButtonLeft'
    rightInfo : '_InfoRight'
    mainController : 'MainController'

    def __init__(self, pingData: PingData, mainController : 'MainController'):
        super().__init__()

        self.mainController = mainController
        self.pingData = pingData
        self.leftButton = _ButtonLeft(self)
        self.rightInfo = _InfoRight(self)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.leftButton)
        self.layout.addWidget(self.rightInfo)
        self.outerLayout = QVBoxLayout()
        self.outerLayout.addLayout(self.layout)
        self.setLayout(self.outerLayout)

        self.setTitle(pingData.name)
        self.autosetStyleSheet()

    def ping(self):
        date = Date.now()
        self.pingData.ping(date)
        self.rightInfo.recalculate()
        self.mainController.getDataController().writePingDatas()

    def openSettings(self):
        self.settings = StaterSetting(self)
        self.settings.show()

    def setStatsToShow(self, statsToShow : list[str]):
        self.pingData.setStatsToShow(statsToShow)
        self.rightInfo.redraw()

    def changeColor(self, color : str):
        self.pingData.setColor(color)
        self.mainController.getDataController().writePingDatas()
        self.autosetStyleSheet()

    def autosetStyleSheet(self):
        self.setStyleSheet("PingStatsWidget { border: 1px solid black; background-color: " + self.pingData.color + "; }")

class _ButtonLeft(QWidget):
    button1 : QPushButton
    button2 : QPushButton

    def __init__(self, parent : PingStatsWidget):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.button1 = QPushButton("Ping", self)
        self.button2 = QPushButton("Delete", self)
        self.button3 = QPushButton("Settings", self)

        self.button1.clicked.connect(parent.ping)
        self.button2.clicked.connect(lambda : parent.mainController.removePingStater(parent.pingData))
        self.button3.clicked.connect(parent.openSettings)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.setLayout(self.layout)
        self.setMinimumWidth(max(self.button1.sizeHint().width(), self.button2.sizeHint().width(), self.button3.sizeHint().width()))
        self.setMaximumWidth(max(self.button1.sizeHint().width(), self.button2.sizeHint().width(), self.button3.sizeHint().width()))

class _InfoRight(QWidget):
    parent : PingStatsWidget
    label1 : QLabel
    label2 : QLabel

    def __init__(self, parent : PingStatsWidget):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.parent = parent
        self.redraw()

    def redraw(self):
        if self.layout is not None:
            # The way to delete a layout is to give it to another widget to which no reference is given
            deletionWidget = QWidget()
            deletionWidget.setLayout(self.layout)
        self.layout = QHBoxLayout()
        self.statsToShow = self.parent.pingData.getStatsToShow()
        self.labels = self.getLabelList()
        for label in self.labels:
            self.layout.addWidget(label)
        self.setLayout(self.layout)
        self.recalculate()

    def getLabelList(self) -> list[QLabel]:
        labels = []
        for _ in self.statsToShow:
            label = QLabel("", self) # Label text will be set later through recalculate()
            label.setMinimumWidth(150)
            label.setStyleSheet("background-color: #888888;")
            labels.append(label)
        return labels

    def recalculate(self):
        for statToShow, label in zip(self.statsToShow, self.labels):
            label.setText(" " + self.parent.pingData.getStatText(statToShow) + " ")
