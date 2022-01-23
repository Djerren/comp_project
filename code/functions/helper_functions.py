import networkx as nx
import numpy as np
from posixpath import split

def find_other_node(edge, node):
    """
    This function finds the second node connected to a certain edge.
    (There might be a better way to do this.)
    """
    if edge[0] == node:
        return edge[1]
    else:
        return edge[0]

def get_ages(number):
    """
    This function generates the ages of the nodes according to an age distribution.
    """
    # Extracts the distribution from the file
    age_dist = []
    file = open("data/ages.csv")
    for line in file:
        line_split = line.split(";")
        age_dist.append(int(line_split[1]) + int(line_split[2]))

    # Generates ages according to distribution
    ages = []
    dist_sum = sum(age_dist)
    for age in range(len(age_dist)):
        ages = ages + [age] * int(number * age_dist[age] / dist_sum)
    for i in range(number - len(ages)):
        ages.append(np.random.randint(0,100))
    np.random.shuffle(ages)
    return ages

def facebook_network():
    network = nx.Graph()
    edges = []
    file = open("data/facebook_combined.txt")
    for line in file:
        edge = line.split()
        edges.append((int(edge[0]),int(edge[1])))
    network.add_edges_from(edges)
    return network