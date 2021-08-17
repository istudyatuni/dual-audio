from dataclasses import dataclass, field
import os, re

from config import video_extension_key, template_keys

@dataclass
class Playlist_template():
	header: list = field(default_factory=list)

	lines_in_item: int = 0

	title_line: int = 0
	title_regex: str = ''

	link_line: int = 0
	link_regex: str = ''

def read_file_lines(name):
	with open(name) as f:
		return [x.strip() for x in f.readlines()]

def parse_playlist(content, template):
	if len(content) == 0 or not is_correct_header(content, template.header):
		return False, content

	result = []

	content = content[1:]
	for i in range(0, len(content), template.lines_in_item):
		# get whole item in one step
		segment = content[i:i + template.lines_in_item]
		result.append({
			'title': re.search(template.title_regex, segment[template.title_line]).group(0),
			'link': re.search(template.link_regex, segment[template.link_line]).group(0),
			# now support only files with direct link
			# path/name.(ext) or path/name.(ext)?query=1
			video_extension_key: re.search(r'\/[^?#]+\.(\w+)', segment[2]).group(1),
		})

	return True, result

def read_playlist(name, template):
	content = read_file_lines(name)
	status, data = parse_playlist(content, template)

	if status == False:
		quit(f'Playlist is empty or header is not {template.header}')

	return data

def make_regex(splited_line):
	# if any element in splited_line is empty, regex will still work
	return '(?<={}).+(?={})'.format(*splited_line)

def parse_playlist_template(name):
	content = read_file_lines(name)

	split_by = content.index('---')
	header = content[:split_by]
	item = content[split_by + 1:]

	for ind, line in enumerate(item):
		if re.search(template_keys['title'], line):
			reg = line.split(template_keys['title'])
			title_regex = make_regex(reg)
			title_ind = ind
		elif re.search(template_keys['link'], line):
			reg = line.split(template_keys['link'])
			link_regex = make_regex(reg)
			link_ind = ind

	return Playlist_template(
		header = header,
		lines_in_item = len(item),

		title_line = title_ind,
		title_regex = title_regex,

		link_line = link_ind,
		link_regex = link_regex,
	)

def is_correct_header(content, header):
	# https://stackoverflow.com/a/32149245
	return content[:len(header)] == header
