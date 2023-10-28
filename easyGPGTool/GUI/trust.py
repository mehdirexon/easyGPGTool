from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox, QHBoxLayout, QDial, QApplication


class TrustGUI(QWidget):
    signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Changing a key trust level")
        self.setFixedHeight(300)
        self.setFixedWidth(700)
        # it locks parent form when child is active
        self.setWindowModality(Qt.ApplicationModal)

        self.fingerprintCB = QComboBox()
        self.fingerprintCB.currentIndexChanged.connect(self.fingerpintCBIndexChanged)

        self.fingerprints = []
        self.IDs = []

        self.IDLabel = QLabel()
        self.trustText = QLabel('TRUST_UNDEFINED')
        self.trust = ''

        self.changeButton = QPushButton("Change")
        self.changeButton.setEnabled(False)
        self.changeButton.clicked.connect(self.changeClicked)

        self.trustLVL = QDial()
        self.trustLVL.valueChanged.connect(self.trustLVLChanged)
        self.trustLVL.setRange(1, 5)
        self.trustLVL.setNotchesVisible(True)
        # layouts
        V_layout = QVBoxLayout()
        V_layout.addWidget(self.fingerprintCB)
        V_layout.addWidget(self.IDLabel)
        H_layout = QHBoxLayout()

        H_layout.addWidget(self.trustLVL, alignment=Qt.AlignCenter)
        H_layout.addWidget(self.trustText, alignment=Qt.AlignCenter)

        V_layout.addLayout(H_layout)
        V_layout.addStretch()
        V_layout.addWidget(self.changeButton, alignment=Qt.AlignCenter)

        self.setLayout(V_layout)

    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def trustLVLChanged(self, value):
        if len(self.fingerprints) == 0:
            self.changeButton.setDisabled(True)
        else:
            self.changeButton.setEnabled(True)
        if value == 1:
            self.trustText.setText('TRUST_UNDEFINED')
            self.trust = 'TRUST_UNDEFINED'
        elif value == 2:
            self.trustText.setText('TRUST_NEVER')
            self.trust = 'TRUST_NEVER'
        elif value == 3:
            self.trustText.setText('TRUST_MARGINAL')
            self.trust = 'TRUST_MARGINAL'
        elif value == 4:
            self.trustText.setText('TRUST_FULLY')
            self.trust = 'TRUST_FULLY'
        else:
            self.trustText.setText('TRUST_ULTIMATE')
            self.trust = 'TRUST_ULTIMATE'

    def fingerpintCBIndexChanged(self, index):
        self.IDLabel.setText(self.IDs[index][0])

    def getFingerprints(self, fp):
        for key in fp:
            self.fingerprints.append(key['fingerprint'])
            self.IDs.append(key['uids'])
        self.fingerprintCB.addItems(self.fingerprints)

    @Slot()
    def changeClicked(self):
        self.signal.emit(self.trust)
        self.close()
