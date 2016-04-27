class FakeFileSystem:
    def __init__(self):
        self.dirs = {}

    def create_dir(self, dir_path):
        self.dirs[dir_path] = FakeDir(dir_path)

    def create_file(self, path, content):
        segments = path.split('/')
        filename = segments.pop()
        dir_path = '/'.join(segments)
        if dir_path not in self.dirs:
            raise IOError
        self.dirs[dir_path].create_file(filename, content)

    def open(self, path):
        segments = path.split('/')
        filename = segments.pop()
        dir_path = '/'.join(segments)
        if dir_path not in self.dirs:
            raise IOError
        file = self.dirs[dir_path].get_file(filename)
        return FakeFileOpen(file)


class FakeDir:
    def __init__(self, path):
        self.path = path
        self.files = {}

    def create_file(self, filename, content):
        self.files[filename] = FakeFile(content)

    def get_file(self, filename):
        if filename not in self.files:
            raise IOError(
                "File '{0}' not found in '{1}'".format(filename, self.path)
            )
        return self.files[filename]


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
