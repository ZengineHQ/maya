import os, fnmatch
from wg_config import source_path
from wg_config import build_path

class PluginCanonicalCodeBuilder:

	def __init__(self, source_path, build_path):
		self.source_path = source_path
		self.build_path = build_path

	def build(self, context):
		self.plugin_name = context['plugin_name']

		self.create_build_files()

	def create_build_files(self):

		self.plugin_build_path = self.build_path + "/" + self.plugin_name

		self.create_plugin_build_path()

		self.create_individual_js_html_css_files()

	def create_plugin_build_path(self):
		if not os.path.exists(self.plugin_build_path):
			os.makedirs(self.plugin_build_path)

	def create_individual_js_html_css_files(self):
		self.merge_files_into_one("js")
		self.merge_files_into_one("html")
		self.merge_files_into_one("css")

	def merge_files_into_one(self, extension):
		target_file_name = "plugin." + extension

		target_file_path = self.plugin_build_path + "/" + target_file_name

		plugin_path = self.source_path + "/" + self.plugin_name
		plugin_dependencies_file = plugin_path + "/dependencies"
		dependencies_path = self.source_path + "/common"

		open(target_file_path, 'w').close()

		self.echo_content_of_all_files_with_extension(plugin_path, extension, target_file_path)

		with open(plugin_dependencies_file) as f:
			dependencies = f.read().splitlines()
			for dependency in dependencies:
				dependency_path = dependencies_path + "/" + dependency
				self.echo_content_of_all_files_with_extension(dependency_path, extension, target_file_path)

		if extension == "js":
			f = open(target_file_path, 'a')
			plugin_register_file = open(plugin_path + "/plugin-register.js")
			f.write(plugin_register_file.read())

	def echo_content_of_all_files_with_extension(self, dependency_path, extension, target_file_path):
		path = dependency_path + "/src"

		dependency_files_with_extension = []

		for root, dirnames, filenames in os.walk(path):
			for filename in fnmatch.filter(filenames, '*.' + extension):
				dependency_files_with_extension.append(os.path.join(root, filename))

		if dependency_files_with_extension:
			with open(target_file_path, 'a') as target_file:
				for dependency_file_name in dependency_files_with_extension:
					with open(dependency_file_name) as dependency_file:
						for line in dependency_file:
							target_file.write(line)
						target_file.write('\n')

def make_canonical_builder():
	return PluginCanonicalCodeBuilder(source_path, build_path)
