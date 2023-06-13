from PySide6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QComboBox,QVBoxLayout,QApplication
from PySide6.QtCore import Qt,Signal,Slot
from PySide6.QtGui import QScreen
#-------------------------------------------------------------------------------------------------------#
class newKeyForm(QWidget):
#-------------------------------------------------------------------------------------------------------#
    signal = Signal(dict)
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("creating a new key")
        self.setFixedHeight(350)
        self.setFixedWidth(300)
        #it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #name
        self.fullnameLabel = QLabel("full name : ")
        self.fullNameLineEdit= QLineEdit()
        self.fullNameLineEdit.textEdited.connect(self.textEdited)

        #email
        self.emailLabel = QLabel("email : ")
        self.emailLineEdit= QLineEdit()
        self.emailLineEdit.textEdited.connect(self.textEdited)

        #passphrease
        self.passphraseLabel = QLabel("passphrase : ")
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)

        #the length of the key
        self.lengthLabel = QLabel("length : ")
        self.lengthCombo = QComboBox()
        self.lengthCombo.addItems(["1024","2048","3072","4096"])

        #the key type of the key
        self.keyTypeLabel = QLabel("key type : ")
        self.keyTypeCombo = QComboBox()
        self.keyTypeCombo.addItems(["RSA"])

        #create_button
        self.createButton = QPushButton("create")
        self.createButton.setDisabled(True)
        self.createButton.clicked.connect(self.createClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
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

        VLayout2 = QVBoxLayout()
        VLayout2.addLayout(V_layout1)
        VLayout2.addWidget(self.createButton,alignment=Qt.AlignCenter)

        self.setLayout(VLayout2)
#-------------------------------------------------------------------------------------------------------#
    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
#-------------------------------------------------------------------------------------------------------#
    def textEdited(self):
        if self.fullNameLineEdit.text() == "" or self.passphraseLineEdit.text() == "" or self.emailLineEdit == "":
            self.createButton.setDisabled(True)
        else:
            self.createButton.setDisabled(False)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def createClicked(self):
        data = {
            "fullname" : self.fullNameLineEdit.text(),
            "email" : self.emailLineEdit.text(),
            "passphrase" : self.passphraseLineEdit.text(),
            "key_length" : self.lengthCombo.currentText(),
            "key_type" : self.keyTypeCombo.currentText()
        }
        self.signal.emit(data)
        self.createButton.setDisabled(True)
        self.close()