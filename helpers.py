import subprocess

def get_system_output(args):
	return subprocess.Popen(
		args,
		stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT,  # get all output
		universal_newlines=True,  # return string not bytes
	).communicate()[0]
