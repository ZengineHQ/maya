import requests

def deploy(context, request):
	endpoint = assemble_plugin_endpoint(context)
	headers = assemble_headers(context)

	return requests.put(endpoint, data=request, headers=headers)

def publish(context):
	request = {}
	request['publish'] = True

	endpoint = assemble_plugin_endpoint(context)
	headers = assemble_headers(context)

	return requests.put(endpoint, data=request, headers=headers)

def assemble_plugin_endpoint(context):
	return "https://{0}/v1/plugins/{1}".format(context['api_endpoint'], context['plugin_id'])

def assemble_headers(context):
	return {'Authorization': 'Bearer ' + context['access_token']}
