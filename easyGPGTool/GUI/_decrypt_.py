from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QScreen


class decryptForm(QWidget):
    signal = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Decrypting a file")
        self.setFixedHeight(120)
        self.setFixedWidth(300)
        # it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
        self.passphraseLabel = QLabel("Passphrase")
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)

        self.decryptButton = QPushButton("Decrypt")
        self.decryptButton.setDisabled(True)
        self.decryptButton.clicked.connect(self.decryptClicked)

        # layouts
        V_layout = QVBoxLayout()

        V_layout.addWidget(self.passphraseLabel)
        V_layout.addWidget(self.passphraseLineEdit)

        V_layout.addStretch()
        V_layout.addWidget(self.decryptButton, alignment=Qt.AlignCenter)

        self.setLayout(V_layout)

    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def textEdited(self):
        if self.passphraseLineEdit.text() == "":
            self.decryptButton.setDisabled(True)
        else:
            self.decryptButton.setDisabled(False)

    @Slot()
    def decryptClicked(self):
        self.signal.emit(True)
        self.close()
