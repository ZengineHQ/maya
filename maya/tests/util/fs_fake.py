class FakeFileSystem:
    def __init__(self):
        self.dirs = {}

    def create_dir(self, dir_path):
        self.dirs[dir_path] = FakeDir()

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
    def __init__(self):
        self.files = {}

    def create_file(self, filename, content):
        self.files[filename] = FakeFile(content)

    def get_file(self, filename):
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
