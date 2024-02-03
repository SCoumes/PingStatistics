from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QDialog, QDialogButtonBox, QDateEdit, QTimeEdit, QGridLayout
from PyQt6.QtCore import QDateTime, QTime

from src.utils import cleanDecimals
from src import PingData, Date
from src.widgets.staterSetting import StaterSetting

if TYPE_CHECKING:
    from src.controllers import MainController
from PyQt6.QtWidgets import QDateTimeEdit

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

    def ping(self, date = Date.now()):
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
    button3 : QPushButton
    pingStatWidget : PingStatsWidget

    def __init__(self, parent : PingStatsWidget):
        super().__init__(parent)
        self.pingStatWidget = parent
        self.layout = QVBoxLayout()

        self.button1 = QPushButton("Ping now", self)
        self.button2 = QPushButton("Ping at date", self)
        self.button3 = QPushButton("Settings", self)

        self.button1.clicked.connect(parent.ping)
        self.button2.clicked.connect(self.openDateSelection)
        self.button3.clicked.connect(parent.openSettings)

        self.setMaximumWidth(self.button2.sizeHint().width() + 30)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.setLayout(self.layout)

    def openDateSelection(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select date and time")
        
        # Add time selection option
        hour_selector = QTimeEdit(self)
        hour_selector.setTime(QTime.currentTime())
        hour_selector.setDisplayFormat("HH")

        minute_selector = QTimeEdit(self)
        minute_selector.setTime(QTime.currentTime())
        minute_selector.setDisplayFormat("mm")

        dateTimeEdit = QDateTimeEdit()
        dateTimeEdit.setDisplayFormat("dd/MM/yyyy")
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        dateTimeEdit.setCalendarPopup(True)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(dialog.accept)
        buttonBox.rejected.connect(dialog.reject)

        layout = QGridLayout()
        layout.addWidget(dateTimeEdit, 0, 0, 1, 2)
        layout.addWidget(hour_selector, 1, 0, 1, 1)
        layout.addWidget(minute_selector, 1, 1, 1, 1)
        layout.addWidget(buttonBox, 2, 0, 1, 2)
        dialog.setLayout(layout)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selectedDateTime = dateTimeEdit.dateTime()
            selectedDateTime.setTime(QTime(hour_selector.time().hour(), minute_selector.time().minute()))
            self.pingStatWidget.ping(Date.fromNaive(selectedDateTime.toPyDateTime()))
            # Do something with the selected date and time

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
