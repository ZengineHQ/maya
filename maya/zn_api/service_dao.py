from zn_api import ZnApi


class ServiceDao:
    def __init__(self, api):
        self.api = api

    def upload(self, request):
        service_id = request.pop('id', None)
        plugin_id = request.pop('plugin_id', None)
        endpoint = self.assemble_service_endpoint(plugin_id, service_id) + '/uploads'
        request = {
            'endpoint': endpoint,
            'data': request
        }
        return self.api.upload_file(request)

    def assemble_service_endpoint(self, plugin_id, service_id):
        return "/plugins/{0}/services/{1}".format(plugin_id, service_id)


def upload_service(context, files):
    service_api = ServiceDao(ZnApi(context))
    return service_api.upload({
        'plugin_id': context['plugin_id'],
        'id': context['service']['id'],
        'files': files
    })
