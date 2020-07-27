from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from PyQt5.QtMultimedia import QSound
from card_widget import CardWidget
from users_widget import UsersWidget
from card_request import CardRequest


class CardsDeck(QtWidgets.QWidget):

    @staticmethod
    def _load_data():
        query = QtSql.QSqlQuery()
        query.exec("SELECT number, name, status FROM Card;")
        data = {}
        while query.next():
            data[query.value(0)] = (query.value(1), query.value(2))
        return data

    @staticmethod
    def _load_knows_users():
        knows_users = {}
        query = QtSql.QSqlQuery()
        query.exec("SELECT name, image FROM User")
        while query.next():
            image_data = query.value(1)
            image = None
            if image_data:
                image = QtGui.QPixmap()
                image.loadFromData(image_data)
            knows_users[query.value(0)] = image
        return knows_users

    def btn_users_clicked(self):
        users = UsersWidget()
        users.signal_close.connect(self.slot_update_users)
        users.exec()

    def slot_update_users(self):
        self.known_users = CardsDeck._load_knows_users()
        for card in self.cards:
            user_photo = self.known_users.get(card.get_user_name(), None)
            if user_photo:
                card.change_photo(user_photo)

    def slot_card_add_request(self, card_id):
        users = self.known_users.keys()
        request = CardRequest(users, card_id)
        request.signal_save_request.connect(self.slot_card_set_user)
        request.exec()

    def slot_card_set_user(self, user_name, card_id):
        card = self.cards[card_id]
        user_photo = self.known_users.get(user_name, None)
        card.set_user(user_name, user_photo)
        QSound.play('sounds/request.wav')

    def __init__(self, photo_max_height, rows=2, columns=4, parent=None):
        super().__init__(parent)

        self.known_users = CardsDeck._load_knows_users()

        btn_users = QtWidgets.QPushButton('Пользователи')
        btn_users.setMinimumWidth(100)
        btn_users.clicked.connect(self.btn_users_clicked)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.setAlignment(QtCore.Qt.AlignRight)
        layout_buttons.addWidget(btn_users)

        layout_cards = QtWidgets.QVBoxLayout()
        layout_cards.setAlignment(QtCore.Qt.AlignTop)
        data = CardsDeck._load_data()
        self.cards = []
        for i in range(rows):
            layout_row = QtWidgets.QHBoxLayout()
            layout_row.setAlignment(QtCore.Qt.AlignTop)
            for j in range(columns):
                card_id = columns * i + j
                user_name = data[card_id][0]
                user_image = self.known_users.get(user_name, None)
                card = CardWidget(card_id=card_id, photo_max_height=photo_max_height,
                                  user_name=data[card_id][0], user_photo=user_image,
                                  status=data[card_id][1])
                card.signal_set_user.connect(self.slot_card_add_request)
                self.cards.append(card)
                layout_row.addWidget(card)
            layout_cards.addLayout(layout_row)

        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_cards)
        layout_main.addStretch()
        layout_main.addLayout(layout_buttons)

        self.setLayout(layout_main)
