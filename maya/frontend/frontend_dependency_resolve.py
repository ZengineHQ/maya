
class FrontendDependencyResolve:

    def __init__(self, frontend_path):
        self.frontend_path = frontend_path

    def resolve(self, plugin_path):
        local_dependency_paths = self.get_local_dependency_paths(plugin_path)
        return local_dependency_paths or []

    def get_local_dependency_paths(self, plugin_path):
        plugin_dependencies_config_path = plugin_path + '/dependencies'
        dependencies_path = self.frontend_path + '/common'
        try:
            with open(plugin_dependencies_config_path) as f:
                dependency_names = f.read().splitlines()
                return [
                    dependencies_path + '/' + dependency_name
                    for dependency_name in dependency_names
                ]
        except IOError:
            pass
