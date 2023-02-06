import requests
from rest_framework import status

from utils.Strings import NO_RESPONSE


class ExternalApi:

    url = None
    data = {}
    headers = {}
    body = None

    def __init__(self, **params):
        self.url = params.get('url')
        self.data = params.get('data', {})
        self.headers = params.get('headers', {})
        self.body = params.get("body", {})

    def post(self, **config):
        params = {"url": self.url, "headers": self.headers, **config}
        if self.body:
            params.update({"data": self.body})
        else:
            params.update({"json": self.data})

        response_data = requests.post(**params)

        if not hasattr(response_data, 'status_code'):
            return False, {"failure": ""}

        if response_data.status_code < status.HTTP_200_OK or response_data.status_code > status.HTTP_207_MULTI_STATUS:
            return False, {"failure": response_data.text if hasattr(response_data, 'text') else f'{response_data.status_code}, {NO_RESPONSE}'}

        response = response_data.json() if hasattr(response_data, 'text') and response_data.text else {"data": NO_RESPONSE}

        return True, response

    def get(self, **config):
        response_data = requests.get(url=self.url,
                                     params=self.data,
                                     headers=self.headers,
                                     **config)

        if not hasattr(response_data, 'status_code'):
            return False, {"failure": NO_RESPONSE}

        if response_data.status_code not in [status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_202_ACCEPTED]:
            return False, {"failure": response_data.text if hasattr(response_data, 'text') else f'{response_data.status_code}, {NO_RESPONSE}'}

        response = response_data.json()
        if not response:
            return False, {"failure": response_data.text if hasattr(response_data, 'text') else NO_RESPONSE}

        return True, response

    def delete(self, **config):
        response_data = requests.delete(url=self.url, headers=self.headers)

        if not response_data:
            return None

        if response_data.status_code != status.HTTP_200_OK:
            return None

        return True