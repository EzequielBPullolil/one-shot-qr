from .services.generateQR import generate_qr
from .services.removeQr import remove_qr
from flask import Flask, render_template, request, send_file, session

app = Flask(__name__)

app.secret_key = "s"
@app.get("/")
def renderHomePage():
    if 'ip' not in session:
        session['ip'] = request.remote_addr
    return render_template('index.html')
@app.route('/tmp/<path:filename>')
def serve_image(filename):
    return send_file(f'../tmp/{filename}')


@app.post("/qr")
def generateQr():

    url, cap = request.form["url"], request.form["cap"]
    

    
    qrCode_name = generate_qr(url)
    session['qrCode_name'] = qrCode_name
    return render_template('qr_code.html', qr_code_path=qrCode_name)