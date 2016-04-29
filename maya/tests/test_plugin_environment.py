from maya.plugin_environment import PluginEnvironment
import collections
import json


def d(s):
    return json.loads(s, object_pairs_hook=collections.OrderedDict)


def test_plugin_context_default_values():
    dev_env = d("""{
        "access_token": "devToken",
        "plugins": {
            "some-plugin": {
                "id": 123,
                "namespace": "someNamespace"
            }
        }
    }""")
    data = {
        'environments': {
            'dev': dev_env
        }
    }
    environment = PluginEnvironment(data)
    plugin_context = environment.get_plugin_context('some-plugin')
    assert plugin_context['plugin']['id'] == 123
    assert plugin_context['plugin']['route'] is None
    assert plugin_context['plugin']['services'] == []
    assert plugin_context['api']['access_token'] == 'devToken'
    assert plugin_context['api']['endpoint'] == 'api.zenginehq.com'
    assert plugin_context['api']['endpoint'] == 'api.zenginehq.com'


def test_plugin_context_no_env_uses_default():
    dev_env = d("""{
        "access_token": "devToken",
        "api_endpoint": "some.endpoint",
        "plugins": {
            "some-plugin": {
                "id": 123,
                "namespace": "someNamespace",
                "route": "/some-route"
            }
        },
        "default": true
    }""")
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


def test_plugin_with_services():
    dev_env = d("""{
        "access_token": "devToken",
        "api_endpoint": "some.endpoint",
        "plugins": {
            "some-plugin": {
                "id": 123,
                "namespace": "someNamespace",
                "services": {
                    "service1": {
                        "id": 50
                    },
                    "service2": {
                        "id": 64
                    }
                }
            }
        }
    }""")
    data = {
        'environments': {
            'dev': dev_env
        }
    }
    environment = PluginEnvironment(data)
    plugin_context = environment.get_plugin_context('some-plugin')
    assert plugin_context['plugin']['services'] == [
        {
            'id': 50,
            'name': 'service1'
        },
        {
            'id': 64,
            'name': 'service2'
        }
    ]
    assert plugin_context['api']['endpoint'] == 'some.endpoint'
    assert plugin_context['api']['access_token'] == 'devToken'
