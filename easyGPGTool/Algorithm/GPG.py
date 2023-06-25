import gnupg,os
from colorama import Fore
class GPG():
    def __init__(self):
        super().__init__()
        os.environ["GPG_AGENT_INFO"] = ""
        self.gpg = gnupg.GPG(gnupghome='/home/'+os.getlogin()+'/.gnupg')
        self.gpg.encoding = 'utf-8'
    def getKeys(self,secret : bool= False ):
        if secret:
            return self.gpg.list_keys(secret=True)
        else:
            return self.gpg.list_keys(secret=False)
    def generate_key(self,data):
        inputData = self.gpg.gen_key_input(
            name_email = data['email'],
            passphrase = data['passphrase'],
            key_type = data['key_type'],
            key_length = data['key_length'],
            name_real = data['fullname']
            )
        GPG.key = str(self.gpg.gen_key(inputData))
        if GPG.key == '':
            self.sendLog("the app couldn't create a key",Fore.RED)
            raise Exception("the app couldn't create a key")
        else:
            self.sendLog("a key created with this fingerprint : " + GPG.key ,Fore.GREEN)
    def removeKey(self,mainWindow,state):
        if state:
            result = self.gpg.delete_keys(mainWindow.removeKeyForm.fingerprintLineEdit.text(),passphrase= mainWindow.removeKeyForm.passphraseLineEdit.text(),secret=True)
            if result.status == 'ok':
                GPG.key = ''
                return result
            else:
                self.sendLog(result.stderr,Fore.RED)
                raise Exception(result.stderr)
        else:
            result = self.gpg.delete_keys(mainWindow.removeKeyForm.fingerprintLineEdit.text())
            if result.status == 'ok':
                GPG.key = ''
                return result
            else:
                self.sendLog(result.stderr,Fore.RED)
                raise Exception(result.stderr)
    def encrypt(self,email):
        from PySide6.QtWidgets import QFileDialog
        permission = False
        if self.gpg.list_keys(False) == [] and self.gpg.list_keys(True) == []:
            raise Exception("No such key")
        for this in self.gpg.list_keys(True):
            a = this['uids'][0].split('<')[1].replace('>','')
            if this['uids'][0].split('<')[1].replace('>','') == email:
                permission = True
                break
        if permission is not True:
            raise Exception("No such key")
        else:
            selectedFile = QFileDialog.getOpenFileName(self,"select your file","/home/" + os.getlogin() + "/Desktop")
            if not self.encryptForm.signCB.isChecked():
                with open(os.path.abspath(selectedFile[0]), 'rb') as file:
                    status = self.gpg.encrypt_file(file,recipients = email,output = os.path.splitext(selectedFile[0])[0] + '.safe')
            else:
                with open(os.path.abspath(selectedFile[0]), 'rb') as file:
                    status = self.gpg.encrypt_file(file,recipients = email,output = os.path.splitext(selectedFile[0])[0] + '.safe',sign=self.encryptForm.fingerprintLineEdit.text(),passphrase=self.encryptForm.passphraseLineEdit.text())
        return status
    def decrypt(self,passphrase):
        from PySide6.QtWidgets import QFileDialog,QMessageBox
        from easyGPGTool.GUI._extensions_ import Ext
        import magic

        fileExtension = 'log'
                  
        selectedFile = QFileDialog.getOpenFileName(self,"select your decrypted file","/home/" + os.getlogin() + "/Desktop",filter="*.safe")
        try:
            if selectedFile == '':
                raise Exception("path is empty")
            with open(str(selectedFile[0]), 'rb') as file:
                status = self.gpg.decrypt_file(file,passphrase = passphrase ,output= os.path.splitext(selectedFile[0])[0])
            
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
    def exportKey(self,status,armor):
        from PySide6.QtWidgets import QFileDialog
        if not status:
            pubKey = self.gpg.export_keys(self.exportForm.emailLineEdit.text(),armor=armor)
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
            privateKey = self.gpg.export_keys(self.exportForm.emailLineEdit.text(),True,passphrase=self.exportForm.passphraseLineEdit.text(),armor=armor)
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
    def importKey(self,status):
        if not status:
            result = self.gpg.import_keys_file(self.importForm.keyPathLineEdit.text())
            if result.returncode == 0:
                return (result.stderr,False)
            else:
                raise Exception(result.stderr)
        else:
            result = self.gpg.import_keys_file(self.importForm.keyPathLineEdit.text(),passphrase = self.importForm.passphraseLineEdit.text())
            if result.returncode == 0:
                return (result.stderr,True)
            else:
                raise Exception(result.stderr)
    def sendLog(self,txt_or_exception,status):
        from datetime import datetime
        print(f"{status}[LOG]",datetime.now(),txt_or_exception,f" {Fore.RESET}")
    def changeTrust(self,mode):
        result = self.gpg.trust_keys(self.trustForm.fingerprintCB.currentText(),mode)
        if result.status != 'ok':
            raise Exception(result.stderr)
        return result