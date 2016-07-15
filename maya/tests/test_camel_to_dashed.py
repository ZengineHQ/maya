from maya.frontend.build_namespaced import camel_to_dashed


def test():
    assert camel_to_dashed('myplugin') == 'myplugin'
    assert camel_to_dashed('somePluginNamespace') == 'some-plugin-namespace'
    assert camel_to_dashed('someXYZPlugin') == 'some-x-y-z-plugin'
    assert camel_to_dashed('XYZPlugin') == 'x-y-z-plugin'
