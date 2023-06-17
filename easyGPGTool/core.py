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
from easyGPGTool.GUI._extensions_ import Ext
from easyGPGTool.GUI._passGen_ import passGenForm
from plyer import notification
from colorama import Fore
from glob import glob
import gnupg,os,magic,sys
#-------------------------------------------------------------------------------------------------------#
gpg = gnupg.GPG(gnupghome='/home/'+os.getlogin()+'/.gnupg')
gpg.encoding = 'utf-8'
appPath = os.path.normpath(__file__ + os.sep + os.pardir)
#-------------------------------------------------------------------------------------------------------#
class app(QMainWindow):
    __information__ = {"version" : "0.2beta","author" : "Mehdi Ghazanfari","author_email" : "mehdirexon@gmail.com"}
    now = datetime.now()
#-------------------------------------------------------------------------------------------------------#
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
#-------------------------------------------------------------------------------------------------------#
    def showEvent(self, event):
        super().showEvent(event)
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())
#-------------------------------------------------------------------------------------------------------#
    def sendLog(self,txt_or_exception,status):
        print(f"{status}[LOG]",self.now.strftime("%H:%M:%S :"),txt_or_exception,f" {Fore.RESET}")
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def keyGenSlot(self,data):
        try:
            self.sendLog("recive and generate signal has been recived",Fore.GREEN)
            GPG.generate_key(self,data)
            QMessageBox.information(self,"successful task","fingerprint : " + GPG.key,QMessageBox.Ok)
            menuItems.__Load__(self)
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"error",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.newKey()
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def keyDelSlot(self,state):
        try:
            self.sendLog("recive and delete signal has been recived",Fore.GREEN)
            result = GPG.removeKey(self,state)
            if result.status == 'ok':
                self.sendLog("a key was deleted",Fore.GREEN)
                QMessageBox.information(self,"successful task","key has been deleted successfully",QMessageBox.Ok)
                menuItems.__Load__(self)
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"error",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.removeKey()
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def encryptionSlot(self,status):
        if status is True:
            try:
                self.sendLog("encryption signal has been recived",Fore.GREEN)
                status = GPG.encrypt(self,self.encryptForm.emailLineEdit.text())
                if status.ok is True:
                    QMessageBox.information(self,"encrypting a file",str(status.stderr) + "\n"+ str(status.status),QMessageBox.Ok)
                    self.sendLog("an encryption task has been successfully done",Fore.GREEN)
                else:
                    raise Exception(status.stderr)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"encrypting a file",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.encrypt()
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def decryptionSlot(self,status):
        if status is True:
            try:
                status = GPG.decrypt(self,passphrase=self.decryptForm.passphraseLineEdit.text())
                if status.ok is True:
                    QMessageBox.information(self,"decrypting a file",str(status.stderr) + "\n"+ str(status.status) +"\n"+ str(status.valid) +"\n"+ str(status.trust_text),QMessageBox.Ok)
                    self.sendLog("a decryption task has been successfully done",Fore.GREEN)
                else:
                    raise Exception(status.stderr)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"decrypting a file",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.decrypt()
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def exportSlot(self,status,armor):
        try:
            result = GPG.export(self,status,armor)
            if not result[1]:
                QMessageBox.information(self,"exporting a key","public key has been created at\n" + result[0] + "\nsuccessfully",QMessageBox.Ok)

            elif result[1]:
                QMessageBox.information(self,"exporting a key","private key has been created at\n" + result[0]+ "\nsuccessfully",QMessageBox.Ok)
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"exporting a key",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.exportKey() 
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def importSlot(self,status):
        try:
            status = GPG.importKey(self,status)
            if status[1] == False:
                QMessageBox.information(self,"importing a public key",status[0] + '\n',QMessageBox.Ok)
                menuItems.__Load__(self)
            elif status[1] == True:
                QMessageBox.information(self,"importing a private key",status[0] + '\n',QMessageBox.Ok)
                menuItems.__Load__(self)
            self.sendLog("an import task has been successfully done",Fore.GREEN)
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"importing a key",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.importKey()
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def privateCheckBoxSlot(self):
        menuItems.__Load__(self)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def trustLevelSlot(self,mode):
        try:
            result = GPG.changeTrust(self,mode)
            QMessageBox.information(self,"changing a key trust value",result.status + '\n' + result.stderr,QMessageBox.Ok)
            menuItems.__Load__(self)
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"changing a key trust value",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.trust()
#-------------------------------------------------------------------------------------------------------#
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
                self.sendLog("delete key form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting remove key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.removeKey()
        else:
            try:
                self.removeKeyForm.close()
                self.removeKeyForm = removeKeyForm()
                self.removeKeyForm.show()
                self.removeKeyForm.signal.connect(self.keyDelSlot)
                self.sendLog("previous delete key form destroyed and again been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting remove key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.removeKey()
#-------------------------------------------------------------------------------------------------------#
    def newKey(self):
        if self.newKeyForm is None:
            try:
                self.newKeyForm = newKeyForm()
                self.newKeyForm.show()
                self.newKeyForm.signal.connect(self.keyGenSlot)
                self.sendLog("new key widget has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting new key form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
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
#-------------------------------------------------------------------------------------------------------#
    def aboutUs(self):
        if self.aboutUsForm is None:
            try:
                self.aboutUsForm = aboutUsForm()
                self.aboutUsForm.show()
                self.aboutUsForm.getInformation(self.__information__)
                self.sendLog("about us form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting about us form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.aboutUs()
        else:
            try:
                self.aboutUsForm.close()
                self.aboutUsForm = aboutUsForm()
                self.aboutUsForm.show()
                self.aboutUsForm.getInformation(self.__information__)
                self.sendLog("previous about us form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting about us form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.aboutUs()
#-------------------------------------------------------------------------------------------------------#
    def patchNote(self):
        if self.patchNoteForm is None:
            try:
                self.patchNoteForm = patchNoteForm()
                self.patchNoteForm.show()
                self.sendLog("patch note form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting patch note form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.patchNote()
        else:
            try:
                self.patchNoteForm.close()
                self.patchNoteForm = patchNoteForm()
                self.patchNoteForm.show()
                self.sendLog("previous patch note form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting patch note form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.patchNote()
#-------------------------------------------------------------------------------------------------------#
    def encrypt(self):
        if self.encryptForm is None:
            try:
                self.encryptForm = encryptForm()
                self.encryptForm.show()
                self.encryptForm.signal.connect(self.encryptionSlot)
                self.sendLog("encrypt form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting encrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.encrypt()
        else:
            try:
                self.encryptForm.close()
                self.encryptForm = encryptForm()
                self.encryptForm.show()
                self.encryptForm.signal.connect(self.encryptionSlot)
                self.sendLog("previous encrypt form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting encrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.encrypt()
#-------------------------------------------------------------------------------------------------------#
    def decrypt(self):
        if self.decryptForm is None:
            try:
                self.decryptForm = decryptForm()
                self.decryptForm.signal.connect(self.decryptionSlot)
                self.decryptForm.show()
                self.sendLog("decrypt form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting decrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.decrypt()
        else:
            try:
                self.decryptForm.close()
                self.decryptForm = decryptForm()
                self.decryptForm.show()
                self.decryptForm.signal.connect(self.decryptionSlot)
                self.sendLog("previous decrypt form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting decrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.decrypt()
#-------------------------------------------------------------------------------------------------------#
    def exportKey(self):
        if self.exportForm is None:
            try:
                self.exportForm = exportForm()
                self.exportForm.show()
                self.exportForm.signal.connect(self.exportSlot)
                self.sendLog("export form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting export form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.exportKey()
        else:
            try:
                self.exportForm.close()
                self.exportForm = exportForm()
                self.exportForm.show()
                self.exportForm.signal.connect(self.exportSlot)
                self.sendLog("previous export form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting export form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.exportKey()
#-------------------------------------------------------------------------------------------------------#
    def importKey(self):
        if self.importForm is None:
            try:
                self.importForm = importForm()
                self.importForm.show()
                self.importForm.signal.connect(self.importSlot)
                self.sendLog("import form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.importKey()
        else:
            try:
                self.importForm.close()
                self.importForm = importForm()
                self.importForm.show()
                self.importForm.signal.connect(self.importSlot)
                self.sendLog("previous import form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.importKey()
#-------------------------------------------------------------------------------------------------------#
    def trust(self):
        if self.trustForm is None:
            try:
                self.trustForm = trustForm()
                self.trustForm.show()
                self.trustForm.getFingerprints(gpg.list_keys())
                self.trustForm.signal.connect(self.trustLevelSlot)
                self.sendLog("trust form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.trust()
        else:
            try:
                self.trustForm.close()
                self.trustForm = trustForm()
                self.trustForm.show()
                self.trustForm.getFingerprints(gpg.list_keys())
                self.trustForm.signal.connect(self.trustLevelSlot)
                self.sendLog("previous trust form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting trust form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.trust()
#-------------------------------------------------------------------------------------------------------#
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
#-------------------------------------------------------------------------------------------------------#

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
        QMainWindow.table.setRowCount(len(gpg.list_keys()))

        QMainWindow.table.verticalHeader().setVisible(False)
        QMainWindow.table.setFont(QFont("sans-serif",12))
        QMainWindow.table.setHorizontalHeaderLabels(["Type","Name","Email","Fingerprint","Trust"])

        QMainWindow.table.horizontalHeader().setSectionResizeMode(4,QHeaderView.Fixed) 
        QMainWindow.table.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch) 
        QMainWindow.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        QMainWindow.table.horizontalHeader().setSectionResizeMode(1,QHeaderView.Fixed)
        QMainWindow.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.Fixed)

        for row,key in enumerate(gpg.list_keys()):
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
            QMainWindow.table.setRowCount(len(gpg.list_keys()))

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
            for row,key in enumerate(gpg.list_keys()):
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

                QMainWindow.table.setRowCount(len(gpg.list_keys()))

                QMainWindow.table.setItem(row,0,type)
                QMainWindow.table.setItem(row,1,ID)
                QMainWindow.table.setItem(row,2,email)
                QMainWindow.table.setItem(row,3,fp)
                QMainWindow.table.setItem(row,4,trustLvl)
        else:
            for row,key in enumerate(gpg.list_keys(True)):
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

                QMainWindow.table.setRowCount(len(gpg.list_keys(True)))

                QMainWindow.table.setItem(row,0,type)
                QMainWindow.table.setItem(row,1,ID)
                QMainWindow.table.setItem(row,2,email)
                QMainWindow.table.setItem(row,3,fp)
                QMainWindow.table.setItem(row,4,trustLvl)
class GPG(app):
#-------------------------------------------------------------------------------------------------------#
    @staticmethod
    def generate_key(self,data):
        inputData = gpg.gen_key_input(
            name_email = data['email'],
            passphrase = data['passphrase'],
            key_type = data['key_type'],
            key_length = data['key_length'],
            name_real = data['fullname']
            )
        GPG.key = str(gpg.gen_key(inputData))
        if GPG.key == '':
            self.sendLog("the app couldn't create a key",Fore.RED)
            raise Exception("the app couldn't create a key")
        else:
            self.sendLog("a key created with this fingerprint : " + GPG.key ,Fore.GREEN)
#-------------------------------------------------------------------------------------------------------#
    @staticmethod
    def removeKey(self,state):
        if state:
            result = gpg.delete_keys(self.removeKeyForm.fingerprintLineEdit.text(),passphrase= self.removeKeyForm.passphraseLineEdit.text(),secret=True)
            if result.status == 'ok':
                GPG.key = ''
                return result
            else:
                self.sendLog(result.stderr,Fore.RED)
                raise Exception(result.stderr)
        else:
            result = gpg.delete_keys(self.removeKeyForm.fingerprintLineEdit.text())
            if result.status == 'ok':
                GPG.key = ''
                return result
            else:
                self.sendLog(result.stderr,Fore.RED)
                raise Exception(result.stderr)
#-------------------------------------------------------------------------------------------------------#
    @staticmethod
    def encrypt(self,email):
        permission = False
        if gpg.list_keys(False) == [] and gpg.list_keys(True) == []:
            raise Exception("No such key")
        #-----------------------------------------------------------
        for this in gpg.list_keys(True):
            a = this['uids'][0].split('<')[1].replace('>','')
            if this['uids'][0].split('<')[1].replace('>','') == email:
                permission = True
                break
        #-----------------------------------------------------------      
        if permission is not True:
            raise Exception("No such key")
        #-----------------------------------------------------------      
        else:
            selectedFile = QFileDialog.getOpenFileName(self,"select your file","/home/" + os.getlogin() + "/Desktop")
            if not self.encryptForm.signCB.isChecked():
                with open(os.path.abspath(selectedFile[0]), 'rb') as file:
                    status = gpg.encrypt_file(file,recipients = email,output = os.path.splitext(selectedFile[0])[0] + '.safe')
            else:
                with open(os.path.abspath(selectedFile[0]), 'rb') as file:
                    status = gpg.encrypt_file(file,recipients = email,output = os.path.splitext(selectedFile[0])[0] + '.safe',sign=self.encryptForm.fingerprintLineEdit.text(),passphrase=self.encryptForm.passphraseLineEdit.text())
        return status
#-------------------------------------------------------------------------------------------------------#
    @staticmethod
    def decrypt(self,passphrase):
        fileExtension = 'log'
                  
        selectedFile = QFileDialog.getOpenFileName(self,"select your decrypted file","/home/" + os.getlogin() + "/Desktop",filter="*.safe")
        try:
            if selectedFile == '':
                raise Exception("path is empty")
            with open(str(selectedFile[0]), 'rb') as file:
                status = gpg.decrypt_file(file,passphrase = passphrase ,output= os.path.splitext(selectedFile[0])[0])
            
            with open(os.path.splitext(selectedFile[0])[0], 'rb') as file:
                tmpExtFile = magic.from_file(os.path.splitext(selectedFile[0])[0], mime = True)
                
            for ext in Ext.data.keys():
                if Ext.data[ext]['mime'] == tmpExtFile:
                    fileExtension = ext
                    break

            os.rename(os.path.splitext(selectedFile[0])[0],os.path.splitext(selectedFile[0])[0] + '.'+ fileExtension)

            return status
        except Exception as ex:
            QMessageBox.critical(self,"decrypting a file",str(ex),QMessageBox.Ok)
#-------------------------------------------------------------------------------------------------------#
    @staticmethod
    def exportKey(self,status,armor):
        if not status:
            pubKey = gpg.export_keys(self.exportForm.emailLineEdit.text(),armor=armor)
            if pubKey == '':
                raise Exception('no such key(invalid ID)')
            
            selectedPath = QFileDialog.getExistingDirectory(self,"select your file","/home/" + os.getlogin() + "/Desktop")

            if selectedPath == '':
                raise Exception("empty path can not be used")
            
            if armor:
                with open(selectedPath + '/pubKey.asc',"w") as file:
                    file.write(pubKey)
            else:
                with open(selectedPath + '/pubKey',"wb") as file:
                    file.write(pubKey)

            return (selectedPath,False)
        else:
            privateKey = gpg.export_keys(self.exportForm.emailLineEdit.text(),True,passphrase=self.exportForm.passphraseLineEdit.text(),armor=armor)
            if privateKey == '':
                raise Exception("id is not valid")
            
            selectedPath = QFileDialog.getExistingDirectory(self,"select your file","/home/" + os.getlogin() + "/Desktop")

            if selectedPath == '':
                raise Exception("empty path can not be used")
            
            if armor:
                with open(selectedPath + '/privateKey.asc',"w") as file:
                    file.write(privateKey)
            else:
                with open(selectedPath + '/privateKey',"wb") as file:
                    file.write(privateKey)

            return(selectedPath,True)
#-------------------------------------------------------------------------------------------------------#
    @staticmethod
    def importKey(self,status):
        if not status:
            result = gpg.import_keys_file(self.importForm.keyPathLineEdit.text())
            if result.returncode == 0:
                return (result.stderr,False)
            else:
                raise Exception(result.stderr)
        else:
            result = gpg.import_keys_file(self.importForm.keyPathLineEdit.text(),passphrase = self.importForm.passphraseLineEdit.text())
            if result.returncode == 0:
                return (result.stderr,True)
            else:
                raise Exception(result.stderr)
#-------------------------------------------------------------------------------------------------------#
    @staticmethod
    def changeTrust(self,mode):
        result = gpg.trust_keys(self.trustForm.fingerprintCB.currentText(),mode)
        if result.status != 'ok':
            raise Exception(result.stderr)
        return result
#-------------------------------------------------------------------------------------------------------#
def run():
    easyGPGTool = app()
    easyGPGTool.show()
    easyGPGTool.app.exec()
    del easyGPGTool.app