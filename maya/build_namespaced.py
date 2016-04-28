import os
import re
from collections import OrderedDict
from tempfile import mkstemp
from os import remove, close
from shutil import move, copyfile
from wg_config import canonical_build_path
from wg_config import namespaced_build_path


class PluginNamespacedCodeBuilder:
    def __init__(self, canonical_build_path, namespaced_build_path):
        self.canonical_build_path = canonical_build_path
        self.namespaced_build_path = namespaced_build_path

    def build(self, plugin_name, namespace, route):
        self.plugin_name = plugin_name
        self.namespace = namespace
        self.route = route
        self.create_namespaced_build_path()
        self.resolve_namespace()
        self.resolve_route()

    def create_namespaced_build_path(self):
        path = self.get_namespaced_build_path()
        if not os.path.exists(path):
            os.makedirs(path)

    def resolve_namespace(self):
        replacements = OrderedDict()
        replacements['wgn-'] = camel_to_dashed(self.namespace) + '-'
        replacements['wgn'] = self.namespace
        self.build_namespaced_file(replacements, 'js')
        self.build_namespaced_file(replacements, 'html')
        self.copy_css_file()

    def build_namespaced_file(self, replacements, extension):
        canonical_file_path = self.get_canonical_plugin_file_path(extension)
        namespaced_file_path = self.get_namespaced_plugin_file_path(extension)
        canonical_file = open(canonical_file_path)
        namespaced_file = open(namespaced_file_path, 'w')
        for line in canonical_file:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            namespaced_file.write(line)
        canonical_file.close()
        namespaced_file.close()

    def copy_css_file(self):
        canonical_file_path = self.get_canonical_plugin_file_path('css')
        namespaced_file_path = self.get_namespaced_plugin_file_path('css')
        copyfile(canonical_file_path, namespaced_file_path)

    def resolve_route(self):
        if not self.route:
            return
        javascript_file_path = self.get_namespaced_plugin_file_path('js')
        self.replace(javascript_file_path, '{replace-route}', self.route)

    def replace(self, file_path, pattern, subst):
        fh, abs_path = mkstemp()
        with open(abs_path, 'w') as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    new_file.write(line.replace(pattern, subst))
        close(fh)
        remove(file_path)
        move(abs_path, file_path)

    def contents_of_file(self, plugin_name, extension):
        self.plugin_name = plugin_name
        plugin_file_path = self.get_namespaced_plugin_file_path(extension)
        file = open(plugin_file_path, 'r')
        return file.read()

    def get_canonical_plugin_file_path(self, extension):
        return self.canonical_build_path + '/' + self.get_plugin_file_path(extension)

    def get_namespaced_plugin_file_path(self, extension):
        return self.namespaced_build_path + '/' + self.get_plugin_file_path(extension)

    def get_plugin_file_path(self, extension):
        return self.plugin_name + '/plugin.' + extension

    def get_namespaced_build_path(self):
        return self.namespaced_build_path + '/' + self.plugin_name


def camel_to_dashed(namespace):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', namespace)
    return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()


def make_namespaced_builder():
    return PluginNamespacedCodeBuilder(canonical_build_path, namespaced_build_path)
