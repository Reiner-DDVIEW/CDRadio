class Config(object):
    SECRET_KEY = "justakey"
    UPLOAD_FOLDER = "/srv/dev-disk-by-label-Intermediates/webapps/radio/uploaded_content/"
    MAX_CONTENT_LENGTH = 1024 * 1024 * 50
    mpd_socket = '/run/mpd/socket'
    ALLOWED_EXTENSIONS = ['mp3', 'flac', 'ogg', 'm4a', 'wav']
