from PySide6.QtWidgets import (QMainWindow,QStatusBar,QMessageBox,QFileDialog,QTableWidget,QAbstractItemView,QTableWidgetItem,QWidget,QCheckBox,QHeaderView,QVBoxLayout,QApplication,QSystemTrayIcon)
from PySide6.QtCore import (Slot,Qt)
from PySide6.QtGui import (QIcon,QKeySequence,QFont,QClipboard,QScreen)
from datetime import datetime
from easyGPGTool.GUI._newkey_ import newKeyForm
from easyGPGTool.GUI._patchNote_ import patchNoteForm
from easyGPGTool.GUI._removeKey_ import removeKeyForm
from easyGPGTool.GUI._aboutUs_ import aboutUsForm
from easyGPGTool.GUI._encrypt_ import encryptForm
from easyGPGTool.GUI._decrypt_ import decryptForm
from easyGPGTool.GUI._export_ import exportForm
from easyGPGTool.GUI._import_ import importForm
from easyGPGTool.GUI._trust_ import trustForm
from easyGPGTool.GUI._passGen_ import passGenForm
from easyGPGTool.Algorithm.GPG import GPG
from plyer import notification
from colorama import Fore
from glob import glob
import os,sys


gpg = GPG()
appPath = os.path.normpath(__file__ + os.sep + os.pardir)
class app(QMainWindow):
    __information__ = {"version" : "0.2beta","author" : "Mehdi Ghazanfari","author_email" : "mehdirexon@gmail.com"}
    def __init__(self):
        #basics
        self.app = QApplication(sys.argv)
        super().__init__()
        #forms
        self.newKeyForm = None
        self.removeKeyForm = None
        self.aboutUsForm = None
        self.patchNoteForm = None
        self.encryptForm = None
        self.decryptForm = None
        self.exportForm = None
        self.importForm = None
        self.trustForm = None
        self.passGenForm = None

        #basic configs
        self.setWindowTitle("easyGPG tool")
        self.setMinimumHeight(600)
        self.setMinimumWidth(1000)
        self.setWindowIcon(QIcon(appPath+"/images/logo.png"))
        #menu_table
        menuItems.__showMenuItems__(self)
        #menubar
        topBarMenu.__showTopBarItems__(self)
        #status bar
        self.setStatusBar(QStatusBar(self))
    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
    def sendLog(self,txt_or_exception,status):
        print(f"{status}[LOG]",datetime.now(),txt_or_exception,f" {Fore.RESET}")
    @Slot()
    def keyGenSlot(self,data):
        try:
            self.sendLog("Recive and generate signal has been recived",Fore.GREEN)
            gpg.generate_key(data)
            QMessageBox.information(self,"Successful task","fingerprint : " + gpg.key,QMessageBox.Ok)
            menuItems.__Load__(self)
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"Error",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.newKey()
    @Slot()
    def keyDelSlot(self,state):
        try:
            self.sendLog("Recive and delete signal has been recived",Fore.GREEN)
            result = gpg.removeKey(self,state)
            if result.status == 'ok':
                self.sendLog("A key was deleted",Fore.GREEN)
                QMessageBox.information(self,"Successful task","key has been deleted successfully",QMessageBox.Ok)
                menuItems.__Load__(self)
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"Error",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.removeKey()
    @Slot()
    def encryptionSlot(self,status):
        if status is True:
            try:
                self.sendLog("Encryption signal has been recived",Fore.GREEN)
                status = gpg.encrypt(self.encryptForm.emailLineEdit.text())
                if status.ok is True:
                    QMessageBox.information(self,"Encrypting a file",str(status.stderr) + "\n"+ str(status.status),QMessageBox.Ok)
                    self.sendLog("An encryption task has been successfully done",Fore.GREEN)
                else:
                    raise Exception(status.stderr)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Encrypting a file",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.encrypt()
    @Slot()
    def decryptionSlot(self,status):
        if status is True:
            try:
                status = gpg.decrypt(passphrase=self.decryptForm.passphraseLineEdit.text())
                if status.ok is True:
                    QMessageBox.information(self,"Decrypting a file",str(status.stderr) + "\n"+ str(status.status) +"\n"+ str(status.valid) +"\n"+ str(status.trust_text),QMessageBox.Ok)
                    self.sendLog("A decryption task has been successfully done",Fore.GREEN)
                else:
                    raise Exception(status.stderr)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
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
            self.sendLog(str(ex),Fore.RED)
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
            self.sendLog("An import task has been successfully done",Fore.GREEN)
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
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
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"Changing a key trust value",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.trust()
    def tableCellClicked(self,row,column):
        if column not in [2,3] :
            return
        data = self.table.item(row,column)
        clipboard = QClipboard()
        clipboard.setText(str(data.text()))
        notification.notify(
            title = 'GPG tool notification',
            message = data.text()+'\nhas been copied in clipboard',
        )
#-------------------------------------------------------------------------------------------------------#

#--------------------------------------------Forms------------------------------------------------------#

#-------------------------------------------------------------------------------------------------------#
    def removeKey(self):
        if self.removeKeyForm is None:
            try:
                self.removeKeyForm = removeKeyForm()
                self.removeKeyForm.show()
                self.removeKeyForm.signal.connect(self.keyDelSlot)
                self.sendLog("Delete key form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting remove key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.removeKey()
        else:
            try:
                self.removeKeyForm.close()
                self.removeKeyForm = removeKeyForm()
                self.removeKeyForm.show()
                self.removeKeyForm.signal.connect(self.keyDelSlot)
                self.sendLog("Previous delete key form destroyed and again been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting remove key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.removeKey()
    def newKey(self):
        if self.newKeyForm is None:
            try:
                self.newKeyForm = newKeyForm()
                self.newKeyForm.show()
                self.newKeyForm.signal.connect(self.keyGenSlot)
                self.sendLog("New key widget has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting new key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.newKey()
        else:
            try:
                self.newKeyForm.close()
                self.newKeyForm = newKeyForm()
                self.newKeyForm.show()
                self.newKeyForm.signal.connect(self.keyGenSlot)
                self.sendLog("previoyus new key widget destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting new key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.newKey()
    def aboutUs(self):
        if self.aboutUsForm is None:
            try:
                self.aboutUsForm = aboutUsForm()
                self.aboutUsForm.show()
                self.aboutUsForm.getInformation(self.__information__)
                self.sendLog("About us form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting about us form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.aboutUs()
        else:
            try:
                self.aboutUsForm.close()
                self.aboutUsForm = aboutUsForm()
                self.aboutUsForm.show()
                self.aboutUsForm.getInformation(self.__information__)
                self.sendLog("Previous about us form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting about us form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.aboutUs()
    def patchNote(self):
        if self.patchNoteForm is None:
            try:
                self.patchNoteForm = patchNoteForm()
                self.patchNoteForm.show()
                self.sendLog("Patch note form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting patch note form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.patchNote()
        else:
            try:
                self.patchNoteForm.close()
                self.patchNoteForm = patchNoteForm()
                self.patchNoteForm.show()
                self.sendLog("Previous patch note form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting patch note form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.patchNote()
    def encrypt(self):
        if self.encryptForm is None:
            try:
                self.encryptForm = encryptForm()
                self.encryptForm.show()
                self.encryptForm.signal.connect(self.encryptionSlot)
                self.sendLog("Encrypt form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting encrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.encrypt()
        else:
            try:
                self.encryptForm.close()
                self.encryptForm = encryptForm()
                self.encryptForm.show()
                self.encryptForm.signal.connect(self.encryptionSlot)
                self.sendLog("Previous encrypt form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting encrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.encrypt()
    def decrypt(self):
        if self.decryptForm is None:
            try:
                self.decryptForm = decryptForm()
                self.decryptForm.signal.connect(self.decryptionSlot)
                self.decryptForm.show()
                self.sendLog("Decrypt form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting decrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.decrypt()
        else:
            try:
                self.decryptForm.close()
                self.decryptForm = decryptForm()
                self.decryptForm.show()
                self.decryptForm.signal.connect(self.decryptionSlot)
                self.sendLog("Previous decrypt form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting decrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.decrypt()
    def exportKey(self):
        if self.exportForm is None:
            try:
                self.exportForm = exportForm()
                self.exportForm.show()
                self.exportForm.signal.connect(self.exportSlot)
                self.sendLog("Export form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting export form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.exportKey()
        else:
            try:
                self.exportForm.close()
                self.exportForm = exportForm()
                self.exportForm.show()
                self.exportForm.signal.connect(self.exportSlot)
                self.sendLog("Previous export form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting export form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.exportKey()
    def importKey(self):
        if self.importForm is None:
            try:
                self.importForm = importForm()
                self.importForm.show()
                self.importForm.signal.connect(self.importSlot)
                self.sendLog("Import form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.importKey()
        else:
            try:
                self.importForm.close()
                self.importForm = importForm()
                self.importForm.show()
                self.importForm.signal.connect(self.importSlot)
                self.sendLog("Previous import form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.importKey()
    def trust(self):
        if self.trustForm is None:
            try:
                self.trustForm = trustForm()
                self.trustForm.show()
                self.trustForm.getFingerprints(gpg.getKeys())
                self.trustForm.signal.connect(self.trustLevelSlot)
                self.sendLog("Trust form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.trust()
        else:
            try:
                self.trustForm.close()
                self.trustForm = trustForm()
                self.trustForm.show()
                self.trustForm.getFingerprints(gpg.getKeys())
                self.trustForm.signal.connect(self.trustLevelSlot)
                self.sendLog("Previous trust form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"Starting trust form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.trust()
    def passGen(self):
        if self.passGenForm is None:
            try:
                self.passGenForm = passGenForm()
                self.passGenForm.show()
                #self.passGenForm.signal.connect(self.passDifficultySlot)
                self.sendLog("pass generator form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.passGen()
        else:
            try:
                self.passGenForm.close()
                self.passGenForm = passGenForm()
                self.passGenForm.show()
                #self.passGenForm.signal.connect(self.passDifficultySlot)
                self.sendLog("previous password generator form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting passowrd generator form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.passGen()

#other classes
class topBarMenu():
    @staticmethod
    def __showTopBarItems__(QMainWindow):
        QMainWindow.menuBar = QMainWindow.menuBar()
        topBarMenu.__keyMenu__(QMainWindow)
        topBarMenu.__dataProtectionMenu__(QMainWindow)
        topBarMenu.__keySharing__(QMainWindow)
        topBarMenu.__password__(QMainWindow)
        topBarMenu.__helpMenu__(QMainWindow)
    @staticmethod
    def __keyMenu__(QMainWindow):
        QMainWindow.keyMenu = QMainWindow.menuBar.addMenu("Key")
        #1
        newKey = QMainWindow.keyMenu.addAction("New key")
        newKey.setShortcut(QKeySequence(QKeySequence.New))
        newKey.triggered.connect(QMainWindow.newKey)
        newKey.setIcon(QIcon(appPath+"/icons/newIcon.png"))
        newKey.setStatusTip("creates a new key")
        #2
        trustKey = QMainWindow.keyMenu.addAction("Trust key")
        trustKey.triggered.connect(QMainWindow.trust)
        trustKey.setIcon(QIcon(appPath+"/icons/trust.png"))
        trustKey.setStatusTip("changes trust lvl of a key")
        #3
        removeKey = QMainWindow.keyMenu.addAction("Remove key")
        removeKey.triggered.connect(QMainWindow.removeKey)
        removeKey.setShortcut(QKeySequence(QKeySequence.Delete))
        removeKey.setIcon(QIcon(appPath+"/icons/removeIcon.png"))
        removeKey.setStatusTip("removes a key")
    @staticmethod
    def __dataProtectionMenu__(QMainWindow):
        QMainWindow.dataProtection = QMainWindow.menuBar.addMenu("Data protection")
        encrypt = QMainWindow.dataProtection.addAction('Encrypt')
        encrypt.triggered.connect(QMainWindow.encrypt)
        encrypt.setStatusTip("encrypts a file")
        encrypt.setIcon(QIcon(appPath + "/icons/encrypt.png"))
        encrypt.setShortcut(QKeySequence('Shift+E'))
        #5
        decrypt = QMainWindow.dataProtection.addAction('Decrypt')
        decrypt.triggered.connect(QMainWindow.decrypt)
        decrypt.setStatusTip('decrypts a file')
        decrypt.setIcon(QIcon(appPath+'/icons/decrypt.png'))
        decrypt.setShortcut(QKeySequence('Shift+D'))
    @staticmethod
    def __helpMenu__(QMainWindow):
        QMainWindow.helpMenu = QMainWindow.menuBar.addMenu("Help")
            #actions
        #1
        patchNote = QMainWindow.helpMenu.addAction("What's new")
        patchNote.setStatusTip("show lastest changes in the app")
        patchNote.triggered.connect(QMainWindow.patchNote)
        patchNote.setIcon(QIcon(appPath+'/icons/patchNote.png'))
        #2
        aboutUs = QMainWindow.helpMenu.addAction("About us")
        aboutUs.setStatusTip("shows app and author information")
        aboutUs.setIcon(QIcon(appPath+'/icons/aboutUs.png'))
        aboutUs.setShortcut(QKeySequence(QKeySequence.HelpContents))
        aboutUs.triggered.connect(QMainWindow.aboutUs)
    @staticmethod
    def __keySharing__(QMainWindow):
        QMainWindow.keySharingMenu = QMainWindow.menuBar.addMenu("Key sharing")

        exportAction = QMainWindow.keySharingMenu.addAction("Export")
        exportAction.setStatusTip("exports a key")
        exportAction.setIcon(QIcon(appPath+"/icons/export.png"))
        exportAction.triggered.connect(QMainWindow.exportKey)

        importAction = QMainWindow.keySharingMenu.addAction("Import")
        importAction.setStatusTip("imports a key")
        importAction.setIcon(QIcon(appPath+"/icons/import.png"))
        importAction.triggered.connect(QMainWindow.importKey)
    @staticmethod
    def __password__(QMainWindow):
        QMainWindow.passwordMenu = QMainWindow.menuBar.addMenu("Password")

        passGenAction = QMainWindow.passwordMenu.addAction("Password generator")
        passGenAction.setStatusTip("generates a password based on different difficulty")
        passGenAction.setIcon(QIcon(appPath+"/icons/passGen.png"))
        passGenAction.triggered.connect(QMainWindow.passGen)

        passManagerAction = QMainWindow.passwordMenu.addAction("Password manager")
        passManagerAction.setDisabled(True)
        passManagerAction.setStatusTip("is being used to store and import or export passwords")
        passManagerAction.setIcon(QIcon(appPath+"/icons/import.png"))
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
        QMainWindow.table.setFont(QFont("sans-serif",12))
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
    def __setStyles__(QMainWindow):
        QMainWindow.table.setStyleSheet("""
        QTableWidget 
        {
            color: black;
            font-family: "Helvetica Neue", sans-serif; /* Changes the font */
            font-size: 12px;
            vertical-align: center;
            margin-top: 35px;
            border-collapse: collapse;
            border-radius: 0px 0px 6px 6px !important; /* Curves only the bottom corners */
            min-width: 400px;
            margin-left: 10px;
            margin-right: 10px;
            margin-bottom: 25px;
            alternate-background-color: #f2f2f2; /* Adds alternating row colors */
            background-color: #e6e6e6; /* Lighter gray */
        }

        QHeaderView::section 
        {
            background-color: #1a75ff; /* Blue */
            border-bottom: thin solid #0059b3; /* Darker blue */
            font-family: "Helvetica Neue", sans-serif; /* Changes the font */    
            border: none;
            height: 22px;
        }

        QTableWidget::item 
        {
            padding: 5px; /* Adds padding to table cells */
        }

        QTableWidget::item:selected 
        {
            background-color: #b3d9ff; /* Light blue */
        }

        /* Adds a subtle hover effect to table cells */
        QTableWidget::item:hover 
        {
            background-color: #f2f2f2;
        }

        /* Adds a hover effect to the table header */
        QHeaderView::section:hover 
        {
            background-color: #3399ff; /* Lighter blue */
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

#-------------------------------------------------------------------------------------------------------#"""
def run():
    import time
    start_time = time.time()
    easyGPGTool = app()
    easyGPGTool.show()
    end_time = time.time()
    compile_time = end_time - start_time
    print("Compile time:", compile_time)
    easyGPGTool.app.exec()
    del easyGPGTool.app