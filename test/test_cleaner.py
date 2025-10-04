import pytest
from mobility.backend.data_agent import Cleaner
import datetime
import hashlib

@pytest.fixture()
def create_cleaner():
    def _create_cleaner(dummy_data):
        return Cleaner("task", dummy_data)
    return _create_cleaner

@pytest.fixture()
def dummy_data():
    data = {
        "system_information":{
            "last_updated":1759598961,
            "ttl":0,
            "version":"2.2",
            "data":
                {"stations":
                    [
                        {
                            "station_id":"seattle",
                            "name":"Seattle",
                            "lat":47.6137,
                            "lon":-122.3395
                        }
                    ]
                }
        },
        "source":"https://data.lime.bike/api/partners/v2/gbfs/seattle/gbfs.json"
    }
    return data

def test_epoch_clean(create_cleaner,dummy_data):
    a = create_cleaner(dummy_data)
    epoch = 825022642
    time = a.clean_epoch(epoch)
    assert time == datetime.datetime(1996,2,22,12,57,22)

def test_sha_hashing():
    test_url = "https://data.lime.bike/api/partners/v2/gbfs/seattle/gbfs.json".encode('utf-8')
    hasher = hashlib.sha256()
    hasher.update(test_url)
    assert hasher.hexdigest() == '5c89bc4ad2bcffecfecccbd9c99244e1dac6ba30fbe635dfd9cfa82105787cf8'

def test_cleaner_create(create_cleaner,dummy_data):
    a = create_cleaner(dummy_data)
    assert a
    assert a.owning_id == '5c89bc4ad2bcffecfecccbd9c99244e1dac6ba30fbe635dfd9cfa82105787cf8'
    




