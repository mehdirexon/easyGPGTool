from PySide6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QVBoxLayout,QCheckBox,QFileDialog,QHBoxLayout
from PySide6.QtCore import Qt,Signal,Slot
import os
#-------------------------------------------------------------------------------------------------------#
class importForm(QWidget):
    signal = Signal(bool)
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("importing a key")
        self.setFixedHeight(135)
        self.setFixedWidth(400)
        #it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #email
        self.keyPathLabel = QLabel("public file path : ")

        self.keyPathLineEdit= QLineEdit()
        self.keyPathLineEdit.setReadOnly(True)
        self.keyPathLineEdit.textEdited.connect(self.textEdited)

        #open_button
        self.openDialog = QPushButton("open")
        self.openDialog.clicked.connect(self.openDialogClicked)

        #passphrase
        self.passphraseLabel = QLabel("passphrase : ")
        self.passphraseLabel.setHidden(True)
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setHidden(True)
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)
        
        #check_box
        self.privateKeyCB = QCheckBox("private key")
        self.privateKeyCB.stateChanged.connect(self.privateKeyCBChanged)

        #import_button
        self.importButton = QPushButton("import")
        self.importButton.setDisabled(True)
        self.importButton.clicked.connect(self.importClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()
        H_layout = QHBoxLayout()

        V_layout.addWidget(self.keyPathLabel,alignment= Qt.AlignTop)

        H_layout.addWidget(self.keyPathLineEdit)
        H_layout.addWidget(self.openDialog)

        V_layout.addLayout(H_layout)
        V_layout.addWidget(self.passphraseLabel)
        V_layout.addWidget(self.passphraseLineEdit)
        V_layout.addWidget(self.privateKeyCB)
        V_layout.addStretch()
        V_layout.addWidget(self.importButton, alignment= Qt.AlignCenter)

        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def textEdited(self):
        if not self.privateKeyCB.isChecked():
            if self.keyPathLineEdit.text() == "":                
                self.importButton.setDisabled(True)
            else:
                self.importButton.setDisabled(False)
        else:
            if self.keyPathLineEdit.text() == "" or self.passphraseLineEdit.text() == "": 
                self.importButton.setDisabled(True)
            else:
                self.importButton.setDisabled(False)
#-------------------------------------------------------------------------------------------------------#
    def openDialogClicked(self):
        selectedPath = QFileDialog.getOpenFileName(self,"select your file","/home/" + os.getlogin() + "/Desktop",filter="*.asc")
        self.keyPathLineEdit.setText(selectedPath[0])
        if not self.privateKeyCB.isChecked():
            self.importButton.setEnabled(True)
        else:
            self.importButton.setEnabled(False)
#-------------------------------------------------------------------------------------------------------#
    def privateKeyCBChanged(self):
        if self.privateKeyCB.isChecked():
            self.importButton.setDisabled(True)
            self.setMinimumHeight(190)
            self.keyPathLabel.setText("private key path")
            self.passphraseLabel.setHidden(False)
            self.passphraseLineEdit.setHidden(False)
        else:
            self.importButton.setDisabled(False)
            self.keyPathLabel.setText("public key path")
            self.setFixedHeight(130)
            self.passphraseLabel.setHidden(True)
            self.passphraseLineEdit.setHidden(True)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def importClicked(self):
        if self.privateKeyCB.isChecked():
            self.signal.emit(True)
            self.close()
        else:
            self.signal.emit(False)
            self.close()