""" Flask app and routes """
from os import environ
from flask import Flask, render_template, request, session
from .services.qr_code_manager import QrCodeManager
from .services.url_manager import UrlManager
app = Flask(__name__)

app.secret_key = environ.get("SECRET_KEY")
app.config['URL_ENCRYPT_CODE'] = environ.get(
    "URL_ENCRYPT_CODE", 'fake_encrypt')


@app.get("/")
def render_home():
    '''
    _ 
    '''
    return render_template('index.html')


@app.post("/qr")
def generate_qr():
    '''
        Generates a qr code using the url and cap data 
        received from form
    '''
    url, cap = request.form["url"], request.form["cap"]
    url_manager = UrlManager(
        app_host=app.config.get('APP_HOST'),
        encrypt_code=app.config.get('URL_ENCRYPT_CODE')
    )
    qr_url = url_manager.generate_qr_url(url, cap)
    qr_manager = QrCodeManager(qr_url)
    qr_code = qr_manager.generate_qr()

    session["qrCode"] = qr_code
    return render_template('qr_code.html', qr_image=qr_code)


@app.get("/shortcut/<string:url_uuid>")
def redirect_to_real_url(url_uuid):
    '''
        Uses the url_uuid proved by url param to find
        in the DB the url maped 
    '''
    if 'requested_host' in session:
        session_addrs, session_url_uuid = session['requested_host']
        if session_addrs == request.remote_addr and session_url_uuid == url_uuid:
            return render_template('error.html', error_name='You already claimed this url')

    session['requested_host'] = (request.remote_addr, url_uuid)
    print(app.config)
    url_manager = UrlManager(
        app_host=app.config.get('APP_HOST'),
        encrypt_code=app.config.get('URL_ENCRYPT_CODE')
    )

    try:
        (real_url, cap) = url_manager.find_real_url(
            uuid=url_uuid)
        return render_template('get_url.html', url=real_url, cap=cap)
    except:
        return render_template('error.html', error_name='Url not founded or cap exceded')
