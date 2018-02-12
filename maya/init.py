import os
import json
import re
from shutil import copyfile
from .exception import MayaException

def copyInitFile(source, dest):
    absPath = os.path.dirname(os.path.realpath(__file__))
    registration = absPath + '/default_files/' + source
    destination = os.getcwd() + dest
    copyfile(registration, destination)

def convertToDashCase(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

def init(args):
    folder = args['<plugin>']
    dashFolder = convertToDashCase(folder)
    if os.path.exists(dashFolder):
        raise MayaException('Error: Already Exists!')
    os.makedirs(dashFolder)
    os.makedirs(dashFolder + '/backend')
    os.makedirs(dashFolder + '/plugins')
    os.makedirs(dashFolder + '/plugins/' + dashFolder)
    os.makedirs(dashFolder + '/plugins/' + dashFolder + '/src')
    os.makedirs(dashFolder + '/plugins/' + dashFolder + '/src/controllers')
    os.makedirs(dashFolder + '/plugins/' + dashFolder + '/src/styles')
    os.makedirs(dashFolder + '/plugins/' + dashFolder + '/src/views')
    plugin = {}
    plugin[dashFolder] = {
        "id": "DEFINE AS NUMBER",
        "namespace": folder,
        "route": "/" + dashFolder,
        #"services": {
        #    "some-plugin1-service": {
        #        "id": "DEFINE AS NUMBER"
        #    }
        #}
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

    dname = os.getcwd() + '/' + dashFolder
    maya = open(dname + '/maya.json', 'w')
    json.dump(defaultJSON, maya, indent=2)
    maya.close()

    copyInitFile('default-plugin-register.js', '/' + dashFolder + '/plugins/' + dashFolder + '/plugin-register.js')
    copyInitFile('default-controller.js', '/' + dashFolder + '/plugins/' + dashFolder + '/src/controllers/controller.js')
    copyInitFile('default-settings-controller.js', '/' + dashFolder + '/plugins/' + dashFolder + '/src/controllers/settings-controller.js')
    copyInitFile('default-template.html', '/' + dashFolder + '/plugins/' + dashFolder + '/src/views/main.html')
    copyInitFile('default-settings-template.html', '/' + dashFolder + '/plugins/' + dashFolder + '/src/views/settings.html')
    copyInitFile('default-style.css', '/' + dashFolder + '/plugins/' + dashFolder + '/src/styles/main.css')

    print('Done.')
