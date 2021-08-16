import os
from config import video_dir

def load_files_from_list(data):
	loaded_files = []
	for video in data:
		# -O is out filename, -c is continue
		filename = f"{video['title']}.{video['extension']}"
		result = os.system(f"wget -O '{os.path.join(video_dir, filename)}' -c '{video['link']}'")

		# 0 if download successfully, 256 if file exist
		if result in (0, 256):
			loaded_files.append({**video, 'video_file': filename})
		elif result == 2:
			# SIGINT (ctrl+C)
			quit('\rExiting')
		else:
			print('result code:', result)

	return loaded_files
