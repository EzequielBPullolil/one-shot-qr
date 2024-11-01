import os
def remove_qr(qrName: str):
    qr_code_path = "./tmp/" + qrName
    os.remove(qr_code_path)