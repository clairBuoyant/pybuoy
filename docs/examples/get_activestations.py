from pybuoy import Buoy

buoy = Buoy()

active_stations = buoy.stations.get_active()

print(f"NDBC Active Stations: \n----\n{active_stations}\n----\n")

"""Sample Output of active_stations.

First row (i.e., active_stations[0]) returns this object:

    {
        'id': '00922',
        'lat': '30',
        'lon': '-90',
        'name': 'OTN201 - 4800922',
        'owner': 'Dalhousie University',
        'pgm': 'IOOS Partners',
        'type': 'other',
        'met': 'n',
        'currents': 'n',
        'waterquality': 'n',
        'dart': 'n'
    }
"""
