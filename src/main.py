from os import environ
from .services.QrCodeManager import QrCodeManager
from flask import Flask, render_template, request, send_file, session, after_this_request, json
import os 
app = Flask(__name__)

app.config['TMP_DIR'] = environ.get("TMP_DIR")
app.config['URL_ENCRYPT_CODE'] = environ.get("URL_ENCRYPT_CODE")
app.secret_key = "s"
@app.get("/")
def renderHomePage():
    return render_template('index.html')
    
@app.get('/tmp/<path:filename>')
def serve_image(filename):
    return send_file(f'{app.config.get('TMP_DIR')}/{filename}')


@app.delete('/tmp/<path:filename>')
def delete_image(filename):
    os.remove(f'{app.config.get('TMP_DIR')}/{filename}')
    return json.jsonify({})


@app.post("/qr")
def generateQr():
    url, cap = request.form["url"], request.form["cap"]
    qrManager = QrCodeManager(url)
    
    qrManager.generate_qr()

    return render_template('qr_code.html', qr_code_id=qrManager.get_qr_id())