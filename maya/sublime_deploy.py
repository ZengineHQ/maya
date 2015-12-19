import sys, os
from wg_util import get_plugin_context
from deploy import deploy

def sublime_deploy(current_file_path):

	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

	path_list = current_file_path.split(os.sep)

	try:
		plugin_name = path_list[path_list.index('plugins') + 1]

		context = get_plugin_context(plugin_name)

		deploy(context)

	except ValueError:
		print 'Build failed: file is outside the context of a plugin'
