from maya.tests.util.fs_fake import FakeFileSystem
from maya.frontend.frontend_dependency_resolve import FrontendDependencyResolve


def test_scan_empty_deps():
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
