import requests
from requests.exceptions import RequestException
from requests.exceptions import HTTPError
from ..exception import MayaException


class ZnApi:

    def __init__(self, options):
        self.api_url = "https://{0}/v1".format(options['endpoint'])
        self.headers = {
            'Authorization': 'Bearer ' + options['access_token']
        }
        self.error_message_prefix = 'Error when calling Zengine API: '

    def execute_request(self, r):
        response = self.execute_http_request(r)
        self.assert_request_was_successful(response)
        return response

    def execute_http_request(self, r):
        try:
            url = self.assemble_url(r)
            action = getattr(requests, r['method'])
            return action(url, data=r['data'], headers=self.headers)
        except RequestException as e:
            raise MayaException(self.error_message_prefix + str(e))

    def upload_file(self, r):
        try:
            url = self.assemble_url(r)
            response = requests.post(url, files=r['data'], headers=self.headers)
            self.assert_request_was_successful(response)
            return response
        except RequestException as e:
            raise MayaException(self.error_message_prefix + str(e))

    def assemble_url(self, r):
        return self.api_url + r['endpoint']

    def assert_request_was_successful(self, response):
        try:
            response.raise_for_status()
        except HTTPError:
            raise MayaException(self.error_message_prefix + response.content)
