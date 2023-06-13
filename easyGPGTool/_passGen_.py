from PySide6.QtWidgets import QWidget,QLineEdit,QPushButton,QLabel,QVBoxLayout,QApplication,QComboBox
from PySide6.QtCore import Qt,Signal,Slot
from PySide6.QtGui import QScreen
#-------------------------------------------------------------------------------------------------------#
class passGenForm(QWidget):
    signal = Signal(str)
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("password generator")
        self.setFixedHeight(120)
        self.setFixedWidth(300)
        #it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #level of difficulty
        self.paswrodLVLLabel = QLabel("select your password difficulty : ")
        self.passwordLVL = QComboBox()
        self.passwordLVL.addItems(["weak","fair","strong","secure"])
        self.passwordLVL.setCurrentIndex(2)

        #decrypt_button
        self.generateButton = QPushButton("generate")
        #self.decryptButton.setDisabled(True)
        self.generateButton.clicked.connect(self.generateClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()

        V_layout.addWidget(self.paswrodLVLLabel)
        V_layout.addWidget(self.passwordLVL)

        V_layout.addStretch()
        V_layout.addWidget(self.generateButton, alignment= Qt.AlignCenter)

        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def generateClicked(self):
        self.signal.emit(self.passwordLVL.currentText())   
        self.close()