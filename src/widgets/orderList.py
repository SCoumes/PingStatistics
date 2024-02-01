from typing import List
from PyQt6.QtCore import Qt, QMimeData, QPoint

from PyQt6.QtGui import QDrag, QDropEvent, QDragEnterEvent, QMouseEvent
from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QApplication, QLabel

class DraggableContainer(QWidget):
    def __init__(self, content : QWidget, parent: QWidget) -> None:
        super().__init__(parent)
        self.content = content
        self.layout = QVBoxLayout()
        self.layout.addWidget(content)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def mouseMoveEvent(self, e : QMouseEvent) -> None:
        if e.buttons() == Qt.MouseButton.LeftButton:
            mimeData: QMimeData = QMimeData()
            drag: QDrag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.setPixmap(self.content.grab())
            drag.setHotSpot(e.position().toPoint() - self.rect().topLeft())
            drag.exec(Qt.DropAction.MoveAction)

class Container(QWidget):
    def __init__(self, updateFunction = None) -> None:
        super().__init__()
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setAcceptDrops(True)
        self.updateFunction = updateFunction

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        e.accept()

    def dropEvent(self, e: QDropEvent) -> None:
        pos: QPoint = e.position()
        widget: QWidget = e.source()

        for i in range(self.layout.count()):
            w: QWidget = self.layout.itemAt(i).widget()
            if pos.y() < w.y() + w.height() // 2:
                self.layout.insertWidget(i, widget)
                break

        self.updateFunction()
    
    def addTextOption(self, text : str):
        button: QPushButton = QPushButton(text, self)
        container : DraggableContainer = DraggableContainer(button, self)
        self.layout.addWidget(container)

    def addWidgetOption(self, widget : QWidget):
        container : DraggableContainer = DraggableContainer(widget, self)
        self.layout.addWidget(container)

    def clear(self):
        shortLivedWidget = QWidget()
        shortLivedWidget.setLayout(self.layout)
        self.layout = QVBoxLayout(self)

    def getOptions(self) -> List[QWidget]:
        optionList = []
        for i in range(self.layout.count()):
            container : DraggableContainer = self.layout.itemAt(i).widget()
            optionList.append(container.content)
        return optionList
