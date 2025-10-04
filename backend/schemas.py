from pydantic import BaseModel

class vehicle_status_history(BaseModel):
    owning_system: int
    bike_id: str
    lat: float
    lon: float
    current_range: float
    vehicle_type_id: int
    last_reported: int

class vehicle_id_to_desc(BaseModel):
    owning_system: int
    id: int
    form: str
    propulsion_system: str
    max_range: float

class owning_system(BaseModel):
    id: str
    api_version: float
    system_id: str
    name: str
    timezone: str

class station(BaseModel):
    owning_system: int
    station_id: str
    station_name: str
    lat: float
    lon: float

class station_status(BaseModel):
    owning_system: int
    station_id: str
    num_veh_avail: int
    docks_avail: int
    last_reported: int

