from PySide6.QtWidgets import QApplication
from ext.mainWindow import mainWindow
import sys

app = QApplication(sys.argv)
window = mainWindow(app,"GPG tool")
window.show()

app.exec()