from PySide6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QVBoxLayout,QCheckBox
from PySide6.QtCore import Qt,Signal,Slot
#-------------------------------------------------------------------------------------------------------#
class exportForm(QWidget):
    signal = Signal(bool,bool)
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("exporting a key")
        self.setFixedHeight(170)
        self.setFixedWidth(300)
        #it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #email
        self.emailLabel = QLabel("email : ")
        self.emailLineEdit= QLineEdit()
        self.emailLineEdit.textEdited.connect(self.textEdited)
       
        #passphrase
        self.passphraseLabel = QLabel("passphrase : ")
        self.passphraseLabel.setHidden(True)
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setHidden(True)
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)

        #private_key_check_box
        self.privateCB = QCheckBox("private key")
        self.privateCB.stateChanged.connect(self.privateCBChanged)

        #binary_mode_check_box
        self.binaryCB = QCheckBox("binary mode")

        #export_button
        self.exportButton = QPushButton("export")
        self.exportButton.setDisabled(True)
        self.exportButton.clicked.connect(self.exportClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()

        V_layout.addWidget(self.emailLabel,alignment= Qt.AlignTop)
        V_layout.addWidget(self.emailLineEdit) 
        V_layout.addWidget(self.passphraseLabel)
        V_layout.addWidget(self.passphraseLineEdit)
        V_layout.addWidget(self.privateCB)
        V_layout.addWidget(self.binaryCB)

        V_layout.addStretch()

        V_layout.addWidget(self.exportButton, alignment= Qt.AlignCenter)
        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def textEdited(self):
        if not self.privateCB.isChecked():
            if self.emailLineEdit.text() == "":
                self.exportButton.setDisabled(True)
            else:
                self.exportButton.setDisabled(False)
        else:
            if self.emailLineEdit.text() == "" or self.passphraseLineEdit.text() == "":
                self.exportButton.setDisabled(True)
            else:
                self.exportButton.setDisabled(False)
#-------------------------------------------------------------------------------------------------------#
    def privateCBChanged(self):
        if self.privateCB.isChecked():
            self.exportButton.setDisabled(True)
            self.setMinimumHeight(190)
            self.passphraseLabel.setHidden(False)
            self.passphraseLineEdit.setHidden(False)
        else:
            self.exportButton.setDisabled(False)
            self.setFixedHeight(130)
            self.passphraseLabel.setHidden(True)
            self.passphraseLineEdit.setHidden(True)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def exportClicked(self):
        if self.privateCB.isChecked() and self.binaryCB.isChecked():
            self.signal.emit(True,False)
            self.close()
        elif self.privateCB.isChecked() and not self.binaryCB.isChecked():
            self.signal.emit(True,True)
            self.close()
        elif not self.privateCB.isChecked() and self.binaryCB.isChecked():
            self.signal.emit(False,False)
            self.close()
        else:
            self.signal.emit(False,True)
            self.close()