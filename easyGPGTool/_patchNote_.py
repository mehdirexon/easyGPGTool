from PySide6.QtWidgets import QWidget,QPushButton,QVBoxLayout,QTextEdit,QComboBox
from PySide6.QtCore import Qt
import os,easyGPGTool
#-------------------------------------------------------------------------------------------------------#
class patchNoteForm(QWidget):
#-------------------------------------------------------------------------------------------------------#
    def __init__(self):
        super().__init__()
        self.setWindowTitle("latest patch note")
        self.setFixedWidth(1000)
        self.setFixedHeight(400)
        self.setWindowModality(Qt.ApplicationModal)
#-------------------------------------------------------------------------------------------------------#
        #text_box
        self.textBox = QTextEdit()
        self.textBox.setReadOnly(True)
        self.textBox.setFixedHeight(300)

        #version_combo_box
        self.verComboBox = QComboBox()
        self.verComboBox.currentIndexChanged.connect(self.autoLoad)
        self.verComboBox.addItems(["0.1beta","0.1"])
        self.verComboBox.setCurrentIndex(1)

        #close_button
        self.closeButton = QPushButton("close")
        self.closeButton.clicked.connect(self.closeClicked)
#-------------------------------------------------------------------------------------------------------#
        #layouts
        V_layout = QVBoxLayout()

        V_layout.addWidget(self.verComboBox,alignment=Qt.AlignTop | Qt.AlignLeft)
        V_layout.addWidget(self.textBox,alignment= Qt.AlignTop)
        V_layout.addWidget(self.closeButton,alignment=Qt.AlignCenter | Qt.AlignRight)
    
        self.setLayout(V_layout)
#-------------------------------------------------------------------------------------------------------#
    def closeClicked(self):
        self.close()
#-------------------------------------------------------------------------------------------------------#
    def autoLoad(self):
        ver = self.verComboBox.currentText()
        appPath = os.path.normpath(easyGPGTool.__file__ + os.sep + os.pardir)
        if ver == "0.1beta" :
            self.textBox.clear()
            with open(appPath+"/patch_notes/beta_patch_note.log","r") as file:
                betaPatchNote = file.read()
                self.textBox.append(betaPatchNote)
        elif ver == "0.1":
            self.textBox.clear()
            with open(appPath+"/patch_notes/0.1_patch_note.log","r") as file:
                betaPatchNote = file.read()
                self.textBox.append(betaPatchNote)
        else:
            self.textBox.clear()