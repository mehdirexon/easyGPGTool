from PySide6.QtWidgets import QWidget,QPushButton,QVBoxLayout,QTextEdit
from PySide6.QtCore import Qt
#-------------------------------------------------------------------------------------------------------#
class showAllForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("showing all the keys")
        self.setFixedHeight(400)
        self.setFixedWidth(600)
        #it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #text box
        self.textBox = QTextEdit()
        self.textBox.setReadOnly(True)

        #close button
        self.closeButton = QPushButton("close")        
        self.closeButton.clicked.connect(self.closeClicked)
#-------------------------------------------------------------------------------------------------------#        
        #layouts
        V_layout = QVBoxLayout()
        V_layout.addWidget(self.textBox)
        V_layout.addWidget(self.closeButton,alignment=Qt.AlignRight)

        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def closeClicked(self):
        self.close()