from pybuoy.api.base import ApiBase
from pybuoy.const import API_PATH, Endpoints


class Stations(ApiBase):
    def get_active(self):
        default_dataset = "xml"
        url = f"{API_PATH[Endpoints.ACTIVE_STATIONS.value]}.{default_dataset}"
        return self._clean_activestation_data(self.make_request(url))
