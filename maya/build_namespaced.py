import re, os
from collections import OrderedDict
from tempfile import mkstemp
from os import remove, close
from shutil import move, copyfile
from wg_config import build_path
from wg_config import namespaced_build_path

class PluginNamespacedCodeBuilder:
	def __init__(self, canonical_build_path, namespaced_build_path):
		self.canonical_build_path = canonical_build_path
		self.namespaced_build_path = namespaced_build_path

	def build(self, context):
		self.create_namespaced_build_path(context)
		self.resolve_namespace(context)
		self.resolve_route(context)

	def create_namespaced_build_path(self, context):
		path = self.get_namespaced_build_path(context)

		if not os.path.exists(path):
			os.makedirs(path)

	def resolve_namespace(self, context):

		target_namespace = context['namespace']
		target_dashed_namespace = self.camel_to_dashed(target_namespace)

		replacements = OrderedDict()
		replacements['wgn-'] = target_dashed_namespace + '-'
		replacements['wgn'] = target_namespace

		self.build_namespaced_file(context, replacements, 'js')
		self.build_namespaced_file(context, replacements, 'html')
		self.copy_css_file(context)

	def camel_to_dashed(self, namespace):
		s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', namespace)
		return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

	def build_namespaced_file(self, context, replacements, extension):

		canonical_file_path = self.get_canonical_plugin_file_path(context, extension)
		namespaced_file_path = self.get_namespaced_plugin_file_path(context, extension)

		canonical_file = open(canonical_file_path)
		namespaced_file = open(namespaced_file_path, 'w')

		for line in canonical_file:
			for src, target in replacements.iteritems():
				line = line.replace(src, target)
			namespaced_file.write(line)
		canonical_file.close()
		namespaced_file.close()

	def copy_css_file(self, context):
		canonical_file_path = self.get_canonical_plugin_file_path(context, 'css')
		namespaced_file_path = self.get_namespaced_plugin_file_path(context, 'css')

		copyfile(canonical_file_path, namespaced_file_path)

	def resolve_route(self, context):
		javascript_file_path = self.get_namespaced_plugin_file_path(context, 'js')

		self.replace(javascript_file_path, '{replace-route}', context['route'])

	def replace(self, file_path, pattern, subst):
		fh, abs_path = mkstemp()

		with open(abs_path,'w') as new_file:
			with open(file_path) as old_file:
				for line in old_file:
					new_file.write(line.replace(pattern, subst))
		close(fh)

		remove(file_path)
		move(abs_path, file_path)

	def contents_of_file(self, context, extension):
		plugin_file_path = self.get_namespaced_plugin_file_path(context, extension)

		file = open(plugin_file_path, 'r')

		return file.read()

	def get_canonical_plugin_file_path(self, context, extension):
		return self.canonical_build_path + '/' + self.get_plugin_file_path(context, extension)

	def get_namespaced_plugin_file_path(self, context, extension):
		return self.namespaced_build_path + '/' + self.get_plugin_file_path(context, extension)

	def get_plugin_file_path(self, context, extension):
		return context['plugin_name'] + '/plugin.' + extension

	def get_namespaced_build_path(self, context):
		return self.namespaced_build_path + '/' + context['plugin_name']

def make_namespaced_builder():
	return PluginNamespacedCodeBuilder(build_path, namespaced_build_path)
