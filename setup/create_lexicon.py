import os.path as path
import pandas as pd
import json


def create_base_dict():
    lexicon = {}
    lex = pd.read_csv(path.join(path.dirname(__file__),'systems.csv'))
    for line in lex.itertuples():
        system_id = line[4]
        location = line[3]
        url = line[6]
        lexicon[system_id] = {'location':location, 'api_end':url}
    
    with open('system_lex.json', 'w') as write_file:
        json.dump(lexicon,write_file,indent=4)
    print('Created Base Dict')

def get_all_endpoints():
    return
    
if __name__ == '__main__':
    create_base_dict()