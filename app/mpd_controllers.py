from mpd import MPDClient
from mpd import base as excepts
from config import Config
from flask import jsonify

client = MPDClient()

def on_song_upload(song_location):
    '''On song upload, add the song to the playlist from the
    file URI passed. If the player is currently stopped, start
    playback.'''
    try:
        client.status()
    except excepts.ConnectionError:
        client.connect(Config.mpd_socket)
    print(song_location)
    client.add(song_location)
    if client.status()['state'] == 'stop':
        client.play()
    client.disconnect()

def get_playlist():
    '''Connect to player, get playlist information, parse it for
    simpler display into a list, return list as json.'''
    track_list = []
    try:
        client.status()
    except excepts.ConnectionError:
        client.connect(Config.mpd_socket)
    current_playlist = client.playlistid()
    client.disconnect()
    for pos in range(len(current_playlist)):
        try:
            duration = int(current_playlist[pos]['time'])
        except KeyError:
            duration = 0
        if duration != 0:
            min = int(duration/60)
            sec = int(duration%60)
            time = " (" + str(min) + ":" + format(sec, '02d') + ")"
        try:
            track_title = current_playlist[pos]['title']
        except KeyError:
            track_title = current_playlist[pos]['file'][len(Config.UPLOAD_FOLDER):]
            
        try:
            track_artist = current_playlist[pos]['artist']
        except KeyError:
            track_artist = "Unknown"
        if track_artist != "Unknown":
            full_info = track_artist + " - " + track_title + time
        else:
            full_info = track_title + time
        track_list.append(full_info)
    track_list.reverse()
    return jsonify(track_list)
	    

'''
To do as needed.

1) Work with getting some form of database display.
2) Track skip. Voting to be handled by the page itself.
3) Better exception handling... pls.
'''
