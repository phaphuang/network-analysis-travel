import pandas as pd
import random
import math

def replace_cafe(text):
    if text.split()[-1] == "caf":
        return text.replace("caf", "cafe")
    else:
        return text

def random_time(t):
    ### Random float number
    return round(random.uniform(0,1), 2)

def random_time_if_nan(t):
    if math.isnan(t):
        ### Random float number
        return round(random.uniform(0,1), 2)
    else:
        return t

def time_char_to_int(t):
    
    if "h" in t:
        result = round((60 * int(t.split()[0])) + (int(t.split()[2]) / 60), 2)
    else:
        result = round(int(t.split()[0]) / 60, 2)
    return result

pathList = pd.read_csv("input/4_pathList.csv", encoding = "ISO-8859-1")

### Python 2
#pathList['origin'] = pathList['origin'].apply(lambda x: unicode(x, errors='ignore'))

### Python 3
pathList['origin'] = pathList['origin'].apply(lambda x: x.encode('ascii', 'ignore').decode("utf-8"))
pathList['origin'] = pathList['origin'].apply(replace_cafe)

pathList['target'] = pathList['target'].apply(lambda x: x.encode('ascii', 'ignore').decode("utf-8"))
pathList['target'] = pathList['target'].apply(replace_cafe)

print(pathList)

### Import another dataframe
dist1 = pd.read_csv("input/3_timeDistanceList.csv")

dist2 = dist1.copy()
dist2['origin'] = dist1['target']
dist2['target'] = dist1['origin']
dist2['originId'] = dist1['targetId']
dist2['targetId'] = dist1['originId']

### Rename column name
dist1.rename(columns={'originId': 'V1', 'targetId': 'V2'}, inplace=True)
dist2.rename(columns={'originId': 'V1', 'targetId': 'V2'}, inplace=True)

pre_result1 = pd.merge(pathList, dist1[["V1","V2","time","distance"]], how="left", on=['V1','V2'])
pre_result2 = pd.merge(pathList, dist2[["V1","V2","time","distance"]], how="left", on=['V1','V2'])

### First result
raw_result = pre_result1.combine_first(pre_result2)
clean_data1 = raw_result[(~raw_result["time"].isna()) & (~raw_result["distance"].isna())]
### Convert time with string value to integer
clean_data1['time'] = clean_data1['time'].apply(time_char_to_int)
#raw_result['time'] = raw_result['time'].apply(time_char_to_int)

### Reconcile iron bridge distance data
iron_result = raw_result[(raw_result["V1"]==6) | (raw_result["V2"]==6)]
iron_data1 = iron_result[iron_result['V1'] == 6]
iron_data1['time'] = iron_data1['time'].apply(random_time)

iron_data2 = iron_data1.copy()
iron_data2['origin'] = iron_data1['target']
iron_data2['target'] = iron_data1['origin']
iron_data2['V1'] = iron_data1['V2']
iron_data2['V2'] = iron_data1['V1']
#iron_data2 = iron_result[iron_result['V2'] == 6]
#iron_data2['time'] = iron_data2['time'].apply(random_distance)

### Merge result
temp_iron1 = pd.merge(iron_result[["V1","V2","origin","target"]], iron_data1[["V1","V2","time","distance"]], how="left", on=['V1','V2'])
temp_iron2 = pd.merge(iron_result[["V1","V2","origin","target"]], iron_data2[["V1","V2","time","distance"]], how="left", on=['V1','V2'])
clean_data2 = temp_iron1.combine_first(temp_iron2)
clean_data2['time'] = clean_data2["time"].apply(lambda x: random_time_if_nan(x))

### Populate random distance value between places and starting point
nan_result = raw_result[(raw_result["time"].isna() | raw_result["distance"].isna()) & \
                        ~((raw_result["V1"] == 6) | (raw_result["V2"] == 6))]
sPoint_row1 = nan_result[(nan_result["origin"]=='sPoint')]
sPoint_row1["time"] = sPoint_row1["time"].apply(random_time)

sPoint_row2 = sPoint_row1.copy()
sPoint_row2['origin'] = sPoint_row1['target']
sPoint_row2['target'] = sPoint_row1['origin']
sPoint_row2['V1'] = sPoint_row1['V2']
sPoint_row2['V2'] = sPoint_row1['V1']

### Merge result
temp_sPoint1 = pd.merge(nan_result[["V1","V2","origin","target"]], sPoint_row1[["V1","V2","time","distance"]], how="left", on=['V1','V2'])
temp_sPoint2 = pd.merge(nan_result[["V1","V2","origin","target"]], sPoint_row2[["V1","V2","time","distance"]], how="left", on=['V1','V2'])
clean_data3 = temp_sPoint1.combine_first(temp_sPoint2)
#print(post_result.tail())
#post_result.to_csv("input/5_populatedValue.csv")

frames = [clean_data1,clean_data2,clean_data3]
result = pd.concat(frames)

### Reset index and start from 1
result.reset_index(inplace=True,drop=True)
result.index = result.index + 1

### Remove Unnamed column's name
result = result.loc[:, ~result.columns.str.contains('^Unnamed')]

final_result = result[['V1','V2','time']]
final_result.columns = ['V1','V2','weight']
final_result.to_csv("input/5_pathWithWeight.csv",index=False)