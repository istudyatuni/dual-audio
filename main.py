from setup import setup
from playlist import read_playlist, parse_m3u
from loader import load_files_from_list
from converter import extract_audio

def main():
	content = read_playlist('playlist.m3u')
	status, data = parse_m3u(content)

	if status == False:
		quit('Something wrong')

	loaded_videos = load_files_from_list(data)
	extract_audio(loaded_videos)

if __name__ == '__main__':
	setup()
	main()
