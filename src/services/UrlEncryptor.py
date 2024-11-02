from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

class UrlEncryptor:
    def __init__(self, secret):
        if len(secret) not in {16, 24, 32}:
            print(len(secret))
            raise ValueError("La longitud de la clave debe ser 16, 24 o 32 bytes.")
        self.__secret = secret.encode('utf-8')

    def encrypt(self, url: str):
        """Encripta una URL utilizando AES."""
        iv = os.urandom(16)  # Genera un IV aleatorio para esta operación
        cipher = Cipher(algorithms.AES(self.__secret), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Asegúrate de que la URL tenga un tamaño múltiplo de 16 bytes
        pad_length = 16 - len(url) % 16
        padded_url = url + chr(pad_length) * pad_length
        
        # Encriptar
        encrypted = encryptor.update(padded_url.encode()) + encryptor.finalize()
        
        # Combina el IV y el texto cifrado para la desencriptación
        return base64.b64encode(iv + encrypted).decode()

    def decrypt(self, url_encriptada):
        """Desencripta una URL encriptada utilizando AES."""
        data = base64.b64decode(url_encriptada.encode())
        iv = data[:16]  # Extrae el IV de los primeros 16 bytes
        encrypted_url = data[16:]  # El resto es el texto cifrado
        
        cipher = Cipher(algorithms.AES(self.__secret), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Desencriptar
        decrypted_padded = decryptor.update(encrypted_url) + decryptor.finalize()
        
        # Elimina el padding
        pad_length = decrypted_padded[-1]
        return decrypted_padded[:-pad_length].decode()


