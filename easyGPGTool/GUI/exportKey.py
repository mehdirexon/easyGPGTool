from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QCheckBox, QApplication
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QScreen


class ExportGUI(QWidget):
    signal = Signal(bool, bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exporting a key")
        self.setFixedHeight(170)
        self.setFixedWidth(300)
        # it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)

        self.emailLabel = QLabel("Email : ")
        self.emailLineEdit = QLineEdit()
        self.emailLineEdit.textEdited.connect(self.textEdited)

        # passphrase
        self.passphraseLabel = QLabel("Passphrase : ")
        self.passphraseLabel.setHidden(True)
        self.passphraseLineEdit = QLineEdit()
        self.passphraseLineEdit.setHidden(True)
        self.passphraseLineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.passphraseLineEdit.textEdited.connect(self.textEdited)

        self.privateCB = QCheckBox("Private key")
        self.privateCB.stateChanged.connect(self.privateCBChanged)

        self.binaryCB = QCheckBox("Binary mode")

        self.exportButton = QPushButton("Export")
        self.exportButton.setDisabled(True)
        self.exportButton.clicked.connect(self.exportClicked)
        # layouts
        V_layout = QVBoxLayout()

        V_layout.addWidget(self.emailLabel, alignment=Qt.AlignTop)
        V_layout.addWidget(self.emailLineEdit)
        V_layout.addWidget(self.passphraseLabel)
        V_layout.addWidget(self.passphraseLineEdit)
        V_layout.addWidget(self.privateCB)
        V_layout.addWidget(self.binaryCB)

        V_layout.addStretch()

        V_layout.addWidget(self.exportButton, alignment=Qt.AlignCenter)
        self.setLayout(V_layout)

    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

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

    def privateCBChanged(self):
        if self.privateCB.isChecked():
            self.exportButton.setDisabled(True)
            self.setFixedHeight(220)
            self.passphraseLabel.setHidden(False)
            self.passphraseLineEdit.setHidden(False)
        else:
            self.exportButton.setDisabled(False)
            self.setFixedHeight(170)
            self.passphraseLabel.setHidden(True)
            self.passphraseLineEdit.setHidden(True)

    @Slot()
    def exportClicked(self):
        if self.privateCB.isChecked() and self.binaryCB.isChecked():
            self.signal.emit(True, False)
            self.close()
        elif self.privateCB.isChecked() and not self.binaryCB.isChecked():
            self.signal.emit(True, True)
            self.close()
        elif not self.privateCB.isChecked() and self.binaryCB.isChecked():
            self.signal.emit(False, False)
            self.close()
        else:
            self.signal.emit(False, True)
            self.close()
