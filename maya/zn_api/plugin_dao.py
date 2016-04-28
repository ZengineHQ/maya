from zn_api import ZnApi


class PluginDao:
    def __init__(self, api):
        self.api = api

    def update(self, data):
        plugin_id = data.pop('id')
        endpoint = self.assemble_plugin_endpoint(plugin_id)
        request = {
            'method': 'put',
            'endpoint': endpoint,
            'data': data
        }
        return self.api.execute_request(request)

    def assemble_plugin_endpoint(self, plugin_id):
        return "/plugins/{0}".format(plugin_id)


def update_plugin(context, request):
    plugin_api = PluginDao(ZnApi(context['api']))
    request['id'] = context['plugin']['id']
    return plugin_api.update(request)
