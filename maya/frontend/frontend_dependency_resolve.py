import json


class FrontendDependencyResolve:

    def __init__(self, fs, frontend_path):
        self.fs = fs
        self.frontend_path = frontend_path

    def resolve(self, plugin_path):
        local_dependency_paths = self.get_local_dependency_paths(plugin_path)
        external_dep_paths = self.get_ext_dep_paths(plugin_path)
        return external_dep_paths + local_dependency_paths

    def get_local_dependency_paths(self, plugin):
        plugin_dependencies_config_path = self.frontend_path + '/' + plugin + '/dependencies'
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

    def get_ext_dep_paths(self, plugin):
        package_json_path = self.frontend_path + '/' + plugin + '/package.json'
        node_modules_path = self.frontend_path + '/' + plugin + '/node_modules'
        try:
            with self.fs.open(package_json_path) as f:
                package_json = json.loads(f.read())
                if 'dependencies' not in package_json:
                    return []
                dep_names = package_json['dependencies'].keys()
                return [
                    node_modules_path + '/' + dep_name
                    for dep_name in dep_names
                ]
        except IOError:
            return []
