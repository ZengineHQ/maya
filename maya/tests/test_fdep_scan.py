import json
from maya.tests.util.fs_fake import FakeFileSystem
from maya.frontend.frontend_dependency_resolve import FrontendDependencyResolve


def test_scan_no_deps():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')
    dep_scanner = FrontendDependencyResolve(fs, 'plugins')
    deps = dep_scanner.resolve('portals')
    assert deps == []


def test_scan_local_deps():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')
    deplist = "fileupload\nunderscore\n"
    fs.create_file('plugins/portals/dependencies', deplist)
    dep_scanner = FrontendDependencyResolve(fs, 'plugins')
    deps = dep_scanner.resolve('portals')
    assert deps == [
        'plugins/common/fileupload',
        'plugins/common/underscore'
    ]


def test_scan_when_package_json_with_external_deps():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')
    package = {
        'dependencies': {
            'fileupload': '/some/url',
            'underscore': '/other/url'
        }
    }
    fs.create_file('plugins/portals/package.json', json.dumps(package))
    dep_scanner = FrontendDependencyResolve(fs, 'plugins')
    deps = dep_scanner.resolve('portals')
    assert deps == [
        'plugins/portals/node_modules/fileupload',
        'plugins/portals/node_modules/underscore'
    ]


def test_scan_when_package_json_without_external_deps():
    fs = FakeFileSystem()
    fs.create_dir('plugins/portals')
    package = {
        'name': 'portal'
    }
    fs.create_file('plugins/portals/package.json', json.dumps(package))
    dep_scanner = FrontendDependencyResolve(fs, 'plugins')
    deps = dep_scanner.resolve('portals')
    assert deps == []


def test_scan_ext_deps_come_before_local():
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

    dep_scanner = FrontendDependencyResolve(fs, 'plugins')
    deps = dep_scanner.resolve('portals')
    assert deps == [
        'plugins/portals/node_modules/fileupload',
        'plugins/portals/node_modules/underscore',
        'plugins/common/fileupload',
        'plugins/common/underscore'
    ]
