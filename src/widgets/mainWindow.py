from typing import List

from time import sleep
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtWidgets import QMainWindow, QLabel

from src import PingData, Date
from src.widgets.pingWidgetsPresenter import PingWidgetPresenter

class MainWindow(QMainWindow):
    pingPresenter : 'PingWidgetPresenter'
    addPingStater : QPushButton
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ping stater")
        self.addPingStater = QPushButton("Add ping stater", self)

    def redrawLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.pingPresenter)
        self.layout.addWidget(self.addPingStater)
        self.containerWidget = QWidget()
        self.containerWidget.setLayout(self.layout)
        self.setCentralWidget(self.containerWidget)

