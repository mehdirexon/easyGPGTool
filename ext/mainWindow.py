from PySide6.QtWidgets import QMainWindow,QStatusBar,QMessageBox,QFileDialog
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon,QKeySequence
from datetime import datetime
from ext.new_key import newKeyForm
from ext.show_all import showAllForm
from ext.patch_note import patchNoteForm
from ext.remove_key import removeKeyForm
from ext.about_us import aboutUsForm
from ext.encrypt import encryptForm
from ext.decrypt import decryptForm
from ext.export import exportForm
from ext._import import importForm
from ext.extensions import Ext
from colorama import Fore
from glob import glob
import gnupg,os,magic
#-------------------------------------------------------------------------------------------------------#
gpg = gnupg.GPG(gnupghome='/home/'+os.getlogin()+'/.gnupg')
gpg.encoding = 'utf-8'
#-------------------------------------------------------------------------------------------------------#
class mainWindow(QMainWindow):
    __information__ = {"version" : "beta","author" : "Mehdi Ghazanfari","author_email" : "coming soon"}
    now = datetime.now()
#-------------------------------------------------------------------------------------------------------#
    def __init__(self,app,title):
        #basics
        super().__init__()
        self.app = app
        #forms
        self.newKeyForm = None
        self.removeKeyForm = None
        self.showAllForm = None
        self.aboutUsForm = None
        self.patchNoteForm = None
        self.encryptForm = None
        self.decryptForm = None
        self.exportForm = None
        self.importForm = None
        #basic configs
        self.setWindowTitle(title)
        self.setMinimumHeight(400)
        self.setMinimumWidth(700)
        self.setWindowIcon(QIcon("ext/pictures/gpgIcon.ico"))

        #menubar
        menuBar = self.menuBar()

        #action bar and its actions
        actionMenu = menuBar.addMenu("Action")

        ###actions
        #1
        newKey = actionMenu.addAction("New key")
        newKey.setShortcut(QKeySequence(QKeySequence.New))
        newKey.triggered.connect(self.newKey)
        newKey.setIcon(QIcon("ext/pictures/newIcon.png"))
        newKey.setStatusTip("creates a new key")
        #2
        removeKey = actionMenu.addAction("Remove key")
        removeKey.triggered.connect(self.removeKey)
        removeKey.setShortcut(QKeySequence(QKeySequence.Delete))
        removeKey.setIcon(QIcon("ext/pictures/removeIcon.png"))
        removeKey.setStatusTip("removes a key")

        actionMenu.addSeparator()
        #3
        showAll = actionMenu.addAction('Show all the keys')
        showAll.triggered.connect(self.showAll)
        showAll.setShortcut(QKeySequence(QKeySequence.Paste))
        showAll.setIcon(QIcon("ext/pictures/showAll.png"))
        showAll.setStatusTip("shows all the keys has been crated so far")

        actionMenu.addSeparator()

        #4
        encrypt = actionMenu.addAction('Encrypt')
        encrypt.triggered.connect(self.encrypt)
        encrypt.setStatusTip("encrypts a file")
        encrypt.setIcon(QIcon("ext/pictures/encrypt.png"))
        encrypt.setShortcut(QKeySequence('Shift+E'))
        #5
        decrypt = actionMenu.addAction('Decrypt')
        decrypt.triggered.connect(self.decrypt)
        decrypt.setStatusTip('decrypts a file')
        decrypt.setIcon(QIcon('ext/pictures/decrypt.png'))
        decrypt.setShortcut(QKeySequence('Shift+D'))

        actionMenu.addSeparator()
        #6
        exportAction = actionMenu.addAction("Export")
        exportAction.setStatusTip("exports a key")
        exportAction.setIcon(QIcon("ext/pictures/export.png"))
        exportAction.triggered.connect(self.export)

        #7
        importAction = actionMenu.addAction("Import")
        importAction.setStatusTip("imports a key")
        importAction.setIcon(QIcon("ext/pictures/import.png"))
        importAction.triggered.connect(self.import_)

        actionMenu.addSeparator()
        #8
        quitAction = actionMenu.addAction("Quit")
        quitAction.setStatusTip("application will be closed")
        quitAction.setIcon(QIcon("ext/pictures/quit.png"))
        quitAction.setShortcut(QKeySequence(QKeySequence.Quit))
        quitAction.triggered.connect(self.quit)

        #help bar and its actions
        helpMenu = menuBar.addMenu("Help")
            #actions
        #1
        patchNote = helpMenu.addAction("Patch note")
        patchNote.setStatusTip("show lastest changes in the app")
        patchNote.triggered.connect(self.patchNote)
        patchNote.setIcon(QIcon('ext/pictures/patchNote.png'))
        #2
        aboutUs = helpMenu.addAction("About us")
        aboutUs.setStatusTip("shows app and author information")
        aboutUs.setIcon(QIcon('ext/pictures/aboutUs.png'))
        aboutUs.setShortcut(QKeySequence(QKeySequence.HelpContents))
        aboutUs.triggered.connect(self.aboutUs)

        #status bar
        self.setStatusBar(QStatusBar(self))

        self.sendLog("the app runned successfully",Fore.GREEN)
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
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"error",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.newKey()
#-------------------------------------------------------------------------------------------------------#
    @Slot()
    def reciveAndDelete(self,data):
        try:
            self.sendLog("recive and delete signal has been recived",Fore.GREEN)
            result = GPG.removeKey(self,data)
            if result[0] == 0:
                self.sendLog("a key was deleted",Fore.GREEN)
                QMessageBox.information(self,"successful task","key was deleted successfully",QMessageBox.Ok)
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
                    QMessageBox.information(self,"decrypting a file",str(status.stderr) + "\n"+ str(status.status),QMessageBox.Ok)
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
                
            elif status[1] == True:
                QMessageBox.information(self,"importing a private key",status[0] + '\n',QMessageBox.Ok)
        except Exception as ex:
            self.sendLog(str(ex),Fore.RED)
            result = QMessageBox.critical(self,"importing a key",str(ex),QMessageBox.Retry|QMessageBox.Abort)
            if result == QMessageBox.Retry:
                self.import_() 
#-------------------------------------------------------------------------------------------------------#
    def showAll(self):
        if self.showAllForm is None:
            try:
                self.showAllForm = showAllForm()
                self.showAllForm.show()
                GPG.showAll(self.showAllForm.textBox)
                self.sendLog("show all form has been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting show all form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.showAll()
        else:
            try:
                self.showAllForm.close()
                self.showAllForm = showAllForm()
                self.showAllForm.show()
                GPG.showAll(self.showAllForm.textBox)
                self.sendLog("previous show all form destroyed and again been called",Fore.GREEN)
            except Exception as ex:
                self.sendLog(str(ex),Fore.RED)
                result = QMessageBox.critical(self,"starting show all form",str(ex),QMessageBox.Retry|QMessageBox.Abort)
                if result == QMessageBox.Retry:
                    self.showAll()
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
    def removeKey(self,data):
        result = gpg.delete_keys(fingerprints=data['fingerprint'],passphrase=data['passphrase'],secret=True)
        if result.status == 'ok':
            result = gpg.delete_keys(fingerprints=data['fingerprint'],passphrase=data['passphrase'])
            if result.status == 'ok':
                GPG.key = ''
                return [0,result]
            else:
                self.sendLog(result.stderr,Fore.RED)
                raise Exception(result.stderr)
        else:
            self.sendLog(result.stderr,Fore.RED)
            raise Exception(result.stderr)
#-------------------------------------------------------------------------------------------------------#
    @staticmethod
    def showAll(self):
        if gpg.list_keys(False) != []:
            self.append("public keys :\n")
            for this in gpg.list_keys(False):
                self.append(str(this) + '\n')
            self.append('\nprivate keys :\n')
            for this in gpg.list_keys(True):
                self.append(str(this) + '\n')
        else:
            self.append("empty\n")
#-------------------------------------------------------------------------------------------------------#
    @staticmethod
    def encrypt(self,email):
        permission = False

        if gpg.list_keys(False) == [] and gpg.list_keys(True) == []:
            raise Exception("No such key")
        #-----------------------------------------------------------
        for this in gpg.list_keys(True):
            if this['uids'][0].replace('<','').replace('>','').split()[1] == email:
                permission = True
        #-----------------------------------------------------------      
        if permission is not True:
            raise Exception("No such key")
        #-----------------------------------------------------------      
        else:
            selectedFile = QFileDialog.getOpenFileName(self,"select your file","/home/" + os.getlogin() + "/Desktop")
            with open(os.path.abspath(selectedFile[0]), 'rb') as file:
                status = gpg.encrypt_file(file,recipients = email,output = os.path.splitext(selectedFile[0])[0] + '.safe')
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
#-------------------------------------------------------------------------------------------------------#