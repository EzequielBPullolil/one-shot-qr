'''
QrCodeManager class container
'''
from io import BytesIO
import base64
import qrcode
class QrCodeManager():
    '''
        QrCodeManager generate the qr code from passed url
    '''
    def __init__(self, url: str):
        self.__url = url

    def generate_qr(self)->bytes:
        '''
            Generates qr code using the url passed by parameter
        '''
        img = qrcode.make(self.__url)
        buf = BytesIO()
        img.save(buf, format="PNG")
        qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return qr_base64
