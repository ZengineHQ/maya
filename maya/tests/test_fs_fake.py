from pytest import raises
from maya.tests.util.fs_fake import FakeFileSystem


def test_open_unexisting_file_throws_error():
    fs = FakeFileSystem()
    with raises(IOError):
        fs.open('plugins/a.txt')


def test_create_dir_and_file():
    fs = FakeFileSystem()
    fs.create_dir('/plugins/portals')

    dependency_file_content = 'fileupload\nunderscore\n'
    fs.create_file('/plugins/portals/dependencies', dependency_file_content)

    with fs.open('/plugins/portals/dependencies') as f:
        dependency_names = f.read().splitlines()
        assert dependency_names[0] == 'fileupload'


def test_create_file_without_all_parent_dirs_throws_error():
    fs = FakeFileSystem()

    with raises(IOError):
        dependency_file_content = 'something'
        fs.create_file('/plugins/portals/dependencies', dependency_file_content)


def test_create_files_same_dir():
    fs = FakeFileSystem()
    fs.create_dir('test-dir')
    fs.create_file('test-dir/hi.txt', 'hi')
    fs.create_file('test-dir/hello.txt', 'hello')

    with fs.open('test-dir/hi.txt') as f:
        assert f.read() == 'hi'
    with fs.open('test-dir/hello.txt') as f:
        assert f.read() == 'hello'


def test_create_files_nested_dirs():
    fs = FakeFileSystem()
    fs.create_dir('test-dir')
    fs.create_dir('test-dir/a')
    fs.create_file('test-dir/hi.txt', 'hi')
    fs.create_file('test-dir/a/hello.txt', 'hello')

    with fs.open('test-dir/hi.txt') as f:
        assert f.read() == 'hi'
    with fs.open('test-dir/a/hello.txt') as f:
        assert f.read() == 'hello'


def test_paths_with_extension_when_flat_dir():
    fs = FakeFileSystem()
    fs.create_dir('test-dir')
    fs.create_file('test-dir/hi.txt')
    fs.create_file('test-dir/hello.js')
    fs.create_file('test-dir/hello.txt')
    fs.create_file('test-dir/something.css')
    fs.create_file('test-dir/.gitignore')

    paths = fs.paths_with_extension('test-dir', 'txt')
    assert paths == [
        'test-dir/hi.txt',
        'test-dir/hello.txt'
    ]


def test_paths_with_extension_when_nested_dirs():
    fs = FakeFileSystem()
    fs.create_dir('test-dir')
    fs.create_file('test-dir/hi.txt')
    fs.create_dir('test-dir/src')
    fs.create_file('test-dir/src/hello.js')
    fs.create_dir('test-dir/docs')
    fs.create_file('test-dir/docs/hello.txt')
    fs.create_file('test-dir/.gitignore')

    paths = fs.paths_with_extension('test-dir', 'txt')
    assert paths == [
        'test-dir/hi.txt',
        'test-dir/docs/hello.txt'
    ]
