from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class WebBridge(QObject):

    executionFinished = pyqtSignal(str, str)
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    @pyqtSlot(str)
    def runBlock(self, elem_id):
        output = self.controller.execute_block(elem_id)
        self.executionFinished.emit(elem_id, output)
