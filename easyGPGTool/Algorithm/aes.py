from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from typing import Union


class easyAES:
    @staticmethod
    def encrypt(plainText: Union[str, bytes], key) -> Union[str, bytes]:
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plainText = plainText + b" " * (16 - len(plainText) % 16)
        ciphertext = cipher.encrypt(plainText)

        return iv + ciphertext

    @staticmethod
    def decrypt(ciphertext, key):
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv)

        plaintext = cipher.decrypt(ciphertext)

        plaintext = plaintext.rstrip(b" ")

        return plaintext
