import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, OrderedDict
import sys
import collections
import community

l1=sys.argv

f = open(l1[1],'r')     #Read input file
t = [[int(r.split(' ')[0]),int(r.split(' ')[1])]  for r in f.read().splitlines()]     #create a list of connected nodes


G1 = nx.Graph()         #Generate graph
G1.add_edges_from(t)

G = nx.Graph()          #Generate graph
G.add_edges_from(t)

edges = G.edges()      #create a list of all edges
finalList = []

#Function to display clusters and graph
def DisplayGraph(fList):
    global finalList
    for m in sorted(fList):
        print m

    nodeColor = [0] * len(G1.nodes())

    for i in range(0,len(finalList)):  # created a list for node_color attribute to assign a color for respective clusters
        for j in finalList[i]:
            if 0 in G1.nodes():
                nodeColor[j] = i + 1
            else:
                nodeColor[j - 1] = i + 1

    nx.draw_networkx(G1, cmap=plt.get_cmap('jet'), with_labels=True,
                     node_color=nodeColor)  # draw graph with different clusters
    plt.axis("off")
    plt.savefig(l1[2])                      #Save final graph image

#Implementation of Girvan Newman Algorithm
def girvan_newman_algorithm():
    iterNo = 0
    globDict = {}
    finalDict = {}
    global finalList

    while len(edges):       #while loop until there is no edge in the given graph
        iterNo+=1
        a=nx.edge_betweenness_centrality(G)         #calculates betweenness for each edge in the given graph and returns a list of values

        maxBetw = []

        sortOD = collections.OrderedDict(sorted(a.items()))
        a = sorted(sortOD.items(), key=lambda kv: kv[1], reverse=True)      #sorted the dictionary

        a = dict(a)

        maxBetw = max(a.values())       #Fetching the Maximum betweenness value

        rEdges = []
        for x in a:

            if a[x] == maxBetw:
                rEdges.append(x)        #Fetching the edges with maximum betweenness value


        G.remove_edges_from(rEdges)     #Removing those edges with maximum betweenness value from graph G

        for r in rEdges:
            edges.remove(r)             #Removing those edges with maximum betweenness value from list of edges

        cc = nx.connected_components(G) #Fetching out connected components from the graph G

        Lcc = list(cc)

        globDict.update({iterNo:Lcc})   #updating the dictionary with connected components for each iteration

        modDict = {}

        for i in range(0,len(Lcc)):
            for j in Lcc[i]:

                modDict[j]=i+1

        if (len(G.edges())!=0):
            mod = community.modularity(modDict,G)       #Calculating modularity

            finalDict.update({iterNo:mod})              #Updating the dictionary with modularity for each iteration

    maxMod = max(finalDict.values())                    #Fetching out the maximum modularity value


    for x in finalDict:

        if finalDict[x] == maxMod:                     #Storing the graph structure with highest modularity
            finalList = globDict[x]
    fList = []
    for i in finalList:
        fList.append(list(i))
    return fList


if __name__=="__main__":
    finalClusters=girvan_newman_algorithm()
    DisplayGraph(finalClusters)