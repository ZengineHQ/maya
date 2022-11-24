import os
import json
from .exception import MayaException
from .plugin_create import create_frontend_plugin, add_frontend_plugin_to_config
from .wg_util import convertToDashCase

def init(args):
    folder = args['<plugin>']
    dashFolder = convertToDashCase(folder)
    if os.path.exists(dashFolder):
        raise MayaException('Error: Already Exists!')
    os.makedirs(dashFolder)

    #TODO: Move me to the backend creation part
    os.makedirs(dashFolder + '/backend')

    create_frontend_plugin(folder, True)

    defaultJSON = {
        "environments": {
            "stage": {
                "api_endpoint": "platform.zenginehq.com",
                "access_token": "[insert developer token here]",
                "plugins": {},
                "default": "true"
            }
        }
    }

    defaultJSON = add_frontend_plugin_to_config(defaultJSON, folder)

    dname = os.getcwd() + '/' + dashFolder
    maya = open(dname + '/maya.json', 'w')
    json.dump(defaultJSON, maya, indent=2)
    maya.close()

    print('Done.')
