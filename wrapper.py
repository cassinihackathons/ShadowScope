import cdsapi
import yaml


class Downloader:
    def __init__(self):
        with open(".cdsapirc", 'r') as f:
            credentials = yaml.safe_load(f)
        self.client = cdsapi.Client(
            url=credentials['url'], key=credentials['key'])

    def GetData(self, latitude, longitude):
        self.client.retrieve(
            'cams-solar-radiation-timeseries',
            {
                'sky_type': 'observed_cloud',
                'location': {
                    'latitude': latitude,
                    'longitude': longitude,
                },
                'altitude': '-999.',
                'date': '2021-11-02/2022-11-02',
                'time_step': '1hour',
                'time_reference': 'true_solar_time',
                'format': 'csv',
            },
            "data/" + str(latitude) + '-' + str(longitude) + '.csv')
