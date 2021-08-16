import argparse, os

from setup import setup
from playlist import read_playlist, parse_m3u
from loader import load_files_from_list
from converter import extract_audio

def init_argparser():
	parser = argparse.ArgumentParser(description='Make dual-audio movie')
	parser.add_argument('-a', '--audio-playlist', type=str, help='Path to playlist with videos from which extract audio', default='audio-playlist.m3u')
	parser.add_argument('-v', '--video-playlist', type=str, help='Path to playlist with videos to add a second audio', default='video-playlist.m3u')
	parser.add_argument('-d', '--out-dir', type=str, help='Directory where place audio and video folders', default='')
	return parser.parse_args()

def main(audio_playlist, out_directory):
	content = read_playlist(os.path.abspath(audio_playlist))
	status, data = parse_m3u(content)

	if status == False:
		quit('Something wrong')

	out_dir = os.path.abspath(out_directory)
	loaded_videos = load_files_from_list(data, out_dir)
	extract_audio(loaded_videos, out_dir)

if __name__ == '__main__':
	args = init_argparser()
	setup()
	main(args.audio_playlist, args.out_dir)
