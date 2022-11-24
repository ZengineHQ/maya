import os
import json
from .wg_util import convertToDashCase
from .plugin_create import create_frontend_plugin, add_frontend_plugin_to_config
from pprint import pprint

def add(args):
    folder = args['<plugin>']
    dashFolder = convertToDashCase(folder)
    pluginType = 'frontend'
    if (args['--backend']):
        pluginType = 'backend'

    if pluginType == 'backend':
        print("Maya currently only supports adding a frontend plugin with the add command. Exiting.")
        return

    if not os.path.exists('maya.json'):
        print("Add must be run from the plugins root directory (where maya.json is). Exiting.")
        return

    create_frontend_plugin(folder)

    config = json.load(open('maya.json'))
    config = add_frontend_plugin_to_config(config, folder);
    maya = open('maya.json', 'w')
    json.dump(config, maya, indent=2)
    maya.close()

    print('Done.')
