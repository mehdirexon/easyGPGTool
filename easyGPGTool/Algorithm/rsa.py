from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class easyRSA():
    @staticmethod
    def newPair(bits : int = 2048) -> tuple :
        key = RSA.generate(bits= bits)
        
        publicKey = key.publickey()
        privateKey = key
        
        return (publicKey,privateKey)
    
    @staticmethod
    def encrypt_rsa(publicKey : bytes , target):
        cipher = PKCS1_OAEP.new(publicKey)
        encrypted_message = cipher.encrypt(target)
        return encrypted_message
    
    @staticmethod
    def decrypt_rsa(privateKey : bytes, target):
        decipher = PKCS1_OAEP.new(privateKey)
        decrypted_message = decipher.decrypt(target)
        return decrypted_message
                        
        