import matplotlib.pyplot as plt
import networkx as nx
from pyparsing import countedArray
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
    sum = 0
    counter = 0
    for line in file:
        counter += 1
        line_split = line.split(";")
        sum += int(line_split[index])
    
    return sum / counter

def graph_infection_rate(data):
    if data == "time":
        index = 1
    elif data == "infections":
        index = 2
    else:
        index = 3
    
    infection_rates = [i * 0.1 for i in range(1, 11)]
    none, random, age, degree = [[] for i in range(4)]

    for rate in infection_rates:
        file = open(f"stats/fb_none_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        none += [get_average(file, index)]
        file = open(f"stats/fb_random_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        random += [get_average(file, index)]
        file = open(f"stats/fb_age_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        age += [get_average(file, index)]
        file = open(f"stats/fb_degree_{format(rate, '.1f')}_5_10_25_0.05_0.05.txt")
        degree += [get_average(file, index)]
    
    plt.plot(infection_rates, none, label="none")
    plt.plot(infection_rates, random, label="random")
    plt.plot(infection_rates, age, label="age")
    plt.plot(infection_rates, degree, label="degree")
    plt.legend()
    plt.show()     
    