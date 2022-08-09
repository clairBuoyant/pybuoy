from pybuoy.api.base import ApiBase
from pybuoy.const import ACTIVE_STATIONS, API_PATH


class Stations(ApiBase):
    def get_active(self):
        default_dataset = "xml"
        url = f"{API_PATH[ACTIVE_STATIONS]}.{default_dataset}"
        return self._clean_activestation_data(self.make_request(url))
