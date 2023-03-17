from PySide6.QtWidgets import QWidget,QPushButton,QLabel,QVBoxLayout
from PySide6.QtCore import Qt
#-------------------------------------------------------------------------------------------------------#
class aboutUsForm(QWidget):
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("about us")
        #it locks parent form when child is active
        self.setFixedHeight(120)
        self.setFixedWidth(250)
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #version_label
        self.versionLabel = QLabel()
        #author_label
        self.authorLabel = QLabel()
        #email_label
        self.emailLabel = QLabel()
        #close_button
        self.closeButton = QPushButton("close")
        self.closeButton.clicked.connect(self.closeButtonClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()
        V_layout.addWidget(self.versionLabel,alignment= Qt.AlignTop)
        V_layout.addWidget(self.authorLabel,alignment= Qt.AlignTop)
        V_layout.addWidget(self.emailLabel,alignment= Qt.AlignTop)
        V_layout.addStretch()
        V_layout.addWidget(self.closeButton,alignment=Qt.AlignCenter | Qt.AlignRight)
    
        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def getInformation(self,data):
        self.versionLabel.setText("version : " + data["version"])
        self.authorLabel.setText("author : " + data["author"])
        self.emailLabel.setText("email : " + data["author_email"])
#-------------------------------------------------------------------------------------------------------#
    def closeButtonClicked(self):
        self.close()