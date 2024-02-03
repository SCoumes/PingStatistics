from typing import List, TYPE_CHECKING

from time import sleep
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import QTimer

from src import PingData, Date
from src.widgets.pingWidgetsPresenter import PingWidgetPresenter

if TYPE_CHECKING:
    from src.controllers import MainController

class MainWindow(QMainWindow):
    mainController : 'MainController'
    pingPresenter : 'PingWidgetPresenter'
    addPingStater : QPushButton
    skipRedraw : bool
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ping stater")
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.addPingStater = QPushButton("Add ping stater", self)
        self.skipRedraw = True
        self.resizeTimer = QTimer()
        self.resizeTimer.setSingleShot(True)
        self.resizeTimer.timeout.connect(self.onResizeDone)
    
    def resizeEvent(self, event):
        # Call the base class method
        super().resizeEvent(event)
        if not self.skipRedraw:
            self.resizeTimer.start(100)

    def onResizeDone(self):
        self.mainController.redraw()
        
    def redrawLayout(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.pingPresenter)
        self.layout.addWidget(self.addPingStater)
        self.containerWidget = QWidget()
        self.containerWidget.setLayout(self.layout)
        self.setCentralWidget(self.containerWidget)

