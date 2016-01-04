import os
from shutil import copyfile
from subprocess import Popen


class ServiceBuilder:

    def __init__(self, service_name):
        self.service_path = 'backend/' + service_name
        self.build_path = self.service_path + '/dist'

    def build(self):
        self.make_path(self.build_path)
        self.copy_files_to_build_folder()
        self.exec_npm_install()
        self.zip_build_folder()

    def make_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def copy_files_to_build_folder(self):
        folders_to_copy = ['_runner', 'lib', 'src']
        files_to_copy = ['package.json', 'plugin.js']

        for folder_name in folders_to_copy:
            self.copy_folder(folder_name)

        for file_name in files_to_copy:
            self.copy_file(file_name)

    def copy_folder(self, folder):
        src_path = self.service_path + '/' + folder + '/'
        dst_path = self.build_path + '/' + folder + '/'
        p = Popen(['cp', '-a', src_path, dst_path])
        p.wait()

    def copy_file(self, file_name):
        src_path = self.service_path + '/' + file_name
        dst_path = self.build_path + '/' + file_name
        copyfile(src_path, dst_path)

    def exec_npm_install(self):
        p = Popen(['npm', 'install', '--production'], cwd=self.build_path)
        p.wait()

    def zip_build_folder(self):
        p = Popen(['ditto', '-c', '-k', '--sequesterRsrc', '--keepParent', 'dist', 'dist.zip'], cwd=self.service_path)
        p.wait()


def service_build(context):
    service_name = context['service']['name']
    return ServiceBuilder(service_name).build()
