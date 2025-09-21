import json
from data_getters import get_data

def get_json_version(uri):
    return get_data(uri)['version']

uri = "https://gbfs.api.ridedott.com/public/v2/dubai-hills/gbfs.json"
print(get_json_version(uri))

