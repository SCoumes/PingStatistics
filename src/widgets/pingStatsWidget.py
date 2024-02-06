from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QDialog, QDialogButtonBox, QDateEdit, QTimeEdit, QGridLayout, QSizePolicy, QDateTimeEdit
from PyQt6.QtCore import QDateTime, QTime
from PyQt6.QtGui import QFontMetrics

from src.utils import cleanDecimals
from src import PingData, Date
from src.widgets.staterSetting import StaterSetting
from src.widgets import TimeSelector

if TYPE_CHECKING:
    from src.controllers import MainController
from PyQt6.QtWidgets import QMessageBox

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

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.setTitle(pingData.name)
        self.autosetStyleSheet()

    def pingNow(self):
        self.ping(Date.now())

    def ping(self, date):
        if date < self.pingData.begining:
            confirm = QMessageBox.question(self, "Confirmation", "This ping is older than the begining. Update begining to match the ping?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            if confirm == QMessageBox.StandardButton.Yes:
                self.pingData.begining = date
            else :
                return
        self.mainController.ping(date, self.pingData)

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

    def redraw(self):
        self.rightInfo.redraw()

class _ButtonLeft(QWidget):
    button1 : QPushButton
    button2 : QPushButton
    button3 : QPushButton
    pingStatWidget : PingStatsWidget

    def __init__(self, parent : PingStatsWidget):
        super().__init__(parent)
        self.pingStatWidget = parent
        self.layout = QVBoxLayout()

        self.button1 = QPushButton("Ping now", self)
        self.button2 = QPushButton("Ping at date", self)
        self.button3 = QPushButton("Settings", self)

        self.button1.clicked.connect(parent.pingNow)
        self.button2.clicked.connect(self.openDateSelection)
        self.button3.clicked.connect(parent.openSettings)

        self.setMaximumWidth(self.button2.sizeHint().width() + 30)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.setLayout(self.layout)

    def openDateSelection(self):
        self.timeSelector = TimeSelector(self.pingStatWidget.ping)

class _InfoRight(QWidget):
    parent : PingStatsWidget
    label1 : QLabel
    label2 : QLabel

    def __init__(self, parent : PingStatsWidget):
        super().__init__(parent)
        self.containerLayout = None
        self.parent = parent
        self.redraw()

    def redraw(self):
        # Need to redraw change resizing window
        self.statsToShow = self.parent.pingData.getStatsToShow()
        self.labels = self.getLabelList()
        self.recalculate()
        if self.containerLayout is not None:
            deletionWidget = QWidget()
            deletionWidget.setLayout(self.containerLayout)
        self.containerLayout = QVBoxLayout()
        self.setLayout(self.containerLayout)

        max_width = self.parent.mainController.getMainWindowWidth() - 250
        accumulated_width = 0
        lineLayout = QHBoxLayout()
        lineLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.containerLayout.addLayout(lineLayout)
        for label in self.labels:
            accumulated_width += label.sizeHint().width()
            if accumulated_width > max_width:
                lineLayout = QHBoxLayout()
                lineLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
                self.containerLayout.addLayout(lineLayout)
                accumulated_width = label.sizeHint().width()
            lineLayout.addWidget(label)

    def getLabelList(self) -> list[QLabel]:
        return [_InfoRightLabel(self) for _ in self.statsToShow]

    def recalculate(self):
        for statToShow, label in zip(self.statsToShow, self.labels):
            label.setText(" " + self.parent.pingData.getStatText(statToShow) + " ")

class _InfoRightLabel(QLabel):
    def __init__(self, parent : _InfoRight):
        super().__init__(parent)
        self.parent = parent
        self.setStyleSheet("background-color: #CCCCCC;")

    def setText(self, text : str):
        super().setText(text)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMaximumHeight(self.fontMetrics().height() + 10)
        metrics = QFontMetrics(self.font())
        text_width = metrics.horizontalAdvance(self.text())
        self.setMinimumWidth(text_width + 10) 
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
