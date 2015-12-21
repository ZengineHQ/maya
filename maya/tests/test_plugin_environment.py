from maya.plugin_environment import PluginEnvironment


def testGetPluginContext_Defaults():

    devEnv = {
        'access_token': 'devToken',
        'plugins': {
            'some-plugin': {
                'id': 123,
                'namespace': 'someNamespace'
            }
        }
    }

    data = {
        'environments': {
            'dev': devEnv
        }
    }

    environment = PluginEnvironment(data)
    plugin_context = environment.get_plugin_context('some-plugin')

    assert plugin_context['plugin_id'] == 123
    assert plugin_context['route'] == None
    assert plugin_context['access_token'] == 'devToken'
    assert plugin_context['api_endpoint'] == 'api.zenginehq.com'


def testGetPluginContext_WhenNoEnvSpecified_and_DefaultEnvExists_ShouldPickDefault():

    devEnv = {
        'access_token': 'devToken',
        'api_endpoint': 'some.endpoint',
        'plugins': {
            'some-plugin': {
                'id': 123,
                'namespace': 'someNamespace',
                'route': '/some-route'
            }
        },
        'default': True
    }

    data = {
        'environments': {
            'dev': devEnv
        }
    }

    environment = PluginEnvironment(data)
    plugin_context = environment.get_plugin_context('some-plugin')

    assert plugin_context['plugin_id'] == 123
    assert plugin_context['plugin_name'] == 'some-plugin'
    assert plugin_context['route'] == '/some-route'
    assert plugin_context['namespace'] == 'someNamespace'
    assert plugin_context['api_endpoint'] == 'some.endpoint'
    assert plugin_context['access_token'] == 'devToken'
