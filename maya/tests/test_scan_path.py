import json
from maya.tests.util.fs_fake import FakeFileSystem
from maya.frontend.scan_path import ScanPath


def test_ls_no_deps():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')
    scan_path = ScanPath(fs, 'plugins')
    paths = scan_path.ls('portals')
    assert paths == [
        'plugins/portals'
    ]


def test_ls_local_deps():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')
    deplist = "fileupload\nunderscore\n"
    fs.create_file('plugins/portals/dependencies', deplist)
    scan_path = ScanPath(fs, 'plugins')
    paths = scan_path.ls('portals')
    assert paths == [
        'plugins/common/fileupload',
        'plugins/common/underscore',
        'plugins/portals'
    ]


def test_ls_when_package_json_with_external_deps():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')
    package = {
        'dependencies': {
            'fileupload': '/some/url',
            'underscore': '/other/url'
        }
    }
    fs.create_file('plugins/portals/package.json', json.dumps(package))
    fs.create_dir('plugins/portals/node_modules/fileupload/src')
    fs.create_dir('plugins/portals/node_modules/underscore/src')
    scan_path = ScanPath(fs, 'plugins')
    paths = scan_path.ls('portals')
    assert paths == [
        'plugins/portals/node_modules/fileupload',
        'plugins/portals/node_modules/underscore',
        'plugins/portals'
    ]


def test_ls_when_package_json_with_external_dep_without_src_folder():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')
    package = {
        'dependencies': {
            'fileupload': '/some/url'
        }
    }
    fs.create_file('plugins/portals/package.json', json.dumps(package))
    fs.create_dir('plugins/portals/node_modules/fileupload')
    scan_path = ScanPath(fs, 'plugins')
    paths = scan_path.ls('portals')
    assert paths == [
        'plugins/portals'
    ]


def test_ls_when_package_json_without_external_deps():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')
    package = {
        'name': 'portal'
    }
    fs.create_file('plugins/portals/package.json', json.dumps(package))
    scan_path = ScanPath(fs, 'plugins')
    paths = scan_path.ls('portals')
    assert paths == [
        'plugins/portals'
    ]


def test_ls_ext_deps_come_before_local():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')

    # local deps
    deplist = "fileupload\nunderscore\n"
    fs.create_file('plugins/portals/dependencies', deplist)

    # external deps
    package = {
        'dependencies': {
            'fileupload': '/some/url',
            'underscore': '/other/url'
        }
    }
    fs.create_file('plugins/portals/package.json', json.dumps(package))
    fs.create_dir('plugins/portals/node_modules/fileupload/src')
    fs.create_dir('plugins/portals/node_modules/underscore/src')

    scan_path = ScanPath(fs, 'plugins')
    paths = scan_path.ls('portals')
    assert paths == [
        'plugins/portals/node_modules/fileupload',
        'plugins/portals/node_modules/underscore',
        'plugins/common/fileupload',
        'plugins/common/underscore',
        'plugins/portals'
    ]
