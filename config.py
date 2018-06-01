class Config(object):
    SECRET_KEY = "justakey"
    
    # This determines where uploaded files will be kept.
    UPLOAD_FOLDER = "/srv/dev-disk-by-label-Intermediates/webapps/radio/uploaded_content/"

    # This determines the max file size allowed by Flask.
    MAX_CONTENT_LENGTH = 1024 * 1024 * 50

    # This is the Unix socket path to allow MPD control.
    mpd_socket = '/run/mpd/socket'
    
    # These are the extensions kept for upload.
    ALLOWED_EXTENSIONS = ['mp3', 'flac', 'ogg', 'm4a', 'wav']

    # This is the IP and port of the Redis host, used for tracking users.
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = "6789"


   
    ''' These configuration options affect the web-app. '''
    
    # This is the title shown on the page.
    PAGE_TITLE = "Community Driven Radio"

    # These are the subheadings shown under the title of the page.
    WIT_REMARKS = ["Music is better with others... Sometimes.",
        "The best way to party.",
        "They can't all be gold, give me a break.",
        "If it ain't broke, don't fix it!",
        "No complaints allowed.",
        "What do you really want from me?",
        "Give me some ideas as to what to say here!"]
    
    # Stream source for audio element.
    STREAM_SOURCE = ""
    
    # Link for external players.
    EXT_LINK = ""
