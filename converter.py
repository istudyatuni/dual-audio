import os, re

from config import audio_dir, video_cache_dir, partial_postfix
from helpers import get_system_output

def check_audio_format(filepath):
	# https://stackoverflow.com/a/21789183
	# https://stackoverflow.com/a/28769074
	video_stats = get_system_output(('ffprobe', os.path.abspath(filepath)))
	return re.search(r'Audio: (\w+)', video_stats).group(1)

def extract_audio(videos, cache_key, out_dir):
	for v in videos:
		video_cache_file = os.path.join(out_dir, video_cache_dir, v[cache_key])
		audio_format = check_audio_format(video_cache_file)

		audio_file = os.path.join(out_dir, audio_dir, f"{v['title']}.{audio_format}")

		if os.path.exists(audio_file):
			continue

		not_finished_file = audio_file + partial_postfix
		# https://stackoverflow.com/a/63237888
		# -n is do not overwrite existing files, 0:a:0 is get from '0' input 'audio' with number '0'
		# -c copy is do not convert audio stream
		result = os.system(f"""
			ffmpeg \
			-i '{video_cache_file}' \
			-map 0:a:0 \
			-c copy '{not_finished_file}'
		""")

		# 0 if convert successfully, 256 if file exist
		if result == 0:
			os.system(f"mv '{not_finished_file}' '{audio_file}'")
		elif result == 256:
			print('file', not_finished_file, 'exists')
		else:
			print('result code:', result)
