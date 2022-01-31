import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D
import networkx as nx
from pyparsing import countedArray
import numpy as np
#from matplotlib.animation import

def draw_graph_simple(susceptible, infected, dead, recovered, time):
    """
    This function draws the evolution of dead, infected and recovered people
    over time using the simple time step.
    """

    plt.plot(time, susceptible, label="Susceptibles")
    plt.plot(time, infected, label="Infected")
    plt.plot(time, dead, label="Dead")
    plt.plot(time, recovered, label="Recovered")

    plt.xlabel("Time in days")
    plt.ylabel("Number of persons")
    plt.legend()
    plt.show()

def print_network(network):
    """
    Print the final network.
    """
    nx.draw()
    pass

def boxplot(age_file, degree_file, random_file, none_file):
    age_stats = open(age_file)
    age_deaths = []
    age_infected = []

    for line in age_stats:
        line_split = line.split(";")
        age_infected.append(int(line_split[2]))
        age_deaths.append(int(line_split[3]))


    degree_stats = open(degree_file)
    degree_deaths = []
    degree_infected = []

    for line in degree_stats:
        line_split = line.split(";")
        degree_infected.append(int(line_split[2]))
        degree_deaths.append(int(line_split[3]))

    random_stats = open(random_file)
    random_deaths = []
    random_infected = []

    for line in random_stats:
        line_split = line.split(";")
        random_infected.append(int(line_split[2]))
        random_deaths.append(int(line_split[3]))

    none_stats = open(none_file)
    none_deaths = []
    none_infected = []

    for line in none_stats:
        line_split = line.split(";")
        none_infected.append(int(line_split[2]))
        none_deaths.append(int(line_split[3]))

    plt.subplots(2, 2)
    plt.subplot(2, 2, 1)
    plt.title('Deaths')
    plt.boxplot([none_deaths])
    plt.xticks([1], ['None'])

    plt.subplot(2,2,2)
    plt.boxplot([random_deaths, age_deaths, degree_deaths])
    plt.xticks([1, 2, 3], ['Random', 'Age', 'Degree'])

    plt.subplot(2, 2, 3)
    plt.title('Infected')
    plt.boxplot([none_infected])
    plt.xticks([1], ['None'])

    plt.subplot(2,2,4)
    plt.boxplot([random_infected, age_infected, degree_infected])
    plt.xticks([1, 2, 3], ['Random', 'Age', 'Degree'])

    plt.show()

def get_average(file, index):
    list = []
    for line in file:
        line_split = line.split(";")
        list += [int(line_split[index])]
    
    return np.mean(list), np.std(list)
   
def compare_methods(data, parameter):
    if data == "time":
        index = 1
    elif data == "infections":
        index = 2
    else:
        index = 3
    
    if parameter == "infection_rate":
        parameters = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        file_names = []
        for p in parameters:
            file_names.append(f"{format(p, '.1f')}_5_10_25_0.05_0.05.txt")
    elif parameter == "incubation_period":
        parameters = [4, 5, 6, 7]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_{p}_10_25_0.05_0.05.txt")
    elif parameter == "infection_time":
        parameters = [6, 8, 10, 12, 14]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_{p}_25_0.05_0.05.txt")
    elif parameter == "vaccination_rate":
        parameters = [15, 20, 25, 30, 35]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_10_{p}_0.05_0.05.txt")
    elif parameter == "vaccine_spread_effectiveness":
        parameters = [0.03, 0.05, 0.07, 0.10]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_10_25_{format(p, '.2f')}_0.05.txt")
    else:
        parameters = [0.03, 0.05, 0.07, 0.10]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_10_25_0.05_{format(p, '.2f')}.txt")
    
    age_avg, degree_avg = [[],[]]
    age_std, degree_std = [[],[]]

    for file_name in file_names:
        file = open(f"stats/fb_age_" + file_name)
        avg, std = get_average(file, index)
        age_avg += [avg]
        age_std += [std]
        file = open(f"stats/fb_degree_" + file_name)
        avg, std = get_average(file, index)
        degree_avg += [avg]
        degree_std += [std]
    
    plt.subplot(121)
    plt.ylim(0,max(max(age_avg),max(degree_avg))+max(max(age_std),max(degree_std)))
    plt.errorbar(parameters, age_avg, yerr=age_std, label="age", marker="o", markersize=3, linestyle="none", elinewidth=1)
    plt.subplot(122)
    plt.ylim(0,max(max(age_avg),max(degree_avg))+max(max(age_std),max(degree_std)))
    plt.errorbar(parameters, degree_avg, yerr=degree_std, label="degree", marker="o", markersize=3, linestyle="none", elinewidth=1)
    plt.show()

def graph_methods(data, parameter):
    if data == "time":
        index = 1
    elif data == "infections":
        index = 2
    else:
        index = 3
    
    if parameter == "infection_rate":
        parameters = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        file_names = []
        for p in parameters:
            file_names.append(f"{format(p, '.1f')}_5_10_25_0.05_0.05.txt")
    elif parameter == "incubation_period":
        parameters = [4, 5, 6, 7]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_{p}_10_25_0.05_0.05.txt")
    elif parameter == "infection_time":
        parameters = [6, 8, 10, 12, 14]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_{p}_25_0.05_0.05.txt")
    elif parameter == "vaccination_rate":
        parameters = [15, 20, 25, 30, 35]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_10_{p}_0.05_0.05.txt")
    elif parameter == "vaccine_spread_effectiveness":
        parameters = [0.03, 0.05, 0.07, 0.10]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_10_25_{format(p, '.2f')}_0.05.txt")
    else:
        parameters = [0.03, 0.05, 0.07, 0.10]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_10_25_0.05_{format(p, '.2f')}.txt")
    
    none_avg, random_avg, age_avg, degree_avg = [[] for i in range(4)]
    none_std, random_std, age_std, degree_std = [[] for i in range(4)]

    for file_name in file_names:
        file = open("stats/fb_none_" + file_name)
        avg, std = get_average(file, index)
        none_avg += [avg]
        none_std += [std]
        file = open(f"stats/fb_random_" + file_name)
        avg, std = get_average(file, index)
        random_avg += [avg]
        random_std += [std]
        file = open(f"stats/fb_age_" + file_name)
        avg, std = get_average(file, index)
        age_avg += [avg]
        age_std += [std]
        file = open(f"stats/fb_degree_" + file_name)
        avg, std = get_average(file, index)
        degree_avg += [avg]
        degree_std += [std]
    
    diff = 0.05 * (parameters[1] - parameters[0])
    parameters1 = [p - diff for p in parameters]
    parameters2 = [p + diff for p in parameters]
    parameters3 = [p + 2 * diff for p in parameters]
    plt.errorbar(parameters1, none_avg, yerr=none_std, label="none", marker="o", markersize=3, linestyle="none", elinewidth=1)
    plt.errorbar(parameters, random_avg, yerr=random_std, label="random", marker="o", markersize=3, linestyle="none", elinewidth=1)
    plt.errorbar(parameters2, age_avg, yerr=age_std, label="age", marker="o", markersize=3, linestyle="none", elinewidth=1)
    plt.errorbar(parameters3, degree_avg, yerr=degree_std, label="degree", markersize=3, marker="o", linestyle="none", elinewidth=1)
    plt.legend()
    plt.show() 