from PySide6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QVBoxLayout,QCheckBox,QApplication
from PySide6.QtCore import Qt,Signal,Slot
from PySide6.QtGui import QScreen
#-------------------------------------------------------------------------------------------------------#
class removeKeyForm(QWidget):
#-------------------------------------------------------------------------------------------------------#
    signal = Signal(bool)
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("removing a new key")
        self.setFixedHeight(130)
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
        self.passphraseLabel.setHidden(True)
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setHidden(True)
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)

        #private key CB
        self.privateKeyCB = QCheckBox("private key")
        self.privateKeyCB.stateChanged.connect(self.privateKeyCBChanged)

        #remove_button
        self.removeButton = QPushButton("remove")
        self.removeButton.setDisabled(True)
        self.removeButton.clicked.connect(self.removeClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()
        V_layout.addWidget(self.fingerprintLabel)
        V_layout.addWidget(self.fingerprintLineEdit)
        V_layout.addWidget(self.privateKeyCB)
        V_layout.addWidget(self.passphraseLabel)
        V_layout.addWidget(self.passphraseLineEdit)
        V_layout.addStretch()
        V_layout.addWidget(self.removeButton, alignment= Qt.AlignCenter)

        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
#-------------------------------------------------------------------------------------------------------#
    def privateKeyCBChanged(self):
        if self.privateKeyCB.isChecked():
            self.removeButton.setDisabled(True)
            self.setFixedHeight(190)
            self.passphraseLabel.setHidden(False)
            self.passphraseLineEdit.setHidden(False)
        else:
            self.setFixedHeight(130)
            if self.fingerprintLineEdit.text() != "":
                self.removeButton.setDisabled(False)
            else:
                self.removeButton.setDisabled(True)
            self.passphraseLineEdit.clear()
            self.passphraseLabel.setHidden(True)
            self.passphraseLineEdit.setHidden(True)
    def textEdited(self):
        if not self.privateKeyCB.isChecked():
            if self.fingerprintLineEdit.text() == "":                
                self.removeButton.setDisabled(True)
            else:
                self.removeButton.setDisabled(False)
        else:
            if self.fingerprintLineEdit.text() == "" or self.passphraseLineEdit.text() == "": 
                self.removeButton.setDisabled(True)
            else:
                self.removeButton.setDisabled(False)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def removeClicked(self):
        if self.privateKeyCB.isChecked():
            self.signal.emit(True)
            self.close()
        else:
            self.signal.emit(False)
            self.close()