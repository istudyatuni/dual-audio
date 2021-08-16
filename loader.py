import os
from config import video_cache_dir

not_downloaded_postfix = '-partial'

def load_files_from_list(data, out_dir):
	loaded_files = []
	for video in data:
		# -O is out filename, -c is continue
		filename = f"{video['title']}.{video['extension']}"
		file_path = os.path.join(out_dir, video_cache_dir, filename)

		if os.path.exists(file_path):
			# just for message
			os.system(f"wget -O '{file_path}' -nc -c '{video['link']}'")
			continue

		result = os.system(f"wget -O '{file_path + not_downloaded_postfix}' -c '{video['link']}'")

		if result == 0:
			# download successfully
			os.system(f"mv '{file_path + not_downloaded_postfix}' '{file_path}'")
			loaded_files.append({**video, 'video_file': filename})
		elif result == 2:
			# SIGINT (ctrl+C)
			quit('\nExiting')
		else:
			print('result code:', result)

	return loaded_files
