from os import environ
from .services.QrCodeManager import QrCodeManager
from flask import Flask, render_template, request, send_file, session, after_this_request, json
import os 
app = Flask(__name__)

app.config['TMP_DIR'] = environ.get("TMP_DIR")
app.config['URL_ENCRYPT_CODE'] = environ.get("URL_ENCRYPT_CODE")
app.secret_key = environ.get("SECRET_KEY")
@app.get("/")
def renderHomePage():
    return render_template('index.html')

@app.post("/qr")
def generateQr():
    url, cap = request.form["url"], request.form["cap"]
    qrManager = QrCodeManager(url)
    
    qrCode = qrManager.generate_qr()

    session["qrCode"] = qrCode
    return render_template('qr_code.html', qr_image=qrCode)