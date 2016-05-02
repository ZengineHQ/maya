import collections
import json


class ScanPath:
    def __init__(self, fs, frontend_path):
        self.fs = fs
        self.frontend_path = frontend_path

    def ls(self, plugin):
        self.plugin_path = self.frontend_path + '/' + plugin
        dependency_paths = \
            self.get_external_dependency_paths() + \
            self.get_local_dependency_paths()
        return dependency_paths + [self.plugin_path]

    def get_local_dependency_paths(self):
        plugin_dependencies_config_path = self.plugin_path + '/dependencies'
        dependencies_path = self.frontend_path + '/common'
        try:
            with self.fs.open(plugin_dependencies_config_path) as f:
                dependency_names = f.read().splitlines()
                return [
                    dependencies_path + '/' + dependency_name
                    for dependency_name in dependency_names
                ]
        except IOError:
            return []

    def get_external_dependency_paths(self):
        package_json_path = self.plugin_path + '/package.json'
        node_modules_path = self.plugin_path + '/node_modules'
        try:
            with self.fs.open(package_json_path) as f:
                package_json = json.loads(
                    f.read(),
                    object_pairs_hook=collections.OrderedDict
                )
                if 'dependencies' not in package_json:
                    return []
                dependency_names = package_json['dependencies'].keys()
                dependency_paths = [
                    node_modules_path + '/' + dependency_name
                    for dependency_name in dependency_names
                ]
                return [
                    dependency_path
                    for dependency_path in dependency_paths
                    if self.fs.dir_exists(dependency_path + '/src')
                ]
        except IOError:
            return []
