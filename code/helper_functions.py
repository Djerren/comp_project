# helper_functions.py consists of a few functions that are useful in the rest of the project
# but don't fit in any other file.

import networkx as nx
import numpy as np

def get_vulnerabilities(number):
    """
    This function generates the vulnerabilities of the nodes according to an age distribution.
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

    # Sets vulnerability of nodes according to RIVM data
    vulnerabilities = [0.0] * len(ages)
    for i in range(len(vulnerabilities)):
        if ages[i] <= 49:
            continue
        elif ages[i] <= 54:
            vulnerabilities[i] = 0.001
            continue
        elif ages[i] <= 59:
            vulnerabilities[i] = 0.002
            continue
        elif ages[i] <= 64:
            vulnerabilities[i] = 0.005
            continue
        elif ages[i] <= 69:
            vulnerabilities[i] = 0.013
            continue
        elif ages[i] <= 74:
            vulnerabilities[i] = 0.03
            continue
        elif ages[i] <= 79:
            vulnerabilities[i] = 0.067
            continue
        elif ages[i] <= 84:
            vulnerabilities[i] = 0.114
            continue
        elif ages[i] <= 89:
            vulnerabilities[i] = 0.158
            continue
        elif ages[i] <= 94:
            vulnerabilities[i] = 0.188
            continue
        else:
            vulnerabilities[i] = 0.215

    return vulnerabilities

def facebook_network():
    """
    This function creates a social network based on data from facebook connections.
    https://snap.stanford.edu/data/ego-Facebook.html
    """
    network = nx.Graph()
    edges = []
    file = open("data/facebook_combined.txt")
    for line in file:
        edge = line.split()
        edges.append((int(edge[0]),int(edge[1])))
    network.add_edges_from(edges)
    return network

def get_average(file, index):
    """
    This function gives the average value and standard deviation for the data in a file.
    """
    file.seek(0)
    list = []
    for line in file:
        line_split = line.split(";")
        list += [int(line_split[index])]

    return np.mean(list), np.std(list)