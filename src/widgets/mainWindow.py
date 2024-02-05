from typing import List, TYPE_CHECKING

from time import sleep
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QPushButton, QScrollArea
from PyQt6.QtWidgets import QMainWindow, QLabel, QToolBar
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from src.widgets.pingWidgetsPresenter import PingWidgetPresenter

if TYPE_CHECKING:
    from src.controllers import MainController

class MainWindow(QMainWindow):
    mainController : 'MainController'
    pingPresenter : 'PingWidgetPresenter'
    addPingStater : QAction
    skipRedraw : bool
    
    def __init__(self):
        # Create a toolbar
        super().__init__()
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)
        self.addPingStater = toolbar.addAction("Add ping stater")
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.skipRedraw = True
        self.resizeTimer = QTimer()
        self.resizeTimer.setSingleShot(True)
        self.resizeTimer.timeout.connect(self.onResizeDone)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if not self.skipRedraw:
            self.resizeTimer.start(100)

    def onResizeDone(self):
        self.mainController.redraw()
        
    def redrawLayout(self):
        self.vlayout = QVBoxLayout()
        self.containerWidget = QWidget()
        self.containerWidget.setLayout(self.vlayout)
        self.vlayout.addWidget(self.pingPresenter)
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollArea.setWidget(self.containerWidget)
        self.setCentralWidget(scrollArea)

