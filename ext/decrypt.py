from PySide6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QVBoxLayout
from PySide6.QtCore import Qt,Signal,Slot
#-------------------------------------------------------------------------------------------------------#
class decryptForm(QWidget):
    signal = Signal(bool)
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("decrypting a file")
        self.setFixedHeight(100)
        self.setFixedWidth(300)
        #it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #passphrase
        self.passphraseLabel = QLabel("passphrase")
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)

        #decrypt_button
        self.decryptButton = QPushButton("check and decrypt")
        self.decryptButton.setDisabled(True)
        self.decryptButton.clicked.connect(self.decryptClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()

        V_layout.addWidget(self.passphraseLabel)
        V_layout.addWidget(self.passphraseLineEdit)

        V_layout.addStretch()
        V_layout.addWidget(self.decryptButton, alignment= Qt.AlignCenter)

        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def textEdited(self):
        if self.passphraseLineEdit.text() == "":
            self.decryptButton.setDisabled(True)
        else:
            self.decryptButton.setDisabled(False)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def decryptClicked(self):
        self.signal.emit(True)
        self.close()