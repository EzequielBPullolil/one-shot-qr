from os import environ
from .services.QrCodeManager import QrCodeManager
from .services.UrlManager import UrlManager
from flask import Flask, render_template, request, send_file, session, after_this_request, json, redirect
app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")

app.config['APP_HOST'] = environ.get("APP_HOST", 'http://localhost:5000')
app.config['URL_ENCRYPT_CODE'] = environ.get("URL_ENCRYPT_CODE",'fake_encrypt' )
@app.get("/")
def renderHomePage():
    return render_template('index.html')

@app.post("/qr")
def generateQr():
    url, cap = request.form["url"], request.form["cap"]
    url_manager = UrlManager(
        appHost =  app.config.get('APP_HOST'),
        encryptCode = app.config.get('URL_ENCRYPT_CODE')
    )
    qr_url = url_manager.generate_qr_url(url, cap)
    qrManager = QrCodeManager(qr_url)
    qrCode = qrManager.generate_qr()

    
    session["qrCode"] = qrCode
    return render_template('qr_code.html', qr_image=qrCode)


@app.get("/shortcut/<string:url_uuid>")
def redirect_to_real_url(url_uuid):
    url_manager = UrlManager(
        appHost =  app.config.get('APP_HOST'),
        encryptCode = app.config.get('URL_ENCRYPT_CODE')
    )
    
    return redirect(
        location=url_manager.find_real_url(
            uuid=url_uuid,
            host_ip=request.remote_addr), 
        code=302
    )