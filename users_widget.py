from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from TableView import TableView
from add_user_widget import AddUserWidget


class UsersWidget(QtWidgets.QDialog):
    signal_close = QtCore.pyqtSignal()

    def btn_add_user_clicked(self):
        user_widget = AddUserWidget('Добавить пользователя')
        user_widget.signal_save_user.connect(self.slot_add_user)
        user_widget.exec()

    def slot_add_user(self):
        self.table_users.model().select()

    def btn_remove_user_clicked(self):
        selected_cells = self.table_users.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Пользователи', 'Выберите пользователя для удаления')
            return

        selected_cell = selected_cells[0]
        self.table_users.model().removeRow(selected_cell.row())
        self.table_users.model().submitAll()

    def edit_user(self, selected_cell):
        model = self.table_users.model()
        name = model.data(model.createIndex(selected_cell.row(), 0))
        image_data = model.data(model.createIndex(selected_cell.row(), 1))
        image = None
        if image_data:
            image = QtGui.QPixmap()
            image.loadFromData(image_data)
        user_id = model.data(model.createIndex(selected_cell.row(), 2))
        user_widget = AddUserWidget('Редактировать пользователя', user_id=user_id, name=name, image=image)
        user_widget.signal_save_user.connect(self.slot_add_user)
        user_widget.exec()

    def slot_user_edited(self):
        self.table_users.model().select()

    def btn_edit_user_clicked(self):
        selected_cells = self.table_users.selectedIndexes()
        if len(selected_cells) == 0:
            QtWidgets.QMessageBox.information(self, 'Пользователи', 'Выберите пользователя для редактирования')
            return

        selected_cell = selected_cells[0]
        self.edit_user(selected_cell)

    def table_users_double_clicked(self, index):
        self.edit_user(index)

    def closeEvent(self, event):
        self.signal_close.emit()
        super().closeEvent(event)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Пользователи')
        self.setWindowIcon(QtGui.QIcon('images/logo_era.png'))
        self.setWindowFlags(self.windowFlags() & (~QtCore.Qt.WindowContextHelpButtonHint))

        lbl_users = QtWidgets.QLabel('Пользователи:')

        btn_add_user = QtWidgets.QPushButton('Добавить')
        btn_remove_user = QtWidgets.QPushButton('Удалить')
        btn_edit_user = QtWidgets.QPushButton('Редактировать')

        btn_add_user.clicked.connect(self.btn_add_user_clicked)
        btn_remove_user.clicked.connect(self.btn_remove_user_clicked)
        btn_edit_user.clicked.connect(self.btn_edit_user_clicked)

        model_users = QtSql.QSqlTableModel()
        model_users.setTable('User')
        model_users.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        model_users.setHeaderData(0, QtCore.Qt.Horizontal, "Имя")
        model_users.setSort(0, QtCore.Qt.AscendingOrder)
        model_users.select()

        self.table_users = TableView()
        self.table_users.setModel(model_users)
        self.table_users.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.table_users.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.table_users.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
        self.table_users.setHorizontalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_users.setVerticalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.table_users.verticalHeader().setHidden(True)
        self.table_users.horizontalHeader().setStretchLastSection(True)
        self.table_users.setColumnHidden(1, True)
        self.table_users.setColumnHidden(2, True)

        self.table_users.doubleClicked.connect(self.table_users_double_clicked)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addWidget(lbl_users)
        layout_buttons.addWidget(btn_add_user)
        layout_buttons.addWidget(btn_remove_user)
        layout_buttons.addWidget(btn_edit_user)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_buttons)
        layout_main.addWidget(self.table_users)

        self.setLayout(layout_main)
