from PySide6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QVBoxLayout
from PySide6.QtCore import Qt,Signal,Slot
#-------------------------------------------------------------------------------------------------------#
class encryptForm(QWidget):
    signal = Signal(bool)
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("encrypting a file")
        self.setFixedHeight(110)
        self.setFixedWidth(300)
        #it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #email
        self.emailLabel = QLabel("email : ")
        self.emailLineEdit= QLineEdit()
        self.emailLineEdit.textEdited.connect(self.textEdited)

        #encrypt_button
        self.encryptButton = QPushButton("check and encrypt")
        self.encryptButton.setDisabled(True)
        self.encryptButton.clicked.connect(self.encryptClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()
        V_layout.addWidget(self.emailLabel,alignment= Qt.AlignTop)
        V_layout.addWidget(self.emailLineEdit)
        V_layout.addStretch()
        V_layout.addWidget(self.encryptButton,alignment= Qt.AlignCenter)

        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def textEdited(self):
        if self.emailLineEdit.text() == "":
            self.encryptButton.setDisabled(True)
        else:
            self.encryptButton.setDisabled(False)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def encryptClicked(self):
        self.signal.emit(True)
        self.close()