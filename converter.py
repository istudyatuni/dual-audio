import os, re, subprocess
from config import audio_dir, video_dir

def check_audio_format(filename):
	filepath = os.path.join(video_dir, filename)

	# https://stackoverflow.com/a/21789183
	# https://stackoverflow.com/a/28769074
	video_stats = subprocess.Popen(
		('ffprobe', os.path.abspath(filepath)),
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,  # get all output
		universal_newlines=True,  # return string not bytes
	).communicate()[0]
	return re.search(r'Audio: (\w+)', video_stats).group(1)

def extract_audio(videos):
	for v in videos:
		audio_format = check_audio_format(v['video_file'])
		audio_file = os.path.join(audio_dir, f"{v['title']}.{audio_format}")
		# https://stackoverflow.com/a/63237888
		# -n is do not overwrite existing files, 0:a:0 is get from '0' input 'audio' with number '0'
		# -c copy is do not convert audio stream
		res = os.system(f"""
			ffmpeg -n \
			-i '{os.path.join(video_dir, v['video_file'])}' \
			-map 0:a:0 \
			-c copy '{audio_file}'
		""")

		# 0 if convert successfully, 256 if file exist
		if res not in (0, 256):
			print(res)
