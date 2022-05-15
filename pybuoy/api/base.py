import requests  # type: ignore

from pybuoy.mixins.parser import ParserMixin  # type: ignore


class ApiBase(ParserMixin):
    def make_request(self, url: str):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            print(f"Data not available for url: {url}")
            return None
        else:
            raise ValueError(f"Error code {response.status_code} for url: {url}")
