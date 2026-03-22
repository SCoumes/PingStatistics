from typing import List
from PyQt6.QtCore import Qt, QMimeData, QPoint

from PyQt6.QtGui import QDrag, QDropEvent, QDragEnterEvent, QMouseEvent
from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QApplication, QLabel

class DraggableContainer(QWidget):
    def __init__(self, content : QWidget, parent: QWidget) -> None:
        super().__init__(parent)
        self.content = content
        self.vlayout = QVBoxLayout()
        self.vlayout.addWidget(content)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)

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
        self.vlayout = None
        self.clear()

        self.setAcceptDrops(True)
        self.updateFunction = updateFunction

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        e.accept()

    def dropEvent(self, e: QDropEvent) -> None:
        pos: QPoint = e.position()
        dragged: QWidget = e.source()
        source = dragged.parent()

        # Handle cross-container drop: remove from the source container
        if isinstance(source, Container) and source is not self:
            source.vlayout.removeWidget(dragged)
            dragged.setParent(self)

        # Find insert position by y-coordinate
        inserted = False
        for i in range(self.vlayout.count()):
            w: QWidget = self.vlayout.itemAt(i).widget()
            if w is not None and pos.y() < w.y() + w.height() // 2:
                self.vlayout.insertWidget(i, dragged)
                inserted = True
                break

        if not inserted:
            # Drop was below all widgets. Append before the trailing stretch spacer.
            # Use takeAt + addWidget + addItem to avoid Qt's index-shift ambiguity
            # when the dragged widget is still in this layout (same-container case).
            count = self.vlayout.count()
            last = self.vlayout.itemAt(count - 1) if count > 0 else None
            if last is not None and last.widget() is None:
                spacer = self.vlayout.takeAt(count - 1)
                self.vlayout.addWidget(dragged)
                self.vlayout.addItem(spacer)
            else:
                self.vlayout.addWidget(dragged)

        self.updateFunction()

    def addTextOption(self, text : str):
        button: QPushButton = QPushButton(text, self)
        container : DraggableContainer = DraggableContainer(button, self)
        self.vlayout.addWidget(container)

    def addWidgetOption(self, widget : QWidget):
        container : DraggableContainer = DraggableContainer(widget, self)
        self.vlayout.addWidget(container)

    def clear(self):
        if self.vlayout is not None:
            shortLivedWidget = QWidget()
            shortLivedWidget.setLayout(self.vlayout)
        self.vlayout = QVBoxLayout(self)

    def getOptions(self) -> List[QWidget]:
        optionList = []
        for i in range(self.vlayout.count()):
            container : DraggableContainer = self.vlayout.itemAt(i).widget()
            if container is not None:
                optionList.append(container.content)
        return optionList
