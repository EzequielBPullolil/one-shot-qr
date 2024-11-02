import threading
import shortuuid
from base64 import urlsafe_b64encode, urlsafe_b64decode
from cryptography.fernet import Fernet
from .UrlEncryptor import UrlEncryptor
from ..database.Url import UrlModel
class UrlManager:
    def __init__(self, appHost : str, encryptCode: str):
        self.__app_host = appHost
        self.__encrypter = UrlEncryptor(encryptCode)

    def generate_qr_url(self, url: str, cap: int) -> str:

        encrypted_url = self.__encrypter.encrypt(url)
        url_id = shortuuid.uuid()
        thread = threading.Thread(
            target=self.__persist_url_shortcut_and_cap,
            name="one_shot_qr",
            args=(url_id, encrypted_url, cap)
        )
        thread.start()
        return self.__generate_shortcut_url(url_id)

    def __generate_shortcut_url(self, uuid: str) -> str:
        return f'{self.__app_host}/shortcut/{uuid}'


    def find_real_url(self, uuid: str, host_ip) -> str:
        encrypted_url_str = UrlModel.read_and_decrease_cap(uuid)

        decriptedUrl = self.__encrypter.decrypt(encrypted_url_str)
        return decriptedUrl


    def __persist_url_shortcut_and_cap(self,url_id, encryptedUrl, cap: int): 
        UrlModel.create(url_id, encryptedUrl, cap)