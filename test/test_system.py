from mobility.backend.data_agent import System
import pytest

source = {"lime_seattle":"https://data.lime.bike/api/partners/v2/gbfs/seattle/gbfs.json"}

@pytest.fixture()
def create_agent():
    def _create_system(source = {"lime_seattle":"https://data.lime.bike/api/partners/v2/gbfs/seattle/gbfs.json"}):
        return System([i for i in source.keys()][0], source[[i for i in source.keys()][0]])
    
    return _create_system


def test_agent_creation(create_agent: System):
    a = create_agent()
    assert a
    assert a.name == "lime_seattle"
    assert a.version == '2.2'
    assert a.endpoints['free_bike_status']

def test_custom_agent_creation(create_agent):
    a = create_agent({"test": "https://maas.zeus.cooltra.com/gbfs/brussels/3.0/en/gbfs.json"})
    assert a.name == "test"

def test_get_version():
    data = {"1.0":"hamilton.socialbicycles.com/opendata/gbfs.json",
            "2.0": "https://mds.neuron-mobility.com/yxe/gbfs/2/",
            "2.2": "https://data.lime.bike/api/partners/v2/gbfs/antwerp/gbfs.json",
            "2.3": "https://gbfs.api.ridedott.com/public/v2/ghent/gbfs.json",
            "3.0": "https://maas.zeus.cooltra.com/gbfs/brussels/3.0/en/gbfs.json"
            }
    for ver in data.keys():
        a = System("dummy",data[ver])
        assert a.version == ver

def test_find_feeds(create_agent: System):
    j = {"last_updated":1759261745,"ttl":0,"version":"2.2","data":{"en":{"feeds":[{"name":"system_information","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/system_information"},{"name":"station_information","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/station_information"},{"name":"station_status","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/station_status"},{"name":"free_bike_status","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/free_bike_status"},{"name":"vehicle_types","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/vehicle_types"}]}}}
    
    a = create_agent()
    endpoints = a.find_feeds(j)
    assert endpoints == [{"name":"system_information","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/system_information"},{"name":"station_information","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/station_information"},{"name":"station_status","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/station_status"},{"name":"free_bike_status","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/free_bike_status"},{"name":"vehicle_types","url":"https://data.lime.bike/api/partners/v2/gbfs/seattle/vehicle_types"}]


def test_agent_pull_from_source(create_agent):
    tasks = ["system_information", "station_information","station_status","free_bike_status","vehicle_types"]
    a = create_agent()
    for task in tasks:
        assert a.pull_from_source(task)

def test_compile_and_push_to_cleaner(create_agent):
    a = create_agent()
    data = a.run_all_tasks()
    assert len(data.keys()) > 0

def test_overall_data_grab(create_agent: System):
    a = create_agent()

    data = a.run_all_tasks()
    assert data["free_bike_status"]
    assert data["vehicle_types"]["data"] == {"vehicle_types":[{"vehicle_type_id":"1","form_factor":"scooter","propulsion_type":"electric","max_range_meters":24140},{"vehicle_type_id":"2","form_factor":"scooter","propulsion_type":"electric","max_range_meters":40233},{"vehicle_type_id":"3","form_factor":"bicycle","propulsion_type":"electric_assist","max_range_meters":85000},{"vehicle_type_id":"4","form_factor":"bicycle","propulsion_type":"human"}]}


def test_targeted_data_grab(create_agent):
    a = create_agent()
    task = "vehicle_types"
    data = a.pull_from_source(task)
    assert data["data"] == {"vehicle_types":[{"vehicle_type_id":"1","form_factor":"scooter","propulsion_type":"electric","max_range_meters":24140},{"vehicle_type_id":"2","form_factor":"scooter","propulsion_type":"electric","max_range_meters":40233},{"vehicle_type_id":"3","form_factor":"bicycle","propulsion_type":"electric_assist","max_range_meters":85000},{"vehicle_type_id":"4","form_factor":"bicycle","propulsion_type":"human"}]}

