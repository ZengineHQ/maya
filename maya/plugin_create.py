import os
from shutil import copyfile
from .wg_util import convertToDashCase

def copyInitFile(source, dest):
    absPath = os.path.dirname(os.path.realpath(__file__))
    registration = absPath + '/default_files/' + source
    destination = os.getcwd() + dest
    copyfile(registration, destination)

def create_frontend_plugin(folder, init = False):
    dashFolder = convertToDashCase(folder)

    baseFolder = 'plugins/' + dashFolder
    if init:
        baseFolder = dashFolder + '/' + baseFolder

    os.makedirs(baseFolder + '/src/controllers')
    os.makedirs(baseFolder + '/src/styles')
    os.makedirs(baseFolder + '/src/views')

    copyInitFile('default-plugin-register.js', '/' + baseFolder + '/plugin-register.js')
    copyInitFile('default-controller.js', '/' + baseFolder + '/src/controllers/controller.js')
    copyInitFile('default-settings-controller.js', '/' + baseFolder + '/src/controllers/settings-controller.js')
    copyInitFile('default-template.html', '/' + baseFolder + '/src/views/main.html')
    copyInitFile('default-settings-template.html', '/' + baseFolder + '/src/views/settings.html')
    copyInitFile('default-style.css', '/' + baseFolder + '/src/styles/main.css')

def add_frontend_plugin_to_config(config, folder):
    dashFolder = convertToDashCase(folder)

    config['environments']['stage']['plugins'][dashFolder] = {
        "id": "DEFINE AS NUMBER",
        "namespace": folder,
        "route": "/" + dashFolder,
        #"services": {
        #    "some-plugin1-service": {
        #        "id": "DEFINE AS NUMBER"
        #    }
        #}
    }

    return config
