from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen


class AboutUsGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About us")
        # it locks parent form when child is active
        self.setFixedHeight(120)
        self.setFixedWidth(250)
        self.setWindowModality(Qt.ApplicationModal)

        self.versionLabel = QLabel()
        self.authorLabel = QLabel()
        self.emailLabel = QLabel()
        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.closeButtonClicked)

        # layouts
        V_layout = QVBoxLayout()
        V_layout.addWidget(self.versionLabel, alignment=Qt.AlignTop)
        V_layout.addWidget(self.authorLabel, alignment=Qt.AlignTop)
        V_layout.addWidget(self.emailLabel, alignment=Qt.AlignTop)
        V_layout.addStretch()
        V_layout.addWidget(self.closeButton, alignment=Qt.AlignCenter | Qt.AlignRight)

        self.setLayout(V_layout)

    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

    def getInformation(self, data):
        self.versionLabel.setText("Version : " + data["version"])
        self.authorLabel.setText("Author : " + data["author"])
        self.emailLabel.setText("Email : " + data["author_email"])

    def closeButtonClicked(self):
        self.close()
