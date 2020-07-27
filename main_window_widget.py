from PyQt5 import QtWidgets, QtGui, QtCore
from cards_deck_widget import CardsDeck
from digital_clock import DigitalClock


class MainWindowWidget(QtWidgets.QWidget):

    def update_date(self):
        current_date = QtCore.QDate.currentDate()
        self.lbl_current_date.setText(current_date.toString(QtCore.Qt.DefaultLocaleLongDate))

    def __init__(self, parent=None):
        super().__init__(parent)

        window_width = 1200
        window_height = 800
        header_height = 120
        clock_width = 200
        clock_height = header_height
        clock_digits_color = QtGui.QColor(194, 13, 25)

        self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)

        self.setWindowTitle('Технополис ЭРА')
        self.setMinimumSize(window_width, window_height)
        self.setWindowIcon(QtGui.QIcon('images/logo_era.ico'))

        cards_deck = CardsDeck(photo_max_height=200, rows=2, columns=5)

        lbl_logo_era = QtWidgets.QLabel()
        logo = QtGui.QPixmap('images/logo_era_full2.png')
        logo_scaled = logo.scaledToHeight(header_height)
        lbl_logo_era.setPixmap(logo_scaled)

        clock = DigitalClock(clock_width, clock_height, clock_digits_color)

        current_date = QtCore.QDate.currentDate()
        self.lbl_current_date = QtWidgets.QLabel(current_date.toString(QtCore.Qt.DefaultLocaleLongDate))
        self.lbl_current_date.setAlignment(QtCore.Qt.AlignRight)
        self.lbl_current_date.setFont(QtGui.QFont('IMPACT', 18))
        palette = self.lbl_current_date.palette()
        palette.setColor(palette.Foreground, clock_digits_color)
        self.lbl_current_date.setPalette(palette)

        layout_logo = QtWidgets.QHBoxLayout()
        layout_logo.setAlignment(QtCore.Qt.AlignLeft)
        layout_logo.addWidget(lbl_logo_era)

        layout_clock_and_date = QtWidgets.QVBoxLayout()
        layout_clock_and_date.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        layout_clock_and_date.addWidget(clock)
        layout_clock_and_date.addWidget(self.lbl_current_date)

        layout_calendar_clock_date = QtWidgets.QHBoxLayout()
        layout_calendar_clock_date.setAlignment(QtCore.Qt.AlignRight)
        layout_calendar_clock_date.addLayout(layout_clock_and_date)

        layout_header = QtWidgets.QHBoxLayout()
        layout_header.setAlignment(QtCore.Qt.AlignTop)
        layout_header.addLayout(layout_logo)
        layout_header.addLayout(layout_calendar_clock_date)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.setAlignment(QtCore.Qt.AlignTop)
        layout_main.addLayout(layout_header)
        layout_main.addWidget(cards_deck)

        self.setLayout(layout_main)

        self.timer_update_date = QtCore.QTimer()
        self.timer_update_date.timeout.connect(self.update_date)
        self.timer_update_date.start(5000)
