from flask import Flask, request, redirect, url_for, render_template, flash, session, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
AUTH_MODE = os.environ.get('AUTH_MODE', 'none')  # none | token | password
UPLOAD_TOKEN = os.environ.get('UPLOAD_TOKEN', 'changeme')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')

app = Flask(__name__)
app.config.update(UPLOAD_FOLDER=UPLOAD_FOLDER, SECRET_KEY=SECRET_KEY, MAX_CONTENT_LENGTH=4 * 1024 * 1024 * 1024)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def check_auth():
    if AUTH_MODE == 'none':
        return True
    if AUTH_MODE == 'token':
        token = request.headers.get('X-UPLOAD-TOKEN') or request.args.get('token')
        return token == UPLOAD_TOKEN
    if AUTH_MODE == 'password':
        return session.get('logged_in') is True
    return False


@app.route('/', methods=['GET'])
def index():
    if AUTH_MODE == 'password' and not check_auth():
        return redirect(url_for('login', next=request.path))
    return render_template('index.html', auth_mode=AUTH_MODE)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if AUTH_MODE != 'password':
        return redirect(url_for('index'))
    if request.method == 'POST':
        pwd = request.form.get('password')
        if pwd == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid password')
    return render_template('login.html')


@app.route('/upload', methods=['POST'])
def upload():
    if not check_auth():
        return jsonify({'error': 'unauthorized'}), 401
    if 'file' not in request.files:
        return jsonify({'error': 'no file uploaded'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'empty filename'}), 400
    filename = secure_filename(f.filename)
    target = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(target)

    # if the client appears to be a browser (prefers html) then redirect to the
    # browse UI so users can immediately navigate the uploaded files.
    if request.accept_mimetypes.accept_html and not request.accept_mimetypes.accept_json:
        return redirect(url_for('browse'))

    # otherwise return machine-readable JSON (used by curl/clients)
    return jsonify({'ok': True, 'filename': filename, 'path': target})


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# browsing UI for uploaded files
@app.route('/browse/', defaults={'req_path': ''})
@app.route('/browse/<path:req_path>')
def browse(req_path):
    # simple authentication check for UI, same as other pages
    if AUTH_MODE == 'password' and not check_auth():
        return redirect(url_for('login', next=request.path))

    base = app.config['UPLOAD_FOLDER']
    # compute absolute path and ensure it's within uploads folder
    abs_path = os.path.abspath(os.path.join(base, req_path))
    if not abs_path.startswith(os.path.abspath(base)):
        return "Invalid path", 400

    if os.path.isdir(abs_path):
        entries = []
        for entry in sorted(os.listdir(abs_path)):
            full = os.path.join(abs_path, entry)
            if os.path.isdir(full):
                entries.append({'name': entry, 'type': 'dir'})
            else:
                entries.append({'name': entry, 'type': 'file'})
        return render_template('browse.html', entries=entries, current=req_path)
    else:
        # if it's a file, just serve it
        return send_from_directory(base, req_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '5000')), debug=os.environ.get('DEBUG', '') == '1')
