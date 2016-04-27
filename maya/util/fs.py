import os
import fnmatch


class FileSystem:
    def __init__(self):
        self.dirs = {}

    def create_dir(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def create_file(self, path):
        open(path, 'w').close()

    def open(self, path):
        return open(path)

    def paths_with_extension(self, path, extension):
        paths_with_extension = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.' + extension):
                paths_with_extension.append(os.path.join(root, filename))
        return paths_with_extension

    def append_files(self, src_paths, dst_file_path):
        with open(dst_file_path, 'a') as dst_file:
            for src_path in src_paths:
                with open(src_path) as src_file:
                    for line in src_file:
                        dst_file.write(line)
                    dst_file.write('\n')

    def append_file(self, src_file_path, dst_file_path):
        with open(dst_file_path, 'a') as dst_file:
            with open(src_file_path) as src_file:
                dst_file.write(src_file.read())
