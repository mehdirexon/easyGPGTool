from PySide6.QtWidgets import QMainWindow,QStatusBar,QMessageBox,QFileDialog,QTableWidget,QAbstractItemView,QTableWidgetItem,QWidget,QCheckBox,QHeaderView,QVBoxLayout
from PySide6.QtCore import Slot,Qt
from PySide6.QtGui import QIcon,QKeySequence,QFont,QClipboard
from datetime import datetime
from ext.new_key import newKeyForm
from ext.patch_note import patchNoteForm
from ext.remove_key import removeKeyForm
from ext.about_us import aboutUsForm
from ext.encrypt import encryptForm
from ext.decrypt import decryptForm
from ext.export import exportForm
from ext._import import importForm
from ext.trust import trustForm
from ext.extensions import Ext
from plyer import notification
from colorama import Fore
from glob import glob
import gnupg,os,magic
#-------------------------------------------------------------------------------------------------------#
gpg = gnupg.GPG(gnupghome='/home/'+os.getlogin()+'/.gnupg')
gpg.encoding = 'utf-8'
#-------------------------------------------------------------------------------------------------------#
class mainWindow(QMainWindow):
    __information__ = {"version" : "beta","author" : "Mehdi Ghazanfari","author_email" : "mehdirexon@gmail.com"}
    now = datetime.now()
#-------------------------------------------------------------------------------------------------------#
    def __init__(self,app,title):
        #basics
        super().__init__()
        self.app = app
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
        #basic configs
        self.setWindowTitle(title)
        self.setMinimumHeight(600)
        self.setMinimumWidth(1000)
        self.setWindowIcon(QIcon("ext/pictures/gpgIcon.ico"))

        #menu_table
        menuItems.__showMenuItems__(self)
        #menubar
        topBarMenu.__showTopBarItems__(self)
        #status bar
        self.setStatusBar(QStatusBar(self))
#-------------------------------------------------------------------------------------------------------#
    def quit(self):
        try:
            self.app.quit()
            self.sendLog("the application was closed by quit action",Fore.GREEN)
        except Exception as ex:
            self.sendLog(ex,Fore.RED)
#-------------------------------------------------------------------------------------------------------#
    def sendLog(self,txt_or_exception,status):
        print(f"{status}[LOG]",self.now.strftime("%H:%M:%S :"),txt_or_exception,f" {Fore.RESET}")
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def reciveAndGenerate(self,data):
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
    def reciveAndDelete(self,state):
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
    def encryptionSignal(self,status):
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
    def decryptionSignal(self,status):
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
#----------------------------------------------------d---------------------------------------------------#
    @Slot()
    def exportSignal(self,status,armor):
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
                self.export() 
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def importSignal(self,status):
        try:
            status = GPG.import_(self,status)
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
                self.import_()
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def privateCBChanged(self):
        menuItems.__Load__(self)
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def trustLVLChanged(self,mode):
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
        data = self.table.item(row,column)
        clipboard = QClipboard()
        clipboard.setText(str(data.text()))
        notification.notify(
            title = 'GPG tool notification',
            message = data.text()+'\nhas been copied in clipboard',
        )
#-------------------------------------------------------------------------------------------------------#
    def removeKey(self):
        if self.removeKeyForm is None:
            try:
                self.removeKeyForm = removeKeyForm()
                self.removeKeyForm.show()
                self.removeKeyForm.signal.connect(self.reciveAndDelete)
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
                self.removeKeyForm.signal.connect(self.reciveAndDelete)
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
                self.newKeyForm.signal.connect(self.reciveAndGenerate)
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
                self.newKeyForm.signal.connect(self.reciveAndGenerate)
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
                self.encryptForm.signal.connect(self.encryptionSignal)
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
                self.encryptForm.signal.connect(self.encryptionSignal)
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
                self.decryptForm.show()
                self.decryptForm.signal.connect(self.decryptionSignal)
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
                self.decryptForm.signal.connect(self.decryptionSignal)
                self.sendLog("previous decrypt form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting decrypt form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.decrypt()
#-------------------------------------------------------------------------------------------------------#
    def export(self):
        if self.exportForm is None:
            try:
                self.exportForm = exportForm()
                self.exportForm.show()
                self.exportForm.signal.connect(self.exportSignal)
                self.sendLog("export form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting export form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.export()
        else:
            try:
                self.exportForm.close()
                self.exportForm = exportForm()
                self.exportForm.show()
                self.exportForm.signal.connect(self.exportSignal)
                self.sendLog("previous export form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting export form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.export()
#-------------------------------------------------------------------------------------------------------#
    def import_(self):
        if self.importForm is None:
            try:
                self.importForm = importForm()
                self.importForm.show()
                self.importForm.signal.connect(self.importSignal)
                self.sendLog("import form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.import_()
        else:
            try:
                self.importForm.close()
                self.importForm = importForm()
                self.importForm.show()
                self.importForm.signal.connect(self.importSignal)
                self.sendLog("previous import form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.import_()
#-------------------------------------------------------------------------------------------------------#
    def trust(self):
        if self.trustForm is None:
            try:
                self.trustForm = trustForm()
                self.trustForm.show()
                self.trustForm.getFingerprints(gpg.list_keys())
                self.trustForm.signal.connect(self.trustLVLChanged)
                self.sendLog("trust form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting import form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.import_()
        else:
            try:
                self.trustForm.close()
                self.trustForm = trustForm()
                self.trustForm.show()
                self.trustForm.getFingerprints(gpg.list_keys())
                self.trustForm.signal.connect(self.trustLVLChanged)
                self.sendLog("previous trust form destoryed and again called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting trust form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.import_()
#-------------------------------------------------------------------------------------------------------#
#classes
class topBarMenu():
    @staticmethod
    def __showTopBarItems__(QMainWindow):
        QMainWindow.menuBar = QMainWindow.menuBar()
        topBarMenu.__keyMenu__(QMainWindow)
        topBarMenu.__dataProtectionMenu__(QMainWindow)
        topBarMenu.__keySharing__(QMainWindow)
        topBarMenu.__helpMenu__(QMainWindow)
    @staticmethod
    def __keyMenu__(QMainWindow):
        QMainWindow.keyMenu = QMainWindow.menuBar.addMenu("Key")
        #1
        newKey = QMainWindow.keyMenu.addAction("New key")
        newKey.setShortcut(QKeySequence(QKeySequence.New))
        newKey.triggered.connect(QMainWindow.newKey)
        newKey.setIcon(QIcon("ext/pictures/newIcon.png"))
        newKey.setStatusTip("creates a new key")
        #2
        trustKey = QMainWindow.keyMenu.addAction("Trust key")
        trustKey.triggered.connect(QMainWindow.trust)
        trustKey.setIcon(QIcon("ext/pictures/trust.png"))
        trustKey.setStatusTip("changes trust lvl of a key")
        #3
        removeKey = QMainWindow.keyMenu.addAction("Remove key")
        removeKey.triggered.connect(QMainWindow.removeKey)
        removeKey.setShortcut(QKeySequence(QKeySequence.Delete))
        removeKey.setIcon(QIcon("ext/pictures/removeIcon.png"))
        removeKey.setStatusTip("removes a key")
    @staticmethod
    def __dataProtectionMenu__(QMainWindow):
        QMainWindow.dataProtection = QMainWindow.menuBar.addMenu("Data protection")
        encrypt = QMainWindow.dataProtection.addAction('Encrypt')
        encrypt.triggered.connect(QMainWindow.encrypt)
        encrypt.setStatusTip("encrypts a file")
        encrypt.setIcon(QIcon("ext/pictures/encrypt.png"))
        encrypt.setShortcut(QKeySequence('Shift+E'))
        #5
        decrypt = QMainWindow.dataProtection.addAction('Decrypt')
        decrypt.triggered.connect(QMainWindow.decrypt)
        decrypt.setStatusTip('decrypts a file')
        decrypt.setIcon(QIcon('ext/pictures/decrypt.png'))
        decrypt.setShortcut(QKeySequence('Shift+D'))
    @staticmethod
    def __helpMenu__(QMainWindow):
        QMainWindow.helpMenu = QMainWindow.menuBar.addMenu("Help")
            #actions
        #1
        patchNote = QMainWindow.helpMenu.addAction("What's new")
        patchNote.setStatusTip("show lastest changes in the app")
        patchNote.triggered.connect(QMainWindow.patchNote)
        patchNote.setIcon(QIcon('ext/pictures/patchNote.png'))
        #2
        aboutUs = QMainWindow.helpMenu.addAction("About us")
        aboutUs.setStatusTip("shows app and author information")
        aboutUs.setIcon(QIcon('ext/pictures/aboutUs.png'))
        aboutUs.setShortcut(QKeySequence(QKeySequence.HelpContents))
        aboutUs.triggered.connect(QMainWindow.aboutUs)
    @staticmethod
    def __keySharing__(QMainWindow):
        QMainWindow.keySharingMenu = QMainWindow.menuBar.addMenu("Key sharing")

        exportAction = QMainWindow.keySharingMenu.addAction("Export")
        exportAction.setStatusTip("exports a key")
        exportAction.setIcon(QIcon("ext/pictures/export.png"))
        exportAction.triggered.connect(QMainWindow.export)

        #7
        importAction = QMainWindow.keySharingMenu.addAction("Import")
        importAction.setStatusTip("imports a key")
        importAction.setIcon(QIcon("ext/pictures/import.png"))
        importAction.triggered.connect(QMainWindow.import_)
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
        QMainWindow.privateCB.stateChanged.connect(QMainWindow.privateCBChanged)

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
        QMainWindow.table.setFont(QFont("sans-serif",8))
        QMainWindow.table.setHorizontalHeaderLabels(["Type","Name","Email","Fingerprint","trust"])

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
            color : black;
            font-family :sans-serif;
            font-size : 12px; 
            vertical-align: center;
        }
        QTableWidget
        {
            margin-top: 35px;
            border-collapse: collapse;
            border-radius:6px 6px 6px 6px;
            min-width: 400px;
            margin-left : 10px;
            margin-right : 10px;
            margin-bottom : 25px;
            alternate-background-color: #f2f2f2;
            background-color : #c5c7c9;
        }
        QHeaderView::section {
            background-color: #04AA6D;
            border-bottom: thin solid #009879;
            font-family : sans-serif;    
            border: none;
            height: 22px;
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
class GPG(mainWindow):
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
            result = gpg.delete_keys(self.removeKeyForm.fingerprintLineEdit.text(),self.removeKeyForm.passphraseLineEdit.text())
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
    def export(self,status,armor):
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
    def import_(self,status):
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
    @staticmethod
    def changeTrust(self,mode):
        result = gpg.trust_keys(self.trustForm.fingerprintCB.currentText(),mode)
        if result.status != 'ok':
            raise Exception(result.stderr)
        return result