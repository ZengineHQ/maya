import os
import json
from shutil import copyfile
from .exception import MayaException

def copyInitFile(source, dest):
    absPath = os.path.dirname(os.path.realpath(__file__))
    registration = absPath + '/default_files/' + source
    destination = os.getcwd() + dest
    copyfile(registration, destination)

def init(args):
    folder = args['<plugin>']
    if os.path.exists(folder):
        raise MayaException('Error: Already Exists!')
    os.makedirs(folder)
    os.makedirs(folder + '/backend')
    os.makedirs(folder + '/plugins')
    os.makedirs(folder + '/plugins/' + folder)
    os.makedirs(folder + '/plugins/' + folder + '/src')
    os.makedirs(folder + '/plugins/' + folder + '/src/controllers')
    os.makedirs(folder + '/plugins/' + folder + '/src/styles')
    os.makedirs(folder + '/plugins/' + folder + '/src/views')
    plugin = {}
    plugin[folder] = {
        "id": "DEFINE AS NUMBER",
        "namespace": "pluginOneNamespace",
        "route": "/plugin-one-route",
        "services": {
            "some-plugin1-service": {
                "id": "DEFINE AS NUMBER"
            }
        }
    }
    defaultJSON = {
        "environments": {
            "stage": {
                "api_endpoint": "platform.zenginehq.com",
                "access_token": "[insert developer token here]",
                "plugins": plugin,
                "default": "true"
            }
        }
    }

    dname = os.getcwd() + '/' + folder
    maya = open(dname + '/maya.json', 'w')
    json.dump(defaultJSON, maya, indent=2)
    maya.close()

    copyInitFile('default-plugin-register.js', '/' + folder + '/plugins/' + folder + '/plugin-register.js')
    copyInitFile('default-controller.js', '/' + folder + '/plugins/' + folder + '/src/controllers/controller.js')
    copyInitFile('default-settings-controller.js', '/' + folder + '/plugins/' + folder + '/src/controllers/settings-controller.js')
    copyInitFile('default-template.html', '/' + folder + '/plugins/' + folder + '/src/views/main.html')
    copyInitFile('default-settings-template.html', '/' + folder + '/plugins/' + folder + '/src/views/settings.html')
    copyInitFile('default-style.css', '/' + folder + '/plugins/' + folder + '/src/styles/main.css')

    print('Done.')
