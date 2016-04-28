class FakeFileSystem:
    def __init__(self):
        self.root_dirs = {}

    def dir_exists(self, dir_path):
        try:
            self.__get_dir(dir_path)
            return True
        except IOError:
            return False

    def create_dir(self, dir_path):
        (root_segment, segments) = self.__extract_root(dir_path)
        if root_segment not in self.root_dirs:
            root_dir = FakeDir(root_segment)
            self.root_dirs[root_segment] = root_dir
        parent = self.root_dirs[root_segment]
        for segment in segments:
            parent = parent.get_or_create_dir(segment)

    def create_file(self, path, content=None):
        (dir_path, filename) = self.__parse_path(path)
        dir = self.__get_dir(dir_path)
        dir.create_file(filename, content)

    def open(self, path):
        (dir_path, filename) = self.__parse_path(path)
        dir = self.__get_dir(dir_path)
        file = dir.get_file(filename)
        return FakeFileOpen(file)

    def paths_with_extension(self, dir_path, extension):
        dir = self.__get_dir(dir_path)
        return dir.paths_with_extension(extension)

    def __parse_path(self, path):
        segments = path.split('/')
        filename = segments.pop()
        dir_path = '/'.join(segments)
        return (dir_path, filename)

    def __get_dir(self, dir_path):
        (root_segment, segments) = self.__extract_root(dir_path)
        if root_segment not in self.root_dirs:
            raise IOError(
                "Folder '{0}' does not exist".format(dir_path)
            )
        root_dir = self.root_dirs[root_segment]
        if len(segments) == 0:
            return root_dir
        dir = root_dir.get_dir(segments)
        if not dir:
            raise IOError(
                "Folder '{0}' does not exist".format(dir_path)
            )
        return dir

    def __extract_root(self, dir_path):
        segments = dir_path.split('/')
        root_segment = segments.pop(0)
        if not root_segment:
            root_segment = segments.pop(0)
        return (root_segment, segments)


class FakeDir:
    def __init__(self, name):
        self.name = name
        self.files = {}
        self.dirs = {}

    def get_or_create_dir(self, name):
        if name in self.dirs:
            return self.dirs[name]
        dir = FakeDir(name)
        self.dirs[name] = dir
        return dir

    def add_dir(self, dir):
        self.dirs.append(dir)

    def get_dir(self, segments):
        dir_name = segments.pop(0)
        dir = self.dirs.get(dir_name)
        if not dir:
            return
        if not segments:
            return dir
        return dir.get_dir(segments)

    def create_file(self, filename, content):
        self.files[filename] = FakeFile(content)

    def get_file(self, filename):
        if filename not in self.files:
            raise IOError(
                "File '{0}' not found in '{1}'".format(filename, self.name)
            )
        return self.files[filename]

    def paths_with_extension(self, extension):
        r_paths = []
        for dir in self.dirs.itervalues():
            r_paths += dir.paths_with_extension(extension)
        f_paths = [
            filename
            for filename in self.files.keys()
            if filename.endswith('.' + extension)
        ]
        paths = f_paths + r_paths
        return [
            self.name + '/' + path
            for path in paths
        ]


class FakeFile:
    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content


class FakeFileOpen:
    def __init__(self, fake_file):
        self.fake_file = fake_file

    def __enter__(self):
        return self.fake_file

    def __exit__(self, type, value, traceback):
        pass
