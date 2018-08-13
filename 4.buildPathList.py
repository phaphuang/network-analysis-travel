import pandas as pd

df = pd.read_csv('input/2_convertScoreToRating.csv', index_col=0)

pathList = []

for x in df.index:
    pathList.append([0,x,'sPoint',df.loc[x,'place']])

#print(pathList)

for i in df.index:
    #print(i, " with ", df.loc[i,'long'])
    pathList.append([i,0,df.loc[i,'place'],'sPoint'])
    for j in df.index:
        if i == j:
            pass
        else:
            if ((df.loc[i,'open'] + df.loc[i,'duration']) >= df.loc[j,'open']) and \
                (df.loc[i,'close'] >= (df.loc[j,'close'])):
                pathList.append([i,j,df.loc[i,'place'],df.loc[j,'place']])

column_names = ['V1','V2','origin','target']

path = pd.DataFrame(pathList, columns=column_names)
print(path.head())
path.to_csv('input/4_pathList.csv')