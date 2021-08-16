import os

def check_system_utilities():
	from config import needed_utilities as utilities

	missing = []
	for u in utilities:
		res = os.system(f'which {u} > /dev/null')
		if res:
			missing.append(u)

	if len(missing) == 0:
		return

	print('Please, install this packages/utilities in system:')
	for m in missing:
		print(m)

	quit()

def setup():
	check_system_utilities()

	from config import needed_dirs as dirs
	for d in dirs:
		os.makedirs(d, exist_ok=True)
