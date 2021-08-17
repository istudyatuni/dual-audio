import os, subprocess

def get_system_output(args):
	return subprocess.Popen(
		args,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,  # get all output
		universal_newlines=True,  # return string not bytes
	).communicate()[0]

def check_system_utilities():
	from config import needed_utilities as utilities

	missing = []
	for u in utilities:
		if os.system(f'which {u} > /dev/null'):
			missing.append(u)

	if len(missing) == 0:
		return

	print('Please, install this packages/utilities in system:')
	for m in missing:
		print(m)

	quit()

def setup_checks(out_directory):
	check_system_utilities()

	out_dir = os.path.abspath(out_directory)

	from config import needed_dirs as dirs
	for d in dirs:
		os.makedirs(os.path.join(out_dir, d), exist_ok=True)
