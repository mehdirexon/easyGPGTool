from PySide6.QtWidgets import (QMainWindow,QStatusBar,QMessageBox,QTableWidget,QAbstractItemView,QTableWidgetItem,QWidget,QCheckBox,QHeaderView,QVBoxLayout,QApplication)
from PySide6.QtCore import (Slot,Qt)
from PySide6.QtGui import (QIcon,QKeySequence,QFont,QClipboard,QScreen)
from easyGPGTool.GUI.newkey import NewKeyGUI
from easyGPGTool.GUI.patchNote import PatchNoteGUI
from easyGPGTool.GUI.removeKey import RemoveKeyGUI
from easyGPGTool.GUI.aboutUs import AboutUsGUI
from easyGPGTool.GUI.encrypt import EncryptGUI
from easyGPGTool.GUI.decrypt import DecryptGUI
from easyGPGTool.GUI.exportKey import ExportGUI
from easyGPGTool.GUI.importKey import ImportGUI
from easyGPGTool.GUI.trust import TrustGUI
from easyGPGTool.GUI.passGen import PassGenGUI
from easyGPGTool.Algorithm.gpg import easyGPG as easyGPG
from colorama import Fore
from glob import glob
import os,sys

gpg = easyGPG()
class App(QMainWindow):
    appPath = os.path.normpath(__file__ + os.sep + os.pardir)
    def __init__(self):
        self.app = QApplication(sys.argv)
        super().__init__()

        # Forms
        self.NewKeyGUI = None
        self.RemoveKeyGUI = None
        self.AboutUsGUI = None
        self.PatchNoteGUI = None
        self.EncryptGUI = None
        self.DecryptGUI = None
        self.ExportGUI = None
        self.ImportGUI = None
        self.TrustGUI = None
        self.PassGenGUI = None

        # Basic configs
        self.setWindowTitle("EasyGPG Tool")
        self.setMinimumHeight(600)
        self.setMinimumWidth(1000)
        self.setWindowIcon(QIcon(App.appPath+"/Images/logo.png"))
        # Menu table
        menuItems.__showMenuItems__(self)
        # Menubar
        topBarMenu.__showTopBarItems__(self)
        # Status bar
        self.setStatusBar(QStatusBar(self))
        
    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
        
    @Slot()
    def keyGenSlot(self,data):
        try:
            logging("Recive and generate signal has been recived",Fore.GREEN)
            gpg.generate_key(data)
            QMessageBox.information(self,"Successful task","fingerprint : " + gpg.key,QMessageBox.Ok)
            menuItems.__Load__(self)
        except Exception as ex:
            logging(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"Error",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.newKey()
    @Slot()
    def keyDelSlot(self,state):
        try:
            logging("Recive and delete signal has been recived",Fore.GREEN)
            result = gpg.removeKey(self,state)
            if result.status == 'ok':
                logging("A key was deleted",Fore.GREEN)
                QMessageBox.information(self,"Successful task","key has been deleted successfully",QMessageBox.Ok)
                menuItems.__Load__(self)
        except Exception as ex:
            logging(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"Error",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.removeKey()
    @Slot()
    def encryptionSlot(self,status):
        if status is True:
            try:
                logging("Encryption signal has been recived",Fore.GREEN)
                status = gpg.encrypt(self.EncryptGUI.emailLineEdit.text())
                if status.ok is True:
                    QMessageBox.information(self,"Encrypting a file",str(status.stderr) + "\n"+ str(status.status),QMessageBox.Ok)
                    logging("An encryption task has been successfully done",Fore.GREEN)
                else:
                    raise Exception(status.stderr)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Encrypting a file",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.encrypt()
    @Slot()
    def decryptionSlot(self,status):
        if status is True:
            try:
                status = gpg.decrypt(passphrase=self.DecryptGUI.passphraseLineEdit.text())
                if status.ok is True:
                    QMessageBox.information(self,"Decrypting a file",str(status.stderr) + "\n"+ str(status.status) +"\n"+ str(status.valid) +"\n"+ str(status.trust_text),QMessageBox.Ok)
                    logging("A decryption task has been successfully done",Fore.GREEN)
                else:
                    raise Exception(status.stderr)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Decrypting a file",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.decrypt()
    @Slot()
    def exportSlot(self,status,armor):
        try:
            result = gpg.export(status,armor)
            if not result[1]:
                QMessageBox.information(self,"Exporting a key","public key has been created at\n" + result[0] + "\nsuccessfully",QMessageBox.Ok)

            elif result[1]:
                QMessageBox.information(self,"Exporting a key","private key has been created at\n" + result[0]+ "\nsuccessfully",QMessageBox.Ok)
        except Exception as ex:
            logging(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"Exporting a key",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.exportKey()
    @Slot()
    def importSlot(self,status):
        try:
            status = gpg.importKey(status)
            if status[1] == False:
                QMessageBox.information(self,"Importing a public key",status[0] + '\n',QMessageBox.Ok)
                menuItems.__Load__(self)
            elif status[1] == True:
                QMessageBox.information(self,"Importing a private key",status[0] + '\n',QMessageBox.Ok)
                menuItems.__Load__(self)
            logging("An import task has been successfully done",Fore.GREEN)
        except Exception as ex:
            logging(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"Importing a key",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.importKey()
    @Slot()
    def privateCheckBoxSlot(self):
        menuItems.__Load__(self)
    @Slot()
    def trustLevelSlot(self,mode):
        try:
            result = gpg.changeTrust(self,mode)
            QMessageBox.information(self,"Changing a key trust value",result.status + '\n' + result.stderr,QMessageBox.Ok)
            menuItems.__Load__(self)
        except Exception as ex:
            logging(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"Changing a key trust value",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.trust()
    def tableCellClicked(self,row,column):
        if column not in [2,3] :
            return
        from plyer import notification
        data = self.table.item(row,column)
        clipboard = QClipboard()
        clipboard.setText(str(data.text()))
        notification.notify(
            title = 'easyGPG tool notification',
            message = data.text()+'\nhas been copied in clipboard',
        )
#-------------------------------------------------------------------------------------------------------#

#--------------------------------------------Forms------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------#
    def removeKey(self):
        if self.RemoveKeyGUI is None:
            try:
                self.RemoveKeyGUI = RemoveKeyGUI()
                self.RemoveKeyGUI.show()
                self.RemoveKeyGUI.signal.connect(self.keyDelSlot)
                logging("Delete key form has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting remove key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.removeKey()
        else:
            try:
                self.RemoveKeyGUI.close()
                self.RemoveKeyGUI = RemoveKeyGUI()
                self.RemoveKeyGUI.show()
                self.RemoveKeyGUI.signal.connect(self.keyDelSlot)
                logging("Previous delete key form destroyed and again been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting remove key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.removeKey()
    def newKey(self):
        if self.NewKeyGUI is None:
            try:
                self.NewKeyGUI = NewKeyGUI()
                self.NewKeyGUI.show()
                self.NewKeyGUI.signal.connect(self.keyGenSlot)
                logging("New key widget has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting new key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.newKey()
        else:
            try:
                self.NewKeyGUI.close()
                self.NewKeyGUI = NewKeyGUI()
                self.NewKeyGUI.show()
                self.NewKeyGUI.signal.connect(self.keyGenSlot)
                logging("previoyus new key widget destoryed and again called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting new key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.newKey()
    def aboutUs(self):
        if self.AboutUsGUI is None:
            try:
                self.AboutUsGUI = AboutUsGUI()
                self.AboutUsGUI.show()
                logging("About us form has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting about us form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.aboutUs()
        else:
            try:
                self.AboutUsGUI.close()
                self.AboutUsGUI = AboutUsGUI()
                self.AboutUsGUI.show()
                logging("Previous about us form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting about us form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.aboutUs()
    def patchNote(self):
        if self.PatchNoteGUI is None:
            try:
                self.PatchNoteGUI = PatchNoteGUI()
                self.PatchNoteGUI.show()
                logging("Patch note form has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting patch note form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.patchNote()
        else:
            try:
                self.PatchNoteGUI.close()
                self.PatchNoteGUI = PatchNoteGUI()
                self.PatchNoteGUI.show()
                logging("Previous patch note form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting patch note form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.patchNote()
    def encrypt(self):
        if self.EncryptGUI is None:
            try:
                self.EncryptGUI = EncryptGUI()
                self.EncryptGUI.show()
                self.EncryptGUI.signal.connect(self.encryptionSlot)
                logging("Encrypt form has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting encrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.encrypt()
        else:
            try:
                self.EncryptGUI.close()
                self.EncryptGUI = EncryptGUI()
                self.EncryptGUI.show()
                self.EncryptGUI.signal.connect(self.encryptionSlot)
                logging("Previous encrypt form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting encrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.encrypt()
    def decrypt(self):
        if self.DecryptGUI is None:
            try:
                self.DecryptGUI = DecryptGUI()
                self.DecryptGUI.signal.connect(self.decryptionSlot)
                self.DecryptGUI.show()
                logging("Decrypt form has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting decrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.decrypt()
        else:
            try:
                self.DecryptGUI.close()
                self.DecryptGUI = DecryptGUI()
                self.DecryptGUI.show()
                self.DecryptGUI.signal.connect(self.decryptionSlot)
                logging("Previous decrypt form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting decrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.decrypt()
    def exportKey(self):
        if self.ExportGUI is None:
            try:
                self.ExportGUI = ExportGUI()
                self.ExportGUI.show()
                self.ExportGUI.signal.connect(self.exportSlot)
                logging("Export form has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting export form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.exportKey()
        else:
            try:
                self.ExportGUI.close()
                self.ExportGUI = ExportGUI()
                self.ExportGUI.show()
                self.ExportGUI.signal.connect(self.exportSlot)
                logging("Previous export form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting export form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.exportKey()
    def importKey(self):
        if self.ImportGUI is None:
            try:
                self.ImportGUI = ImportGUI()
                self.ImportGUI.show()
                self.ImportGUI.signal.connect(self.importSlot)
                logging("Import form has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.importKey()
        else:
            try:
                self.ImportGUI.close()
                self.ImportGUI = ImportGUI()
                self.ImportGUI.show()
                self.ImportGUI.signal.connect(self.importSlot)
                logging("Previous import form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.importKey()
    def trust(self):
        if self.TrustGUI is None:
            try:
                self.TrustGUI = TrustGUI()
                self.TrustGUI.show()
                self.TrustGUI.getFingerprints(gpg.getKeys())
                self.TrustGUI.signal.connect(self.trustLevelSlot)
                logging("Trust form has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.trust()
        else:
            try:
                self.TrustGUI.close()
                self.TrustGUI = TrustGUI()
                self.TrustGUI.show()
                self.TrustGUI.getFingerprints(gpg.getKeys())
                self.TrustGUI.signal.connect(self.trustLevelSlot)
                logging("Previous trust form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting trust form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.trust()
    def passGen(self):
        if self.PassGenGUI is None:
            try:
                self.PassGenGUI = PassGenGUI()
                self.PassGenGUI.show()
                #self.PassGenGUI.signal.connect(self.passDifficultySlot)
                logging("pass generator form has been called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.passGen()
        else:
            try:
                self.PassGenGUI.close()
                self.PassGenGUI = PassGenGUI()
                self.PassGenGUI.show()
                #self.PassGenGUI.signal.connect(self.passDifficultySlot)
                logging("previous password generator form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                logging(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting passowrd generator form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.passGen()
class topBarMenu():
    @staticmethod
    def __showTopBarItems__(QMainWindow : QMainWindow):
        QMainWindow.menuBar = QMainWindow.menuBar()
        topBarMenu.__keyMenu__(QMainWindow)
        topBarMenu.__dataProtectionMenu__(QMainWindow)
        topBarMenu.__keySharing__(QMainWindow)
        topBarMenu.__password__(QMainWindow)
        topBarMenu.__helpMenu__(QMainWindow)
    @staticmethod
    def __keyMenu__(QMainWindow : QMainWindow):
        QMainWindow.keyMenu = QMainWindow.menuBar.addMenu("Key")
        #1
        newKey = QMainWindow.keyMenu.addAction("New key")
        newKey.setShortcut(QKeySequence(QKeySequence.New))
        newKey.triggered.connect(QMainWindow.newKey)
        newKey.setIcon(QIcon(App.appPath+"/Icons/newIcon.png"))
        newKey.setStatusTip("creates a new key")
        #2
        trustKey = QMainWindow.keyMenu.addAction("Trust key")
        trustKey.triggered.connect(QMainWindow.trust)
        trustKey.setIcon(QIcon(App.appPath+"/Icons/trust.png"))
        trustKey.setStatusTip("changes trust lvl of a key")
        #3
        removeKey = QMainWindow.keyMenu.addAction("Remove key")
        removeKey.triggered.connect(QMainWindow.removeKey)
        removeKey.setShortcut(QKeySequence(QKeySequence.Delete))
        removeKey.setIcon(QIcon(App.appPath+"/Icons/removeIcon.png"))
        removeKey.setStatusTip("removes a key")
    @staticmethod
    def __dataProtectionMenu__(QMainWindow):
        QMainWindow.dataProtection = QMainWindow.menuBar.addMenu("Data protection")
        encrypt = QMainWindow.dataProtection.addAction('Encrypt')
        encrypt.triggered.connect(QMainWindow.encrypt)
        encrypt.setStatusTip("encrypts a file")
        encrypt.setIcon(QIcon(App.appPath + "/Icons/encrypt.png"))
        encrypt.setShortcut(QKeySequence('Shift+E'))
        #5
        decrypt = QMainWindow.dataProtection.addAction('Decrypt')
        decrypt.triggered.connect(QMainWindow.decrypt)
        decrypt.setStatusTip('decrypts a file')
        decrypt.setIcon(QIcon(App.appPath+'/Icons/decrypt.png'))
        decrypt.setShortcut(QKeySequence('Shift+D'))
    @staticmethod
    def __helpMenu__(QMainWindow):
        QMainWindow.helpMenu = QMainWindow.menuBar.addMenu("Help")
            #actions
        #1
        patchNote = QMainWindow.helpMenu.addAction("What's new")
        patchNote.setStatusTip("show lastest changes in the app")
        patchNote.triggered.connect(QMainWindow.patchNote)
        patchNote.setIcon(QIcon(App.appPath+'/Icons/patchNote.png'))
        #2
        aboutUs = QMainWindow.helpMenu.addAction("About us")
        aboutUs.setStatusTip("shows app and author information")
        aboutUs.setIcon(QIcon(App.appPath+'/Icons/aboutUs.png'))
        aboutUs.setShortcut(QKeySequence(QKeySequence.HelpContents))
        aboutUs.triggered.connect(QMainWindow.aboutUs)
    @staticmethod
    def __keySharing__(QMainWindow):
        QMainWindow.keySharingMenu = QMainWindow.menuBar.addMenu("Key sharing")

        exportAction = QMainWindow.keySharingMenu.addAction("Export")
        exportAction.setStatusTip("exports a key")
        exportAction.setIcon(QIcon(App.appPath+"/Icons/export.png"))
        exportAction.triggered.connect(QMainWindow.exportKey)

        importAction = QMainWindow.keySharingMenu.addAction("Import")
        importAction.setStatusTip("imports a key")
        importAction.setIcon(QIcon(App.appPath+"/Icons/import.png"))
        importAction.triggered.connect(QMainWindow.importKey)
    @staticmethod
    def __password__(QMainWindow):
        QMainWindow.passwordMenu = QMainWindow.menuBar.addMenu("Password")

        passGenAction = QMainWindow.passwordMenu.addAction("Password generator")
        passGenAction.setStatusTip("generates a password based on different difficulty")
        passGenAction.setIcon(QIcon(App.appPath+"/Icons/passGen.png"))
        passGenAction.triggered.connect(QMainWindow.passGen)

        passManagerAction = QMainWindow.passwordMenu.addAction("Password manager")
        passManagerAction.setDisabled(True)
        passManagerAction.setStatusTip("is being used to store and import or export passwords")
        passManagerAction.setIcon(QIcon(App.appPath+"/Icons/import.png"))
        #importAction.triggered.connect(QMainWindow.importKey)
class menuItems():
    @staticmethod
    def __showMenuItems__(QMainWindow):
        menuItems.__configs__(QMainWindow)
        menuItems.__setStyles__(QMainWindow)
    @staticmethod
    def __configs__(QMainWindow):
        QMainWindow.verLayout = QVBoxLayout()

        QMainWindow.privateCB = QCheckBox("private key")
        QMainWindow.table = QTableWidget(QMainWindow)
        QMainWindow.widget = QWidget()

        QMainWindow.privateCB.setStatusTip("shows private keys")
        QMainWindow.table.setStatusTip("list of keys")

        QMainWindow.table.cellClicked.connect(QMainWindow.tableCellClicked)
        QMainWindow.privateCB.stateChanged.connect(QMainWindow.privateCheckBoxSlot)

        QMainWindow.verLayout.addWidget(QMainWindow.table)
        QMainWindow.verLayout.addWidget(QMainWindow.privateCB,alignment=Qt.AlignRight)

        QMainWindow.widget.setLayout(QMainWindow.verLayout)
        QMainWindow.setCentralWidget(QMainWindow.widget)
        #QMainWindow.table.setSelectionMode(QAbstractItemView.NoSelection)
        QMainWindow.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        QMainWindow.table.setFocusPolicy(Qt.NoFocus)
        QMainWindow.table.setAlternatingRowColors(True)

        QMainWindow.table.setColumnCount(5)
        QMainWindow.table.setRowCount(len(gpg.getKeys()))

        QMainWindow.table.verticalHeader().setVisible(False)
        QMainWindow.table.setFont(QFont("Arial",12))
        QMainWindow.table.setHorizontalHeaderLabels(["Type","Name","Email","Fingerprint","Trust"])

        QMainWindow.table.horizontalHeader().setSectionResizeMode(4,QHeaderView.Fixed)
        QMainWindow.table.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
        QMainWindow.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        QMainWindow.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Fixed)
        QMainWindow.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.Fixed)

        for row,key in enumerate(gpg.getKeys()):
            type = QTableWidgetItem(str(key['type']))
            ID = QTableWidgetItem(str(key['uids'][0].split(f"<")[0]))
            email = QTableWidgetItem(str(key['uids'][0].split("<")[1].split(">")[0]))
            fp = QTableWidgetItem(str(key['fingerprint']))
            trustLvl = QTableWidgetItem(str(key['trust']))

            type.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            ID.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            email.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            fp.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            trustLvl.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            QMainWindow.table.setRowCount(len(gpg.getKeys()))

            QMainWindow.table.setItem(row,0,type)
            QMainWindow.table.setItem(row,1,ID)
            QMainWindow.table.setItem(row,2,email)
            QMainWindow.table.setItem(row,3,fp)
            QMainWindow.table.setItem(row,4,trustLvl)
    @staticmethod
    def __setStyles__(QMainWindow : QMainWindow):
        QMainWindow.table.setStyleSheet("""
        QTableWidget {
        color: black;
        font-family: "Helvetica Neue", sans-serif;
        font-size: 12px;
        vertical-align: center;
        margin-top: 35px;
        border: 2px solid #1a75ff;
        border-radius: 10px;
        min-width: 400px;
        margin-left: 10px;
        margin-right: 10px;
        margin-bottom: 25px;
        alternate-background-color: #f2f2f2;
        background-color: #e6e6e6;
    }

    QHeaderView::section {
        background-color: #1a75ff;
        border-bottom: thin solid #0059b3;
        font-family: "Helvetica Neue", sans-serif;
        border: none;
        height: 22px;
    }

    QTableWidget::item {
        padding: 5px;
    }

    QTableWidget::item:selected {
        background-color: #a6a39d;
    }

    QTableWidget::item:hover {
        background-color: #d9edf7; /* Lighter blue for better visibility */
        border: 1px solid #1a75ff;
        //border-radius: 5px;
    }

    QHeaderView::section:hover {
        background-color: #3399ff;
        border: 1px solid #0059b3;
        border-radius: 5px;
    }
        """)
    @staticmethod
    def __Load__(QMainWindow):
        QMainWindow.table.clear()
        QMainWindow.table.setHorizontalHeaderLabels(["Type","Name","Email","Fingerprint","trust"])
        if not QMainWindow.privateCB.isChecked():
            for row,key in enumerate(gpg.getKeys()):
                type = QTableWidgetItem(str(key['type']))
                ID = QTableWidgetItem(str(key['uids'][0].split(f"<")[0]))
                email = QTableWidgetItem(str(key['uids'][0].split("<")[1].split(">")[0]))
                fp = QTableWidgetItem(str(key['fingerprint']))
                trustLvl = QTableWidgetItem(str(key['trust']))

                type.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                ID.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                email.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                fp.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                trustLvl.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                QMainWindow.table.setRowCount(len(gpg.getKeys()))

                QMainWindow.table.setItem(row,0,type)
                QMainWindow.table.setItem(row,1,ID)
                QMainWindow.table.setItem(row,2,email)
                QMainWindow.table.setItem(row,3,fp)
                QMainWindow.table.setItem(row,4,trustLvl)
        else:
            for row,key in enumerate(gpg.getKeys(True)):
                type = QTableWidgetItem(str(key['type']))
                ID = QTableWidgetItem(str(key['uids'][0].split(f"<")[0]))
                email = QTableWidgetItem(str(key['uids'][0].split("<")[1].split(">")[0]))
                fp = QTableWidgetItem(str(key['fingerprint']))
                trustLvl = QTableWidgetItem(str(key['trust']))

                type.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                ID.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                email.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                fp.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                trustLvl.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

                QMainWindow.table.setRowCount(len(gpg.getKeys(True)))

                QMainWindow.table.setItem(row,0,type)
                QMainWindow.table.setItem(row,1,ID)
                QMainWindow.table.setItem(row,2,email)
                QMainWindow.table.setItem(row,3,fp)
                QMainWindow.table.setItem(row,4,trustLvl)
def run():
    import time
    start_time = time.time()
    easyGPGTool = App()
    easyGPGTool.show()
    end_time = time.time()
    elapsedTime = end_time - start_time
    print("******************Elapsed Time =>", elapsedTime,"******************")
    easyGPGTool.app.exec()
    del easyGPGTool.app
    
    
def logging(message,color):
    from datetime import datetime
    print(f"{color}[LOG]",datetime.now(),message,f" {Fore.RESET}")