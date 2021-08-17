import argparse, os, shlex

from config import video_cache_key, video_key, video_cache_dir, video_dir
from converter import extract_audio
from helpers import setup_checks
from loader import load_files_from_list
from playlist import read_playlist, parse_m3u

def init_argparser():
	parser = argparse.ArgumentParser(description='Make dual-audio movie')
	parser.add_argument('-a', '--audio-playlists', nargs='*', help='Path(s) to playlist(s) with videos from which extract audio', default=[])
	parser.add_argument('-v', '--video-playlists', nargs='*', help='Path(s) to playlist(s) with videos to add a second audio', default=[])
	parser.add_argument('-d', '--out-dir', type=str, help='Directory where place audio and video folders', default='.')
	parser.add_argument('--args', type=str, help='File with shell arguments')

	args = parser.parse_args()

	if args.args:
		with open(os.path.abspath(args.args)) as args_file:
			args = parser.parse_args(shlex.split(args_file.read(), comments=True))

	return args

def main(audio_playlists, video_playlists, out_directory):
	out_dir = os.path.abspath(out_directory)

	for p in audio_playlists:
		content = read_playlist(os.path.abspath(p))
		status, data = parse_m3u(content)

		if status == False:
			quit('Something wrong')

		# load videos for audio extracting
		loaded_cache_videos = load_files_from_list(data, video_cache_key, out_dir, video_cache_dir)
		extract_audio(loaded_cache_videos, video_cache_key, out_dir)

	for p in video_playlists:
		content = read_playlist(os.path.abspath(p))
		status, data = parse_m3u(content)

		if status == False:
			quit('Something wrong')

		# load videos for audio appending
		loaded_videos = load_files_from_list(data, video_key, out_dir, video_dir)
		print(loaded_videos)

if __name__ == '__main__':
	args = init_argparser()
	setup_checks(args.out_dir)
	main(args.audio_playlists, args.video_playlists, args.out_dir)
