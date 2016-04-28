import os
import sys
from wg_util import get_plugin_context
from deploy import deploy


def sublime_deploy(current_file_path, args):
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    plugin_name = find_plugin_name(current_file_path)
    if not plugin_name:
        print 'Build failed: file is outside the context of a plugin'
        return
    context = get_plugin_context(plugin_name)
    deploy(context, args)


def find_plugin_name(current_file_path):
    path_list = current_file_path.split(os.sep)
    try:
        return path_list[path_list.index('plugins') + 1]
    except ValueError:
        pass
