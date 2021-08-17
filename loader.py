import os

from config import partial_postfix

def load_files_from_list(data, cache_key, out_dir, media_dir):
	loaded_files = []
	for d in data:
		# -O is out filename, -c is continue
		filename = f"{d['title']}.{d['extension']}"
		file_path = os.path.join(out_dir, media_dir, filename)

		if os.path.exists(file_path):
			# just for message
			os.system(f"wget -O '{file_path}' -nc -c '{d['link']}'")
			continue

		not_finished_file = file_path + partial_postfix
		result = os.system(f"wget -O '{not_finished_file}' -c '{d['link']}'")

		if result == 0:
			# download successfully
			os.system(f"mv '{not_finished_file}' '{file_path}'")
			loaded_files.append({**d, cache_key: filename})
		elif result == 2:
			# SIGINT (ctrl+C)
			quit('\nExiting')
		else:
			print('result code:', result)

	return loaded_files
