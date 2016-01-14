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


def upload_service(context, files):
    api = ZnApi(context)
    endpoint = assemble_service_endpoint(context) + '/uploads'
    request = {
        'endpoint': endpoint,
        'data': files
    }
    return api.upload_file(request)


def assemble_plugin_endpoint(context):
    return "/plugins/{0}".format(context['plugin_id'])


def assemble_service_endpoint(context):
    return "/plugins/{0}/services/{1}".format(context['plugin_id'], context['service']['id'])
