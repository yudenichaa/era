from PyQt5 import QtWidgets, QtGui, QtCore


class CardRequest(QtWidgets.QDialog):
    signal_save_request = QtCore.pyqtSignal(str, int)

    def _btn_add_request_clicked(self):
        if len(self.line_name.text()) == 0:
            QtWidgets.QMessageBox.information(self, 'Электронная приёмная', 'Заполните поле "Имя"')
            return
        self.close()
        self.signal_save_request.emit(self.line_name.text(), self.card_id)

    def _btn_cancel_clicked(self):
        self.close()

    def __init__(self, knows_users, card_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создать заявку")
        self.setWindowIcon(QtGui.QIcon('images/logo_era.png'))
        self.setWindowFlags(self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint))

        self.card_id = card_id

        lbl_name = QtWidgets.QLabel('Имя:')
        self.line_name = QtWidgets.QLineEdit()
        btn_add_request = QtWidgets.QPushButton('Добавить')
        btn_cancel = QtWidgets.QPushButton('Отмена')

        btn_add_request.clicked.connect(self._btn_add_request_clicked)
        btn_cancel.clicked.connect(self._btn_cancel_clicked)

        completer = QtWidgets.QCompleter(knows_users)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.line_name.setCompleter(completer)

        layout_name = QtWidgets.QHBoxLayout()
        layout_name.addWidget(lbl_name)
        layout_name.addWidget(self.line_name)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addWidget(btn_add_request)
        layout_buttons.addWidget(btn_cancel)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_name)
        layout_main.addLayout(layout_buttons)

        self.setLayout(layout_main)
