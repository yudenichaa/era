from PyQt5 import QtWidgets, QtCore


class DigitalClock(QtWidgets.QLCDNumber):
    def show_time(self):
        time = QtCore.QTime.currentTime()
        self.display(time.toString('hh:mm'))

    def __init__(self, width, height, digits_color, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Часы')
        self.setMinimumSize(width, height)
        self.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.setStyleSheet('border-style: none;')
        palette = self.palette()
        palette.setColor(palette.WindowText, digits_color)
        self.setPalette(palette)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
        self.show_time()
