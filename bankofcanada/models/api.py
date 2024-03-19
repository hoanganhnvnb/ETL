import requests

from .base import BaseModelExtract, BaseModelLoad

class ExtractModelApi(BaseModelExtract):
    def __init__(self):
        pass

    def __str__(self):
        return 'API ' + super().__str__()

    def request_data(self, config):
        if not isinstance(config, dict):
            print("Not extract data from API")
            return None
        url = config.get('url', '')
        cursor = config.get('cursor', '')
        data = requests.get(url + cursor)
        return data.text


class LoadModelApi(BaseModelLoad):
    def __init__(self):
        pass

    def __str__(self):
        return 'API ' + super().__str__()
