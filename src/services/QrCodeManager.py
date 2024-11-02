import qrcode
from io import BytesIO
import base64
from flask import current_app
from datetime import datetime
class QrCodeManager():
    def __init__(self, url: str):
        self._file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        self._path = f'{current_app.config.get('TMP_DIR')}/{self._file_name}'
    
    def generate_qr(self): 
        img = qrcode.make(self._path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return qr_base64

    def get_qr_id(self) -> str:
        return self._file_name