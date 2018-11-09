from __future__ import unicode_literals
import youtube_dl
import time
from config import Config

def get_youtube_audio(link):
	fileout = Config.UPLOAD_FOLDER + '%(title)s.%(ext)s'
	options = {
		'format': 'bestaudio',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'vorbis',
			'preferredquality': '3'
		},{
			'key': 'FFmpegMetadata'
		}],
		'nocheckcertificate': True,
		'noprogress': True,
		'outtmpl': fileout
	}
	with youtube_dl.YoutubeDL(options) as ydl:
		info = ydl.extract_info(link, download=True)
	duration = info['duration']
	fakename = ydl.prepare_filename(info)
	filename = fakename.rsplit('.', 1)[0] + '.ogg'
	passed_info = {'file': filename, 'time': duration}
	print(passed_info)
	return passed_info