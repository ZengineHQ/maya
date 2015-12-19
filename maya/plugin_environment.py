import json
from .wg_config import config_file_path
from .exception import MayaException

class PluginEnvironment:
	def __init__(self, data, environment_name=None):
		self.data = data

		if environment_name:
			self.environment_name = environment_name
		else:
			self.environment_name = self.get_default_environment()

	def get_default_environment(self):
		environments = self.get_environments()

		for environment_name, environment in environments.iteritems():
			if environment.get('default'):
				return environment_name

		first_environment_name = environments.keys()[0]

		return first_environment_name

	def get_all_plugin_contexts(self):
		plugins = self.get_environment_plugins()

		plugin_contexts = []

		for plugin_name in plugins.keys():
			context = self.get_plugin_context(plugin_name)
			plugin_contexts.append(context)

		return plugin_contexts

	def get_plugin_context(self, plugin_name):

		environment = self.get_environment()
		plugin = self.get_plugin(plugin_name)

		default_api_endpoint = 'api.zenginehq.com'

		context = {
			'plugin_id': plugin['id'],
			'plugin_name': plugin_name,
			'namespace': plugin['namespace'],
			'route': plugin.get('route'),
			'api_endpoint': environment.get('api_endpoint', default_api_endpoint),
			'access_token': environment['access_token']
		}

		return context

	def get_plugin(self, plugin_name):
		plugins = self.get_environment_plugins()

		try:
			return plugins[plugin_name]
		except KeyError:
			raise MayaException("Plugin not found: " + plugin_name)

	def get_environment_plugins(self):
		environment = self.get_environment()

		return environment['plugins']

	def get_environment(self):
		environments = self.get_environments()

		try:
			return environments[self.environment_name]
		except KeyError:
			raise MayaException("Environment not found: " + self.environment_name)

	def get_environments(self):
		try:
			return self.data['environments']
		except KeyError:
			raise MayaException("Config file: \"environments\" attribute not found.")

def make_environment(environment_name=None):

	data = read_json_config_file()

	return PluginEnvironment(data, environment_name)

def read_json_config_file():
	try:
		with open(config_file_path) as json_file:
			return json.load(json_file)
	except IOError:
		raise MayaException('Config file not found: ' + config_file_path)
	except:
		raise MayaException('Config file: JSON syntax error on ' + config_file_path)
