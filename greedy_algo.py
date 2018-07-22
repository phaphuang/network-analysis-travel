# Force division to floating point in python 2.7
from __future__ import division

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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
        return (xmax - x)/(xmax - xmin)

def search_nodes(graph, node, start_time, end_time, visited=[], total_score=[]):
    visited.append(node)

    priority_cal = dict()
    best_time_cal = dict()
    distance_cal = dict()

    priority_score = dict()
    best_time_score = dict()
    distance_score = dict()
    total_score = dict()

    if(start_time < end_time):
        print("Node: ", node, " with neighbors node: ", graph.neighbors(node))
        for neighbor in graph.neighbors(node):
            if not neighbor in visited:

                print("Next Node ==========> ", neighbor)
                
                # Find Priority list
                priority_cal.update({neighbor: landmark_weight[int(neighbor)]})
                print("Priority raw: ", priority_cal)

                # Find Best time list
                best_time_cal.update({neighbor: cal_best_time(best_time[int(neighbor)], start_time+G[node][neighbor][0]['distance'])})
                print("Best time raw: ", best_time_cal)
                

                # Create distance list
                distance_cal.update({neighbor: G[node][neighbor][0]['distance']})
                print("Distance raw: ", distance_cal)
                
        print("################################ RESULT ################################")
        
        # Find Priority score
        priority_score.update({ key: cal_score(value, priority_cal.values()) for key, value in priority_cal.items() })
        print("Priority score: ", priority_score)

        # Find Best time score
        best_time_score.update({ key: cal_score(value, best_time_cal.values()) for key, value in best_time_cal.items() })
        print("Best time score: ", best_time_score)

        # Find Distance score
        distance_score.update({ key: cal_score_distance(value, distance_cal.values()) for key, value in distance_cal.items() })
        print("Distance score: ", distance_score)

        total_score.update({ key: priority_score[key] + best_time_score[key] + distance_score[key] 
                             for key, value in priority_score.items()})
        print("Total Score: ", total_score)

        #DUT = duration_hr[int(node)]
        #start_time = start_time + G[node][neighbor][0]['distance'] + DUT
        #print("Departure time of current node in this path: ", start_time)

    return visited


if __name__ == '__main__':

    G = nx.MultiDiGraph()

    edgefile = pd.read_csv('../data/edges.csv', header=0, dtype=object)

    for idx, row in edgefile.iterrows():
        G.add_edge(str(row[0]), str(row[1]), distance=float(row[2]))
    
    # Draw the network
    #nx.draw_networkx(G, with_labels = True, node_size = 500)
    #plt.show()

    # Convert networkx to pygraphviz
    A = nx.nx_agraph.to_agraph(G)
    A.layout(prog='circo')
    #A.layout(prog='dot')
    A.draw('output/test.png')

    # Define initial variable
    k = 5   # Number of user

    # First argument is for S
    start_time = 9      # Open time
    end_time = 21     # Close time
    TimeRange = start_time - end_time

    landmark_weight = [0, 4, 3, 4, 5, 5, 4]
    duration_min = [0, 120, 120, 120, 120, 120, 120]    # Duration time of its region langmark in min
    duration_hr = [x / 60 for x in duration_min] # Duration time of its region langmark in hr
    best_time = [end_time, 12, 11, 14, 16, 15, 18] # Assume Best time of starting point best_time[0] equal to Close time

    final_result = search_nodes(G, '0', start_time, end_time)
    #print(G.neighbors('0'))
    print(final_result)