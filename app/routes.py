from flask import render_template, redirect, url_for, request, jsonify
from werkzeug import secure_filename
from app import app
from config import Config
import app.mpd_controllers as mpd_controllers
import app.database as database
import os
from random import randint

def allow_file(file_name):
    ''' Only allow certain file types as determined by the config. '''
    return file_name.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
@app.route('/index')
def index():
    remark = app.config['WIT_REMARKS'][randint(0, len(app.config['WIT_REMARKS'])-1)]
    title = app.config['PAGE_TITLE']
    ext_link = app.config['EXT_LINK']
    stream_source = app.config['STREAM_SOURCE']
    return render_template('test.html', remark=remark, title=title, ext_link=ext_link, stream_source=stream_source)

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        ''' Get user IP, behind reverse-proxy or not. '''
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            uploader_ip = request.environ['REMOTE_ADDR']
            print("No forwarding: %s" % uploader_ip)
        else:
            uploader_ip = request.environ['HTTP_X_FORWARDED_FOR']
            print("Forward enabled: %s" % uploader_ip)
        uploaded_file = request.files['file']
        if not database.user_allowed(uploader_ip):
            print("User is not allowed to upload currently.")
            return jsonify({'upload': False, 'reason': "You cannot upload at this time."})
        if allow_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            song_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(song_path)
            mpd_controllers.on_song_upload(song_path, uploader_ip)
            print("File get!")
            return jsonify({'upload': True, 'reason': "N/A"})
        else:
            print("File rejected!")
            print(uploaded_file)
            return jsonify({'upload': False, 'reason': "Please check file type and size."})
    else:
        ''' Return to index on GET request.'''
        return redirect(url_for('index'))

@app.route('/playlist')
def return_playlist():
    return mpd_controllers.get_playlist()

@app.route('/allowed')
def isUserAllowed():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        user_ip = request.environ['REMOTE_ADDR']
    else:
        user_ip = request.environ['HTTP_X_FORWARDED_FOR']
    allowed = database.user_allowed(user_ip)
    if allowed == True:
        return jsonify({'upload_allowed': True})
    else:
        return jsonify({'upload_allowed': False})