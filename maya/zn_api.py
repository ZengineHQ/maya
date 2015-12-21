import requests
from requests.exceptions import RequestException
from requests.exceptions import HTTPError
from .exception import MayaException


def update_plugin(context, data):
    endpoint = assemble_plugin_endpoint(context)
    headers = assemble_headers(context)

    return execute_request(requests.put, endpoint, data, headers)


def assemble_plugin_endpoint(context):
    return "https://{0}/v1/plugins/{1}".format(context['api_endpoint'], context['plugin_id'])


def assemble_headers(context):
    return {'Authorization': 'Bearer ' + context['access_token']}


def execute_request(action, endpoint, data, headers):

    response = execute_http_request(action, endpoint, data, headers)

    assert_request_was_successful(response)

    return response


def execute_http_request(action, endpoint, data, headers):
    try:
        return action(endpoint, data=data, headers=headers)

    except RequestException as e:
        raise MayaException(error_message_prefix + str(e))


def assert_request_was_successful(response):
    try:
        response.raise_for_status()
    except HTTPError:
        raise MayaException(error_message_prefix + response.content)

error_message_prefix = 'Error when calling Zengine API: '
