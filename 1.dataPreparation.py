import pandas as pd

def assign_landmark_weight(type):
    if type in ["market", "shopping"]:
        return 5
    elif type in ["temple", "landmark", "spa", "zoo", "waterfall"]:
        return 4
    elif type in ["restaurant", "coffee shop", "bar"]:
        return 3

def assign_time_duration(type):
    if type in ["market", "shopping", "zoo"]:
        return 2
    elif type in ["coffee shop", "restaurant", "bar", "waterfall"]:
        return 1
    elif type in ["temple", "landmark", "spa"]:
        return 0.5

def convert_time_to_number(t):
    return t.split(':')[0]

place_info = pd.read_csv('../data/poidata.csv', names=['place','type','lat','long','open','close','besttime'], 
                    header=None, delimiter='\t')
place_info['rating'] = place_info['type'].apply(assign_landmark_weight)
place_info['duration'] = place_info['type'].apply(assign_time_duration)
place_info.to_csv('../data/places_raw.csv')
# covert time value to float format
place_info['close'] = place_info['close'].replace('0:00', '24:00')
place_info['close'] = place_info['close'].apply(convert_time_to_number)
place_info['open'] = place_info['open'].apply(convert_time_to_number)
place_info['besttime'] = place_info['besttime'].apply(convert_time_to_number)
print(place_info.head())
place_info.to_csv('output/places.csv')