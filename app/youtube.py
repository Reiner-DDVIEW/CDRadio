from __future__ import unicode_literals
import youtube_dl
from youtube_dl.postprocessor.ffmpeg import FFmpegMetadataPP
import time
from config import Config

class FFmpegMP3MetadataPP(FFmpegMetadataPP):

		def __init__(self, downloader=None, metadata=None):
				self.metadata = metadata or {}
				super(FFmpegMP3MetadataPP, self).__init__(downloader)

		def run(self, information):
				information = self.purge_metadata(information)
				information.update(self.metadata)
				return super(FFmpegMP3MetadataPP, self).run(information)

		def purge_metadata(self, info):
				info.pop('track', None)
				info.pop('upload_date', None)
				info.pop('description', None)
				info.pop('webpage_url', None)
				info.pop('track_number', None)
				info.pop('artist', None)
				info.pop('creator', None)
				info.pop('uploader', None)
				info.pop('uploader_id', None)
				info.pop('genre', None)
				info.pop('album', None)
				info.pop('album_artist', None)
				info.pop('disc_number', None)
				return info

def get_youtube_audio(link):
	fileout = Config.UPLOAD_FOLDER + '%(title)s.%(ext)s'

	options = {
		'format': 'bestaudio',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'vorbis',
			'preferredquality': '3'
		}],
		'nocheckcertificate': True,
		'noprogress': True,
		'outtmpl': fileout
	}
	
	# In case you want to override other metadata parts later
	metadata = {

	}

	with youtube_dl.YoutubeDL(options) as ydl:
		ffmpeg_mp3_metadata_pp = FFmpegMP3MetadataPP(ydl, metadata)
		ydl.add_post_processor(ffmpeg_mp3_metadata_pp)
		info = ydl.extract_info(link, download=True)
	duration = info['duration']
	fakename = ydl.prepare_filename(info)
	filename = fakename.rsplit('.', 1)[0] + '.ogg'
	passed_info = {'file': filename, 'time': duration}
	print(passed_info)
	return passed_info