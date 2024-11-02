import threading
from base64 import urlsafe_b64encode
from cryptography.fernet import Fernet
import shortuuid
class UrlManager:
    def __init__(self, appHost : str, encryptCode: str):
        print(appHost, encryptCode)
        self.__app_host = appHost
        self.__encrypt = self.__generateEncrypter(encryptCode)
    

    def __generateEncrypter(self, encryptCode):
        if len(encryptCode) < 32:
            custom_code = encryptCode.ljust(32)
            code = urlsafe_b64encode(custom_code.encode())
            print(code)
        self.__encrypt = Fernet(code)

        return Fernet(code)


    def generate_qr_url(self, url: str, cap: int) -> str:
        encrypted_url = self.__encrypt_url(url)
        url_id = shortuuid.uuid()
        thread = threading.Thread(
            target=self.__persist_url_shortcut_and_cap,
            name="one_shot_qr",
            args=(encrypted_url, url_id, cap)
        )
        thread.start()
        return self.__generate_shortcut_url(url_id)
    

    def __encrypt_url(self,url) -> str:
        return self.__encrypt.encrypt(b'{url}')


    def __generate_shortcut_url(self, uuid: str) -> str:
        return f'{self.__app_host}/shortcut/{uuid}'

    def __persist_url_shortcut_and_cap(self, encryptedUrl, shortcutUrl: str, cap: int): 
        pass 