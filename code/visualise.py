import matplotlib.pyplot as plt
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

def graph_infection_rate(data):
    if data == "time":
        index = 1
    elif data == "infections":
        index = 2
    else:
        index = 3
    
    infection_rates = [i * 0.1 for i in range(1, 11)]
    none_avg, random_avg, age_avg, degree_avg = [[] for i in range(4)]
    none_std, random_std, age_std, degree_std = [[] for i in range(4)]

    for rate in infection_rates:
        file = open(f"stats/fb_none_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        none_avg += [avg]
        none_std += [std]
        file = open(f"stats/fb_random_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        random_avg += [avg]
        random_std += [std]
        file = open(f"stats/fb_age_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        age_avg += [avg]
        age_std += [std]
        file = open(f"stats/fb_degree_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        degree_avg += [avg]
        degree_std += [std]
    
    plt.errorbar(infection_rates, none_avg, yerr=none_std, label="none")
    plt.errorbar(infection_rates, random_avg, yerr=random_std, label="random")
    plt.errorbar(infection_rates, age_avg, yerr=age_std, label="age")
    plt.errorbar(infection_rates, degree_avg, yerr=degree_std, label="degree")
    plt.legend()
    plt.show()   
    
def compare_infection_rates(data):
    if data == "time":
        index = 1
    elif data == "infections":
        index = 2
    else:
        index = 3
    
    infection_rates = [i * 0.1 for i in range(1, 11)]
    age_avg, degree_avg = [[],[]]
    age_std, degree_std = [[],[]]

    for rate in infection_rates:
        file = open(f"stats/fb_age_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        age_avg += [avg]
        age_std += [std]
        file = open(f"stats/fb_degree_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        degree_avg += [avg]
        degree_std += [std]
    
    plt.subplot(121)
    plt.ylim(0,max(max(age_avg),max(degree_avg))+max(max(age_std),max(degree_std)))
    plt.errorbar(infection_rates, age_avg, yerr=age_std, label="age")
    plt.subplot(122)
    plt.ylim(0,max(max(age_avg),max(degree_avg))+max(max(age_std),max(degree_std)))
    plt.errorbar(infection_rates, degree_avg, yerr=degree_std, label="degree")
    plt.show()

def graph_incubation_period(data):
    if data == "time":
        index = 1
    elif data == "infections":
        index = 2
    else:
        index = 3
    
    incubation_periods = [4, 5, 6, 7]
    none_avg, random_avg, age_avg, degree_avg = [[] for i in range(4)]
    none_std, random_std, age_std, degree_std = [[] for i in range(4)]

    for period in incubation_periods:
        file = open(f"stats/fb_none_1.0_{period}_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        none_avg += [avg]
        none_std += [std]
        file = open(f"stats/fb_random_1.0_{period}_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        random_avg += [avg]
        random_std += [std]
        file = open(f"stats/fb_age_1.0_{period}_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        age_avg += [avg]
        age_std += [std]
        file = open(f"stats/fb_degree_1.0_{period}_10_25_0.05_0.05.txt")
        avg, std = get_average(file, index)
        degree_avg += [avg]
        degree_std += [std]
    
    plt.errorbar(incubation_periods, none_avg, yerr=none_std, label="none")
    plt.errorbar(incubation_periods, random_avg, yerr=random_std, label="random")
    plt.errorbar(incubation_periods, age_avg, yerr=age_std, label="age")
    plt.errorbar(incubation_periods, degree_avg, yerr=degree_std, label="degree")
    plt.legend()
    plt.show() 