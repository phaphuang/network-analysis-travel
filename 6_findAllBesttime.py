# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 20:06:56 2018

@author: philanderz
"""

# Force division to floating point in python 2.7
from __future__ import division

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm

# tb = best time, ta = arrive time
def cal_best_time(tb, ta):
    #print(tb, ta)
    return 1 - (abs(tb-ta)/tb)

def cal_score(x, xlist):
    xmax = max(xlist)
    xmin = min(xlist)

    if xmax == xmin:
        return 1
    else:
        return (x - xmin)/(xmax - xmin)

def cal_score_distance(x, xlist):
    xmax = max(xlist)
    xmin = min(xlist)

    if xmax == xmin:
        return 1
    else:
        return 1 - ((x - xmin)/(xmax - xmin))

G = nx.MultiDiGraph()

edgefile = pd.read_csv('input/5_pathWithWeight.csv', header=0, dtype=object)

for idx, row in edgefile.iterrows():
    G.add_edge(str(row[0]), str(row[1]), distance=float(row[2]))


# Draw the network
#nx.draw_networkx(G, with_labels = True, node_size = 500)
#plt.show()

# Convert networkx to pygraphviz
#A = nx.nx_agraph.to_agraph(G)
#A.layout(prog='circo')
#A.layout(prog='dot')
#A.draw('output/5_pathNetwork.png')

# Define initial variable
k = 5   # Number of user

# First argument is for S
OT = 9      # Open time
CT = 21     # Close time
TimeRange = CT - OT

df = pd.read_csv('input/2_convertScoreToRating.csv', header=0, encoding="ISO-8859-1")
ratingSr = df["autoRating"].astype("int").tolist()
durationSr = df["duration"].tolist()
bestTimeSr = df["besttime"].tolist()

landmark_weight = [0]
landmark_weight = landmark_weight + ratingSr
duration_hr = [0]
duration_hr = duration_hr + durationSr # Duration time of its region langmark in hr
best_time = [CT]
best_time = best_time + bestTimeSr # Assume Best time of starting point best_time[0] equal to Close time

### Find the possible paths and store in generator for better performance
#for p in  nx.all_simple_paths(G,'0','0'):
#    print p
paths = (nx.all_simple_paths(G,'0','0',cutoff=nx.number_of_nodes(G)+2))

PathDict = dict({
    'Path': [],
    'FinalScore': [],
    'EndTime': [],
    'Beta': [],
    'Rho': []
})

#for path in paths[:10]:
for path in tqdm(paths):
    #print(path)
    # Number of region landmarks within Tr : N(Tr)
    ##print("###################################### START NEW PATH #########################################")
    ##print("Path: ", path)
    NTr = len(path) - 2

    if NTr >= k:

        beta = 1    # Beta is constant
        # Initial total time cost TC(Tr) = TEnd as Open Time
        TEnd = OT
        # Initial summation score
        sum_score = 0

        for idx, node in enumerate(range(0, len(path)-1), 1):
            priority_cal = []
            best_time_cal = []
            distance_cal = []
            time_current_cal = []

            # Find Neighbors of nodes
            ##print("Node: ", path[node], "with neighbors: ", G.neighbors(path[node]))
            if idx == len(path)-1:
                neighbors_of_node = [x for x in G.neighbors(path[node]) if x in path[:node] and x == '0']
            else:
                neighbors_of_node = [x for x in G.neighbors(path[node]) if x not in path[:node]]
            
            ##print("Neighbors which not in previous path: ", neighbors_of_node)
            
            # Find Priority list
            priority_cal.append([landmark_weight[int(n)] for n in neighbors_of_node])
            #print("Priority raw: ", priority_cal)
            priority_score = [cal_score(x, priority_cal[0]) for x in priority_cal[0]]
            #print("Priority score: ", priority_score)

            # Find Best time list
            best_time_cal.append([cal_best_time(best_time[int(n)], TEnd+G[path[node]][n][0]['distance']) for n in neighbors_of_node])
            # TEnd is departure time of current node in this path
            DUT = duration_hr[int(path[node])]
            TEnd = TEnd + G[path[node]][path[node+1]][0]['distance'] + DUT
            ##print("Best time raw: ", best_time_cal)
            best_time_score = [cal_score(x, best_time_cal[0]) for x in best_time_cal[0]]
            ##print("Best time score: ", best_time_score)
            ##print("Departure time of current node in this path: ", TEnd)
            
            if TEnd > CT:
                print("Out of loop")
                break
            else:
                continue
            

            # Find Distance score
            distance_cal.append([G[path[node]][n][0]['distance'] for n in neighbors_of_node])
            #print("Distance raw: ", distance_cal)
            distance_score = [cal_score_distance(x, distance_cal[0]) for x in distance_cal[0]]
            #print("Distance score: ", distance_score)

            ##print("###################### NEXT NODE #######################")
            ##print("Path[node+1] = ", path[node+1])

            if neighbors_of_node:
                total_score = priority_score[neighbors_of_node.index(path[node+1])] + \
                            best_time_score[neighbors_of_node.index(path[node+1])] + \
                            distance_score[neighbors_of_node.index(path[node+1])]
                sum_score = sum_score + total_score
            
            ##print("Final score: ", sum_score)

        # Find rho
        if TEnd <= CT:
            rho = 1
        else:
            rho = 0
        
        PathDict['Path'].append(path)
        PathDict['FinalScore'].append(sum_score)
        PathDict['EndTime'].append(TEnd)
        PathDict['Beta'].append(beta)
        PathDict['Rho'].append(rho)
        
    else:
        beta = 0

dfPath = pd.DataFrame(PathDict)
dfPath['CalScore'] = dfPath['FinalScore'] * dfPath['Rho'] * dfPath['Beta']

print(dfPath)

dfPath.to_csv('output/6_findAllBestTime.csv', encoding='utf-8')