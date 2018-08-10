import pandas as pd

def replace_cafe(text):
    if text.split()[-1] == "caf":
        return text.replace("caf", "cafe")
    else:
        return text

pathList = pd.read_csv("input/4_pathList.csv", encoding = "ISO-8859-1")

### Python 2
#pathList['origin'] = pathList['origin'].apply(lambda x: unicode(x, errors='ignore'))

### Python 3
pathList['origin'] = pathList['origin'].apply(lambda x: x.encode('ascii', 'ignore').decode("utf-8"))
pathList['origin'] = pathList['origin'].apply(replace_cafe)

pathList['target'] = pathList['target'].apply(lambda x: x.encode('ascii', 'ignore').decode("utf-8"))
pathList['target'] = pathList['target'].apply(replace_cafe)

print(pathList)