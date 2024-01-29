from typing import TYPE_CHECKING
from PyQt6.QtGui import QCloseEvent

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox, QCheckBox, QMainWindow

if TYPE_CHECKING:
    from src import PingStatsWidget

class StaterSetting(QMainWindow):
    def __init__(self, parent : 'PingStatsWidget'):
        super().__init__()
        self.internalWidget = _internalStater(parent)
        self.setCentralWidget(self.internalWidget)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.internalWidget.close()
        return super().closeEvent(a0)

class _internalStater(QGroupBox):
    parent : 'PingStatsWidget'

    def __init__(self, parent : 'PingStatsWidget'):
        super().__init__()
        self.parent = parent
        self.parent.mainController.deactivateMainWindow()
        self.layout = QVBoxLayout()

        self.checkbox1 = QCheckBox("Show ping")
        self.layout.addWidget(self.checkbox1)

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
        if self.checkbox1.isChecked():
            print("It is checked")
        else:
            print("It is not checked")

    def closeEvent(self, event):
        self.parent.mainController.activateMainWindow()
        super().closeEvent(event)
