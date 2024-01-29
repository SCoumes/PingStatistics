import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from src import MainWindow
from src.controllers import MainController

def main():
    app = QApplication(sys.argv)
    app_icon = QIcon("icon.png")
    app.setWindowIcon(app_icon)

    window = MainWindow()
    window.show()
    mainController = MainController(window)
    mainController.initApp()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
