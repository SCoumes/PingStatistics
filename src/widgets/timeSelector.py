from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QDialog, QDialogButtonBox, QDateEdit, QTimeEdit, QGridLayout, QSizePolicy, QDateTimeEdit
from PyQt6.QtCore import QDateTime, QTime
from PyQt6.QtGui import QFontMetrics

from src.utils import cleanDecimals
from src import PingData, Date
from src.widgets.staterSetting import StaterSetting

if TYPE_CHECKING:
    from src.controllers import MainController

class TimeSelector(QDialog):
    def __init__(self, returnFunction):
        super().__init__()
        dialog = self
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
            returnFunction(Date.fromNaive(selectedDateTime.toPyDateTime()))