import json
from wg_config import environment_file_path

class PluginEnvironment:
	def __init__(self, environment_file_path, environment_name=None):
		self.environment_file_path = environment_file_path

		if environment_name:
			self.environment_name = environment_name
		else:
			self.environment_name = self.get_default_environment()

	def get_default_environment(self):
		environments = self.read_environments()

		for environment_name, environment in environments.iteritems():
			if environment.get('default'):
				return environment_name

		raise PluginEnvironmentException('No default environment was found')

	def get_all_plugin_contexts(self):
		data = self.get_environment_data()

		plugin_contexts = []

		for plugin_name in data['plugins'].keys():
			context = self.get_plugin_context(plugin_name)
			plugin_contexts.append(context)

		return plugin_contexts

	def get_plugin_context(self, plugin_name):
		context = {}

		env_data = self.get_environment_data()
		plugin_data = self.get_plugin(plugin_name)

		context['plugin_name'] = plugin_name
		context['plugin_id'] = plugin_data['id']
		context['namespace'] = plugin_data['namespace']
		context['route'] = plugin_data['route']
		context['api_endpoint'] = env_data['api_endpoint']
		context['access_token'] = env_data['access_token']

		return context

	def get_plugin(self, plugin_name):
		data = self.get_environment_data()

		try:
			return data['plugins'][plugin_name]
		except KeyError:
			raise PluginEnvironmentException("Plugin not found: " + plugin_name)

	def get_environment_data(self):
		json_data = self.read_environments()

		return json_data[self.environment_name]

	def read_environments(self):
		with open(self.environment_file_path) as json_file:
			json_data = json.load(json_file)
			return json_data

class PluginEnvironmentException(Exception):
	pass

def make_environment(environment_name=None):
	return PluginEnvironment(environment_file_path, environment_name)
