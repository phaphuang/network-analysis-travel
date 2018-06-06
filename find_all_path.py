import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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
landmark_weight = [0, 4, 3, 4, 5, 5, 4]
DUT = 2     # Duration time of its region langmark p(r)
OT = 9      # Open time
CT = 21     # Close time
TimeRange = CT - OT
alpha = 0.5 # Initial alpha

# Find the possible paths
#for p in  nx.all_simple_paths(G,'0','0'):
#    print p
paths = list(nx.all_simple_paths(G,'0','0',cutoff=nx.number_of_nodes(G)+2))

WRank = dict()  # WRank(Tr)
TRank = dict()  # TRank(Tr)
PathDict = dict({
    'WRank': [],
    'TRank': [],
    'Path': [],
    'Beta': [],
    'Rho': []
})

for path in paths:
    #print(path)
    # Number of region landmarks within Tr : N(Tr)
    NTr = len(path) - 2

    if NTr >= k:

        beta = 1    # Beta is constant
        # Initial total time cost TC(Tr), delete start and stop (-2)
        TC = DUT * NTr
        sum_lmw = 0 # Initial summation of landmarks' weight

        for node in range(0, len(path)-1):
            # Find summation
            #print(path, ": ", G[path[node]][path[node+1]][0]['weight'])
            TC = TC + G[path[node]][path[node+1]][0]['distance']
            sum_lmw = sum_lmw + landmark_weight[int(path[node])]

        print("Path {} have TC equal to {}".format(path, TC))

        # Find rho
        if TC <= TimeRange:
            rho = 1
        else:
            rho = 0

        PathDict['Path'].append(path)
        PathDict['WRank'].append(sum_lmw)
        PathDict['TRank'].append(round(TC, 2))
        PathDict['Beta'].append(beta)
        PathDict['Rho'].append(rho)

    else:
        beta = 0

print(PathDict)

dfPath = pd.DataFrame(PathDict)
dfPath['TRanked'] = dfPath['TRank'].rank(ascending=True, method='dense')
dfPath['WRanked'] = dfPath['WRank'].rank(ascending=False, method='dense')
dfPath['FinTr'] = (alpha * ((1 + dfPath['Beta'])**(1/dfPath['WRanked']))) + \
                  ((1-alpha) * ((1 + dfPath['Rho'])**(1/dfPath['TRanked'])))

print(dfPath)

dfPath.to_csv('output/result.csv', encoding='utf-8')
# Find PageRank
#pr = nx.pagerank_numpy(G, alpha=0.9)
#print("Page Range = ", pr)
