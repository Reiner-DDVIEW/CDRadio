from flask import render_template, redirect, url_for, request
from werkzeug import secure_filename
from app import app
from config import Config
import app.mpd_controllers as mpd_controllers
import os

def allow_file(file_name):
    return file_name.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
@app.route('/index')
def index():
    return "Nothing here yet..."

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if allow_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            song_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(song_path)
            mpd_controllers.on_song_upload(song_path)
            print("File get!")
            return render_template('test.html')
        else:
            print("File rejected!")
            print(uploaded_file)
            return render_template('test.html')
    else:
        return render_template('test.html')

@app.route('/playlist')
def return_playlist():
    return mpd_controllers.get_playlist()
