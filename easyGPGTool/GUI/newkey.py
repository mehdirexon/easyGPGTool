from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QComboBox, QVBoxLayout, QApplication, QMessageBox
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QScreen
import re


class NewKeyGUI(QWidget):
    signal = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Creating a new key")
        self.setFixedHeight(400)
        self.setFixedWidth(600)
        # it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)

        self.fullnameLabel = QLabel("Full name : ")
        self.fullNameLineEdit = QLineEdit()
        self.fullNameLineEdit.textEdited.connect(self.textEdited)

        self.emailLabel = QLabel("Email : ")
        self.emailLineEdit = QLineEdit()
        self.emailLineEdit.textEdited.connect(self.textEdited)

        self.passphraseLabel = QLabel("Passphrase : ")
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)

        self.lengthLabel = QLabel("Length : ")
        self.lengthCombo = QComboBox()
        self.lengthCombo.addItems(["1024", "2048", "3072", "4096"])

        self.keyTypeLabel = QLabel("Key type : ")
        self.keyTypeCombo = QComboBox()
        self.keyTypeCombo.addItems(["RSA"])

        self.notesLineEdit = QLabel()
        self.notesLineEdit.setText(
            "Note :\nTo create a new key you must fill required fields.\n"
            "Also if you wish you can select higher length to have more secure encryption")

        self.createButton = QPushButton("Create")
        self.createButton.setDisabled(True)
        self.createButton.clicked.connect(self.createClicked)

        # layouts
        V_layout1 = QVBoxLayout()

        V_layout1.addWidget(self.fullnameLabel)
        V_layout1.addWidget(self.fullNameLineEdit)
        V_layout1.addWidget(self.emailLabel)
        V_layout1.addWidget(self.emailLineEdit)
        V_layout1.addWidget(self.passphraseLabel)
        V_layout1.addWidget(self.passphraseLineEdit)
        V_layout1.addWidget(self.lengthLabel)
        V_layout1.addWidget(self.lengthCombo)
        V_layout1.addWidget(self.keyTypeLabel)
        V_layout1.addWidget(self.keyTypeCombo)
        V_layout1.addWidget(self.notesLineEdit)
        VLayout2 = QVBoxLayout()
        VLayout2.addLayout(V_layout1)
        VLayout2.addWidget(self.createButton, alignment=Qt.AlignCenter)

        self.setLayout(VLayout2)

    def validateEmail(self):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.emailLineEdit.text()):
            return True
        else:
            return False

    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def textEdited(self):
        if self.fullNameLineEdit.text() == "" or self.passphraseLineEdit.text() == "" or self.emailLineEdit.text() == "":
            self.createButton.setDisabled(True)
        else:
            self.createButton.setDisabled(False)

    @Slot()
    def createClicked(self):
        if not self.validateEmail():
            QMessageBox.critical(self, "Validation error", "Email must be valid", QMessageBox.Ok)
            return

        data = {
            "fullname": self.fullNameLineEdit.text(),
            "email": self.emailLineEdit.text(),
            "passphrase": self.passphraseLineEdit.text(),
            "key_length": self.lengthCombo.currentText(),
            "key_type": self.keyTypeCombo.currentText()
        }
        self.signal.emit(data)
        self.createButton.setDisabled(True)
        self.close()
