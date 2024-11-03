'''
_
'''
import threading
import shortuuid
from .url_encryptor import UrlEncryptor
from ..database.url import UrlModel
class UrlManager:
    '''
        UrlManager provide url services to the Flask routes
    '''
    def __init__(self, app_host : str, encrypt_code: str):
        self.__app_host = app_host
        self.__encrypter = UrlEncryptor(encrypt_code)

    def generate_qr_url(self, url: str, cap: int) -> str:
        '''
            Generate the url shortcut for the qr code 
            and persit it encrypted in the DB

        '''
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


    def find_real_url(self, uuid: str) -> (str, int):
        '''
            Provides the actual decrypted URL and URL limit associated with url_uuid
        '''
        (encrypted_url_str, cap) = UrlModel.read_and_decrease_cap(uuid)
        return (self.__encrypter.decrypt(encrypted_url_str), cap)


    def __persist_url_shortcut_and_cap(self,url_uuid, encrypted_url, cap: int):
        '''
            Persist the url in the db
        '''
        UrlModel.create(url_uuid, encrypted_url, cap)
