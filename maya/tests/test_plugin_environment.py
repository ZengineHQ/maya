from maya.plugin_environment import PluginEnvironment


def test_plugin_context_default_values():
    dev_env = {
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
            'dev': dev_env
        }
    }
    environment = PluginEnvironment(data)
    plugin_context = environment.get_plugin_context('some-plugin')
    assert plugin_context['plugin']['id'] == 123
    assert plugin_context['plugin']['route'] is None
    assert plugin_context['api']['access_token'] == 'devToken'
    assert plugin_context['api']['endpoint'] == 'api.zenginehq.com'


def test_plugin_context_no_env_uses_default():
    dev_env = {
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
            'dev': dev_env
        }
    }
    environment = PluginEnvironment(data)
    plugin_context = environment.get_plugin_context('some-plugin')
    assert plugin_context['plugin']['id'] == 123
    assert plugin_context['plugin']['name'] == 'some-plugin'
    assert plugin_context['plugin']['route'] == '/some-route'
    assert plugin_context['plugin']['namespace'] == 'someNamespace'
    assert plugin_context['api']['endpoint'] == 'some.endpoint'
    assert plugin_context['api']['access_token'] == 'devToken'
