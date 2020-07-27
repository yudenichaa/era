from PyQt5 import QtWidgets, QtCore, QtGui, QtSql
from user_photo import UserPhoto


class AddUserWidget(QtWidgets.QDialog):
    signal_save_user = QtCore.pyqtSignal()

    def _btn_load_image_clicked(self):
        photo_info = QtWidgets.QFileDialog.getOpenFileName(self, 'Выбрать файл', QtCore.QDir.currentPath(),
                                                           "Image Files (*.jpg *.jpeg *.png)")
        file_name = photo_info[0]
        if len(file_name) != 0:
            self.photo_file_name = file_name
            self.user_photo.set_photo(QtGui.QPixmap(file_name))

    def _btn_save_clicked(self):
        if len(self.line_name.text()) == 0:
            QtWidgets.QMessageBox.information(self, 'Добавить пользователя', 'Заполните поле "Имя"')
            return

        query = QtSql.QSqlQuery()
        if self.photo_file_name:
            file = QtCore.QFile(self.photo_file_name)
            file.open(QtCore.QIODevice.ReadOnly)
            byte_array = file.readAll()
            if self.user_id:
                query.prepare(
                    "UPDATE User SET name ='" + self.line_name.text() + "', image = :imageData WHERE id = " + str(
                        self.user_id) + ";")
            else:
                query.prepare("INSERT INTO User (name, image) VALUES ('" + self.line_name.text() + "', :imageData);")
            query.bindValue(":imageData", byte_array)
        else:
            if self.user_id:
                query.prepare(
                    "UPDATE User SET name ='" + self.line_name.text() + "' WHERE id = " + str(self.user_id) + ";")
            else:
                query.prepare("INSERT INTO User (name) VALUES ('" + self.line_name.text() + "');")

        query.exec()
        self.close()
        self.signal_save_user.emit()

    def _btn_cancel_clicked(self):
        self.close()

    def __init__(self, headline, user_id=None, name=None, image=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle(headline)
        self.setWindowIcon(QtGui.QIcon('images/logo_era.png'))
        self.setWindowFlags(self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint))

        self.user_id = user_id
        self.photo_file_name = None

        lbl_name = QtWidgets.QLabel('Имя:')
        self.line_name = QtWidgets.QLineEdit()
        if name:
            self.line_name.setText(name)
        lbl_image = QtWidgets.QLabel('Фото:')
        btn_load_image = QtWidgets.QPushButton('Выбрать фото')
        self.user_photo = UserPhoto(photo_max_height=190)
        if image:
            self.user_photo.set_photo(image)
        else:
            self.user_photo.set_no_photo()

        btn_save = QtWidgets.QPushButton('Сохранить')
        btn_cancel = QtWidgets.QPushButton('Отмена')

        btn_load_image.clicked.connect(self._btn_load_image_clicked)
        btn_save.clicked.connect(self._btn_save_clicked)
        btn_cancel.clicked.connect(self._btn_cancel_clicked)

        layout_data = QtWidgets.QFormLayout()
        layout_data.addRow(lbl_name, self.line_name)
        layout_data.addRow(lbl_image, btn_load_image)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.setAlignment(QtCore.Qt.AlignRight)
        layout_buttons.addWidget(btn_save)
        layout_buttons.addWidget(btn_cancel)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_data)
        layout_main.addWidget(self.user_photo)
        layout_main.addLayout(layout_buttons)

        self.setLayout(layout_main)
