from .wg_config import source_path
from .wg_config import canonical_build_path
from .exception import MayaException
from .frontend.scan_path import ScanPath
from .util.fs import FileSystem


class PluginCanonicalCodeBuilder:

    def __init__(self, fs, source_path, build_path):
        self.fs = fs
        self.source_path = source_path
        self.build_path = build_path
        self.scan_path = ScanPath(fs, source_path)

    def build(self, context):
        self.plugin_name = context['plugin_name']

        self.plugin_path = self.source_path + '/' + self.plugin_name
        self.plugin_build_path = self.build_path + '/' + self.plugin_name
        self.scan_paths = self.scan_path.ls(self.plugin_name)

        self.fs.create_dir(self.plugin_build_path)
        self.merge_files_into_one('js')
        self.merge_files_into_one('html')
        self.merge_files_into_one('css')

    def merge_files_into_one(self, extension):
        target_file_path = self.create_target_file(extension)
        for scan_path in self.scan_paths:
            self.merge_all_files_with_extension(scan_path, extension, target_file_path)
        if extension == 'js':
            self.append_plugin_register(target_file_path)

    def create_target_file(self, extension):
        target_file_name = 'plugin.' + extension
        target_file_path = self.plugin_build_path + '/' + target_file_name
        self.fs.create_file(target_file_path)
        return target_file_path

    def merge_all_files_with_extension(self, module_path, extension, target_file_path):
        src_path = module_path + '/src'
        file_paths = self.fs.paths_with_extension(src_path, extension)
        if file_paths:
            self.fs.append_files(file_paths, target_file_path)

    def append_plugin_register(self, target_file_path):
        plugin_register_path = self.plugin_path + '/plugin-register.js'
        try:
            self.fs.append_file(
                plugin_register_path,
                target_file_path
            )
        except IOError:
            raise MayaException('Build error: plugin register file not found: ' + plugin_register_path)


def make_canonical_builder():
    fs = FileSystem()
    return PluginCanonicalCodeBuilder(fs, source_path, canonical_build_path)
