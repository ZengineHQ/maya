from zn_api import ZnApi


def update_plugin(context, data):
    api = ZnApi(context)
    endpoint = assemble_plugin_endpoint(context)
    request = {
        'method': 'put',
        'endpoint': endpoint,
        'data': data
    }
    return api.execute_request(request)


def assemble_plugin_endpoint(context):
    return "/plugins/{0}".format(context['plugin_id'])
