from PySide6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QVBoxLayout,QMessageBox
from PySide6.QtCore import Qt,Signal,Slot
#-------------------------------------------------------------------------------------------------------#
class removeKeyForm(QWidget):
#-------------------------------------------------------------------------------------------------------#
    signal = Signal(dict)
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("removing a new key")
        self.setFixedHeight(150)
        self.setFixedWidth(300)
        #it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #fingerprint
        self.fingerprintLabel = QLabel("fingerprint : ")
        self.fingerprintLineEdit= QLineEdit()
        self.fingerprintLineEdit.textEdited.connect(self.textEdited)

        #passphrase
        self.passphraseLabel = QLabel("passphrase : ")
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)

        #remove_button
        self.removeButton = QPushButton("remove")
        self.removeButton.setDisabled(True)
        self.removeButton.clicked.connect(self.removeClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()
        V_layout.addWidget(self.fingerprintLabel)
        V_layout.addWidget(self.fingerprintLineEdit)
        V_layout.addWidget(self.passphraseLabel)
        V_layout.addWidget(self.passphraseLineEdit)
        V_layout.addStretch()
        V_layout.addWidget(self.removeButton, alignment= Qt.AlignCenter)

        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def textEdited(self):
        #it checks disables all the line edits if they were empty
        if self.fingerprintLineEdit.text() == "" or self.passphraseLineEdit.text() == "":
            self.removeButton.setDisabled(True)
        else:
            self.removeButton.setDisabled(False)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def removeClicked(self):
        self.signal.emit({"fingerprint" : self.fingerprintLineEdit.text(),"passphrase": self.passphraseLineEdit.text()})
        self.close()