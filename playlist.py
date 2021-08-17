import os, re

from config import video_extension_key, template_keys

def read_file_lines(name):
	with open(name) as f:
		return [x.strip() for x in f.readlines()]

def parse_playlist(content):
	if len(content) == 0 or not re.match(r'#EXTM3U', content[0]):
		return False, None

	result, buffer = [], {}

	for line in content[1:]:
		if re.match(r'#EXTINF:', line):
			if buffer:
				result.append(buffer)

			# get title
			data = re.search(r'(?<=#EXTINF:).+', line).group(0)
			title = re.search(r'.+,([^,]+)', data).group(1)
			buffer['title'] = title
		elif line and line[0] != '#':
			# line without directive, get link
			buffer.update({
				'link': line,
				# now support only files with direct link
				# http://path/name.(ext) or http://path/name.(ext)?query=1
				video_extension_key: re.search(r'\/[^?#]+\.(\w+)', line).group(1),
			})

	return True, result

def read_playlist(name):
	content = read_file_lines(name)
	status, data = parse_playlist(content)

	if status == False:
		quit(f'Playlist is empty or file is not valid m3u/m3u8 playlist')

	return data
