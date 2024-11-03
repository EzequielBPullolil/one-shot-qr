'''
UrlEncryptor module container
'''
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class UrlEncryptor:
    '''
        UrlEncryptor provides an abstraction to encrypt and decrypt url
        using an symmetric encryption with an secret key passed when class is instancied 
    '''
    def __init__(self, secret):
        if len(secret) not in {16, 24, 32}:
            raise ValueError(
                f"The length of the secret key must be 16, 24 or 32 bytes but must have a length of: {len(secret)}"
                )
        self.__secret = secret.encode('utf-8')

    def encrypt(self, url: str) -> str:
        '''
            Describes an encrypted URL using a symmetric encryption method
        '''
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.__secret), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        pad_length = 16 - len(url) % 16
        padded_url = url + chr(pad_length) * pad_length
        encrypted = encryptor.update(padded_url.encode()) + encryptor.finalize()
        return base64.b64encode(iv + encrypted).decode()

    def decrypt(self, url_encriptada):
        '''
            Describes an encrypted URL using a symmetric encryption method
        '''
        data = base64.b64decode(url_encriptada.encode())
        iv = data[:16]
        encrypted_url = data[16:]
        cipher = Cipher(algorithms.AES(self.__secret), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_url) + decryptor.finalize()
        pad_length = decrypted_padded[-1]
        return decrypted_padded[:-pad_length].decode()
