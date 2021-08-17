import os, re

from config import video_extension_key, m3u_header_directive

def read_playlist_file(name):
	with open(name) as f:
		return [x.strip() for x in f.readlines()]

def parse_m3u(content):
	if len(content) == 0 or content[0] != m3u_header_directive:
		return False, content

	result = []

	content = content[1:]
	for i in range(0, len(content), 3):
		# get 3 elements in one step
		segment = content[i:i + 3]
		result.append({
			# #EXTINF: 0,<name>
			'title': re.search(r'(?<=#EXTINF: 0,).+', segment[0]).group(0),

			# #EXTVLCOPT:http-user-agent=<agent>
			# not used
			# 'user-agent': re.search(r'(?<=#EXTVLCOPT:http-user-agent=).+', segment[1]).group(0),

			# <link>
			'link': segment[2],
			video_extension_key: re.search(r'.+\.(\w+)', segment[2]).group(1),
		})

	return True, result

def read_playlist(name):
	content = read_playlist_file(name)
	status, data = parse_m3u(content)

	if status == False:
		quit(f'Playlist is empty or first line is not {m3u_header_directive}')

	return data
