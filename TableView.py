from PyQt5 import QtWidgets, QtCore


class TableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, e):
        if e.button() == QtCore.Qt.RightButton:
            self.clearSelection()
        else:
            super().mousePressEvent(e)
