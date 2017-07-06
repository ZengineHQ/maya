import os
import json
from shutil import copyfile

def init(context, args):
	folder = args['<plugin>']
	if os.path.exists(folder):
		print('Error: Already Exists!')
		return
	os.makedirs(folder)
	os.makedirs(folder + '/plugins')
	os.makedirs(folder + '/backend')
	os.makedirs(folder + '/plugins/' + folder)
	os.makedirs(folder + '/plugins/' + folder + '/src')
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
	      "plugins": 
	        plugin
	      ,
	      "default": "true"
	    }
	  }
	}

	dname = os.getcwd() + '/' + folder
	maya = open(dname + '/maya.json','w')
	json.dump(defaultJSON, maya, indent=2)
	maya.close()

	absPath = os.path.dirname(os.path.realpath(__file__))
	registration = absPath + '/default-plugin-register.js'
	destination = os.getcwd() + '/' + folder + '/plugins/' + folder + '/plugin-register.js'
	copyfile(registration, destination)
	

	print('Done.')


