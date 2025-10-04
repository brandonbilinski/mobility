import requests
from pydantic import BaseModel, field_validator
import datetime
from mobility.backend.schemas import vehicle_status_history
import hashlib


class System:
    """Class used to model the data system available.
      Use this class to pull and compile all available api endpoints, keep track of version of data,
       and to pull data from endpoints and pass to cleaner to handle the next step of the process."""

    def __init__(self, name, top_level):
        self.name = name
        self.version = None
        self.endpoints = {"top_level": top_level}
        self.owning_id = self.endpoints["top_level"]
        self.tasks = []

        self.get_version()
        self.compile_endpoints()
    
    def call_api_to_json(self,uri):
        try:
            response = requests.request("GET", uri)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {uri}: {e}")
            return {}
    
    def find_feeds(self, top_data):
        if not isinstance(top_data, dict):
            return None
        elif "feeds" in top_data.keys():
            return top_data["feeds"]
        else:
            for key in top_data.keys():
                found = self.find_feeds(top_data[key])
                if found:
                    return found

    def get_version(self):
        top_data = self.call_api_to_json(self.endpoints["top_level"])

        try:
            self.version = top_data['version'] 
        except:
            self.version = "1.0"
    
    def compile_endpoints(self):
        try:
            top_data = self.call_api_to_json(self.endpoints["top_level"])
            endpoints = self.find_feeds(top_data)
            for endpoint in endpoints:
                self.endpoints[endpoint["name"]] = endpoint["url"]
                self.tasks.append(endpoint["name"])
        except Exception as e:
            print("Issue with requesting data endpoints: ", e)


    def pull_from_source(self, task) -> dict:
        if task == "free_bike_status" and self.version.startswith('3'):
            task = "vehicle_status"

        data = self.call_api_to_json(self.endpoints[task])
        data["source"] = self.owning_id
        return data
    
    def run_all_tasks(self):
        data = {}
        for task in self.tasks:
            data[task] = self.pull_from_source(task)
        data["source"] = self.owning_id
        return data
        

class Cleaner():
    """Class used to clean raw JSON data. According to its data type, fix Unix Epoch times to human dates etc."""
    def __init__(self, task, data):
        self.data = data
        self.schema = None
        self.owning_id = self.get_owning_id()
    
    def get_owning_id(self):
        hasher = hashlib.sha256()
        enc_date = self.data["source"]
        enc_date = enc_date.encode('utf-8')
        hasher.update(enc_date)
        return hasher.hexdigest()

    def discern_schema(self, task):
        if task == "free_bike_status":
            a = self.clean_to_push(vehicle_status_history)
        else:
            return
            

    def clean_epoch(self, epoch: int):
        timestamp = datetime.datetime.fromtimestamp(epoch)
        return timestamp


class Loader():
    pass