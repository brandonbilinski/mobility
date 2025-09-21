from requests import request

def get_data(uri:str) -> dict:
    return request('GET', uri).json()
