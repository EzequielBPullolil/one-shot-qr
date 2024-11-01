import qrcode
from datetime import datetime
def generate_qr(url: str) -> str:
    ''' 
        Generates a qrCode using  
    ''' 
    file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    path = "./tmp/" + file_name
    print(path)
    img = qrcode.make(url)

    img.save(path)
    return file_name