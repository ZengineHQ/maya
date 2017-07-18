import os
from distutils.dir_util import copy_tree
from shutil import make_archive
from shutil import copyfile
from subprocess import Popen, call, PIPE
from maya.wg_util import service_context_message_simple


class ServiceBuilder:
    def __init__(self, service_name, environment_name):
        self.service_path = 'backend/' + service_name
        self.build_path = self.service_path + '/dist'
        self.dist_file_name = 'dist.zip'
        self.environment_name = environment_name

    def build(self):
        self.make_path(self.build_path)
        self.copy_files_to_build_folder()
        self.exec_npm_install()
        self.exec_npm_maya_post_build_script()
        self.zip_build_folder()

    def make_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def copy_files_to_build_folder(self):
        folders_to_copy = ['_runner', 'lib']
        files_to_copy = ['package.json', 'plugin.js']

        for folder_name in folders_to_copy:
            self.copy_folder(folder_name)

        self.copy_folder('src', optional=True)

        for file_name in files_to_copy:
            self.copy_file(file_name)

        self.copy_patched_requestify_lib()

    def copy_patched_requestify_lib(self):
        # The 'requestify' lib bundled in the original plugin zip
        #  was changed by the Zengine Team
        # Therefore it cannot be downloaded via npm install
        # Let's copy it instead
        self.make_path(self.build_path + '/node_modules/requestify')
        self.copy_folder('node_modules/requestify')

    def copy_folder(self, folder, optional=False):
        src_path = self.service_path + '/' + folder
        dst_path = self.build_path + '/' + folder
        if optional and not os.path.exists(src_path):
            return
        copy_tree(src_path, dst_path)

    def copy_file(self, file_name):
        src_path = self.service_path + '/' + file_name
        dst_path = self.build_path + '/' + file_name
        copyfile(src_path, dst_path)

    def exec_npm_install(self):
        p = Popen(['npm', 'install', '--production'], cwd=self.build_path)
        p.wait()

    def exec_npm_maya_post_build_script(self):
        script_name = 'maya-build'

        script_exists = self.check_npm_script_exists(script_name)
        if not script_exists:
            return

        os.environ['MAYA_ENV'] = self.environment_name
        p = Popen(['npm', 'run', script_name], cwd=self.service_path)
        p.wait()

    def check_npm_script_exists(self, script_name):
        # npm run-script | grep $script_name
        p_script_list = Popen(
            ['npm', 'run-script'],
            cwd=self.service_path,
            stdout=PIPE
        )
        p_script_list.wait()
        exit_status = call(
            ('grep', script_name),
            cwd=self.service_path,
            stdin=p_script_list.stdout,
            stdout=open(os.devnull, 'wb')
        )
        return exit_status == 0

    def zip_build_folder(self):
        zip_folder = self.build_path
        zip_file_path = self.service_path + '/dist'
        make_archive(zip_file_path, 'zip', zip_folder)

    def get_dist_file_path(self):
        return self.service_path + '/' + self.dist_file_name


def b_build(context, args):
    if 'services' not in context['plugin']:
        return build_one_service(context, args)
    services = context['plugin'].pop('services')
    for service in services:
        context['service'] = service
        build_one_service(context, args)


def build_one_service(context, args):
    print service_context_message_simple("Building", context)
    instantiate(context).build()
    print "Done"


def get_dist_file_path(context):
    return instantiate(context).get_dist_file_path()


def instantiate(context):
    service_name = context['service']['name']
    environment_name = context['env']
    return ServiceBuilder(service_name, environment_name)
