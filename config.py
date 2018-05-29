class Config(object):
    SECRET_KEY = "justakey"
    UPLOAD_FOLDER = "/srv/dev-disk-by-label-Intermediates/webapps/radio/uploaded_content/"
    MAX_CONTENT_LENGTH = 1024 * 1024 * 50
    mpd_socket = '/run/mpd/socket'
    ALLOWED_EXTENSIONS = ['mp3', 'flac', 'ogg', 'm4a', 'wav']
    WIT_REMARKS = ["Music is better with others... Sometimes.",
        "The best way to party.",
        "They can't all be gold, give me a break.",
        "If it ain't broke, don't fix it!",
        "No complaints allowed.",
        "What do you really want from me?",
        "Give me some ideas as to what to say here!"]
