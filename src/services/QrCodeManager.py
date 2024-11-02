import qrcode

from flask import current_app
from datetime import datetime
class QrCodeManager():
    def __init__(self, url: str):
        self._file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        self._path = f'{current_app.config.get('TMP_DIR')}/{self._file_name}'
    
    def generate_qr(self): 
        img = qrcode.make(self._path)
        img.save(self._path)

    def get_qr_id(self) -> str:
        return self._file_name