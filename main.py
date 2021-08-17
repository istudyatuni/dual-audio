import argparse, os, shlex

from config import (
	video_cache_key,
	audio_key, video_key,
	video_cache_dir, video_dir,
	video_extension_key
)
from converter import extract_audio, append_audios
from helpers import setup_checks, get_filenames
from loader import load_files_from_list
from playlist import read_playlist, parse_playlist_template

def init_argparser():
	parser = argparse.ArgumentParser(description='Make dual-audio movie')

	# playlists
	parser.add_argument('-a', '--audio-playlists', nargs='*', help='Path(s) to playlist(s) with videos from which extract audio', default=[])
	parser.add_argument('-v', '--video-playlists', nargs='*', help='Path(s) to playlist(s) with videos to add a second audio', default=[])

	# playlist templates
	parser.add_argument('--template', type=str, help='Path to template of playlist (if both audio and video playlists are the same format)')
	parser.add_argument('--audio-template', type=str, help='Path to template of playlist with audio (videos to extract audio). Ignored if --template specified')
	parser.add_argument('--video-template', type=str, help='Path to template of playlist with videos. Ignored if --template specified')

	# other
	parser.add_argument('-d', '--out-dir', type=str, help='Directory where place audio and video folders', default='.')
	parser.add_argument('--preserve-video', action='store_true', help='Preserving main video')
	parser.add_argument('--args', type=str, help='File with shell arguments')

	args = parser.parse_args()

	if args.args:
		with open(os.path.abspath(args.args)) as args_file:
			args = parser.parse_args(shlex.split(args_file.read(), comments=True))

	return args

def main(
	audio_playlists, video_playlists,
	out_dir,
	preserve_video,
	template,
	audio_template, video_template,
):
	abs_out_dir = os.path.abspath(out_dir)

	if template:
		playlist_template = parse_playlist_template(template)
	else:
		playlist_template = parse_playlist_template(audio_template)

	for p in audio_playlists:
		data = read_playlist(os.path.abspath(p), playlist_template)

		# load videos for audio extracting
		loaded_cache_videos = load_files_from_list(
			data,
			video_cache_key,
			abs_out_dir,
			video_cache_dir,
			video_extension_key,
		)
		audio_index = extract_audio(loaded_cache_videos, video_cache_key, abs_out_dir)

	if not template:
		playlist_template = parse_playlist_template(video_template)

	for p in video_playlists:
		data = read_playlist(os.path.abspath(p), playlist_template)

		# load videos for audio appending
		videos_index = load_files_from_list(
			data,
			video_key,
			abs_out_dir,
			video_dir,
			video_extension_key,
		)

	filenames = get_filenames(audio_index, videos_index)
	append_audios(filenames, abs_out_dir, preserve_video)

if __name__ == '__main__':
	args = init_argparser()
	setup_checks(args.out_dir)
	main(
		args.audio_playlists,
		args.video_playlists,
		args.out_dir,
		args.preserve_video,
		args.template,
		args.audio_template,
		args.video_template,
	)
	print('Done')
