import math
from typing import List, TYPE_CHECKING, Dict

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from src import PingData, Date
from src.widgets import OrderList
from src.widgets.pingStatsWidget import PingStatsWidget, QSizePolicy

if TYPE_CHECKING:
    from src.controllers import MainController

class PingWidgetPresenter(OrderList):
    pingsWidgets : Dict[str, PingStatsWidget]
    mainController : 'MainController'

    def __init__(self, pingDatas : List[PingData], mainController : 'MainController', twoColumns : bool = False, leftColumnCount : int = None):
        self.twoColumns = twoColumns
        self.mainController = mainController
        self.pingsWidgets = {}
        self.pingDatas : List[PingData] = list(pingDatas)

        if twoColumns:
            # Bypass Container.__init__ and set up manually for two-column mode
            QWidget.__init__(self)
            self.setAcceptDrops(False)
            self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.MinimumExpanding)

            hbox = QHBoxLayout()
            hbox.setSpacing(4)
            hbox.setContentsMargins(0, 0, 0, 0)
            self.setLayout(hbox)

            updateFn = lambda: mainController.getDataController().changePingDataOrderTwoCol(
                [w.pingData.fileName for w in self.leftContainer.getOptions()],
                [w.pingData.fileName for w in self.rightContainer.getOptions()]
            )

            self.leftContainer = OrderList(updateFn)
            self.rightContainer = OrderList(updateFn)
            self.leftContainer.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.MinimumExpanding)
            self.rightContainer.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.MinimumExpanding)
            self.leftContainer.vlayout.setSpacing(4)
            self.leftContainer.vlayout.setContentsMargins(0, 0, 0, 0)
            self.rightContainer.vlayout.setSpacing(4)
            self.rightContainer.vlayout.setContentsMargins(0, 0, 0, 0)
            hbox.addWidget(self.leftContainer)
            hbox.addWidget(self.rightContainer)

            if leftColumnCount is None:
                leftColumnCount = math.ceil(len(self.pingDatas) / 2)
            leftColumnCount = min(leftColumnCount, len(self.pingDatas))

            for pd in self.pingDatas[:leftColumnCount]:
                widget = PingStatsWidget(pd, mainController)
                self.pingsWidgets[pd.fileName] = widget
                self.leftContainer.addWidgetOption(widget)
            self.leftContainer.vlayout.addStretch()

            for pd in self.pingDatas[leftColumnCount:]:
                widget = PingStatsWidget(pd, mainController)
                self.pingsWidgets[pd.fileName] = widget
                self.rightContainer.addWidgetOption(widget)
            self.rightContainer.vlayout.addStretch()

        else:
            super().__init__(lambda : mainController.getDataController().changePingDataOrder(self.getFilepathOrder()))
            self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.MinimumExpanding)

            for pingData in self.pingDatas:
                pingWidget = PingStatsWidget(pingData, mainController)
                self.pingsWidgets[pingData.fileName] = pingWidget
                self.addWidgetOption(pingWidget)

            self.vlayout.addStretch()

        self.setStyleSheet("color: black;")

    def getFilepathOrder(self):
        if self.twoColumns:
            left = [w.pingData.fileName for w in self.leftContainer.getOptions()]
            right = [w.pingData.fileName for w in self.rightContainer.getOptions()]
            return left + right
        pingWidgets : List[PingStatsWidget] = self.getOptions()
        return [pingWidget.pingData.fileName for pingWidget in pingWidgets]

    def getPingsWidgets(self) -> Dict[PingData, PingStatsWidget]:
        return self.pingsWidgets

    @classmethod
    def getPlaceHolder(cls):
        return cls([], None)
