import os, re

from config import audio_dir, video_cache_dir
from helpers import get_system_output

def check_audio_format(filepath):
	# https://stackoverflow.com/a/21789183
	# https://stackoverflow.com/a/28769074
	video_stats = get_system_output(('ffprobe', os.path.abspath(filepath)))
	return re.search(r'Audio: (\w+)', video_stats).group(1)

def extract_audio(videos, out_dir):
	for v in videos:
		video_file = os.path.join(out_dir, video_cache_dir, v['video_file'])
		audio_format = check_audio_format(video_file)

		audio_file = os.path.join(out_dir, audio_dir, f"{v['title']}.{audio_format}")
		# https://stackoverflow.com/a/63237888
		# -n is do not overwrite existing files, 0:a:0 is get from '0' input 'audio' with number '0'
		# -c copy is do not convert audio stream
		res = os.system(f"""
			ffmpeg -n \
			-i '{video_file}' \
			-map 0:a:0 \
			-c copy '{audio_file}'
		""")

		# 0 if convert successfully, 256 if file exist
		if res not in (0, 256):
			print('result code:', res)
