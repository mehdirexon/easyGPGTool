from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QApplication, QSlider, QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen, QClipboard
from passlib.hash import pbkdf2_sha256
from passlib import pwd
from plyer import notification


class passGenForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Generator")

        self.setFixedHeight(180)
        self.setFixedWidth(500)
        # it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)

        self.paswrodLVLLabel = QLabel("Select your password difficulty : ")

        self.difficultySlider = QSlider(Qt.Horizontal, self)
        self.difficultySlider.setToolTip(
            "Adjust the difficulty level to make the generated password harder to guess or crack. Higher difficulty levels result in stronger passwords.")
        self.difficultySlider.valueChanged.connect(self.sliderValueChanged)
        self.difficultySlider.setRange(50, 300)

        self.informationLabel = QLabel("By clicking on the password box below, you can copy it")

        self.passLineEdit = QLineEdit(self)
        self.passLineEdit.mousePressEvent = self.passLineEditClicked
        self.passLineEdit.setReadOnly(True)
        # for ver0.3
        # self.saveCheckBox = QCheckBox("Save")
        # self.saveCheckBox.setToolTip("Check this box to save the generated password in the app’s database.")
        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.closeClicked)

        V_layout = QVBoxLayout()
        V_layout.addWidget(self.paswrodLVLLabel)
        V_layout.addWidget(self.difficultySlider)
        V_layout.addWidget(self.informationLabel)
        # V_layout.addWidget(self.saveCheckBox)
        V_layout.addWidget(self.passLineEdit)
        V_layout.addStretch()
        V_layout.addWidget(self.closeButton, alignment=Qt.AlignCenter)

        self.setLayout(V_layout)

    def sliderValueChanged(self, value):
        password, hashed = self.generatePassword(value)
        self.passLineEdit.setText(str(password))

    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def passLineEditClicked(self, event):
        clipboard = QClipboard()
        clipboard.setText(str(self.passLineEdit.text()))
        notification.notify(
            title='easy GPG tool notification',
            message='the password has been copied successfully',
            app_name='easy GPG tool'
        )

    def closeClicked(self):
        # self.signal.emit(self.passwordLVL.currentText())
        self.close()

    def generatePassword(self, entropy: int):
        password: str = pwd.genword(entropy)
        hashed_password: str = pbkdf2_sha256.hash(password)
        return password, hashed_password
