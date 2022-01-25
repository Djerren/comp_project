import matplotlib.pyplot as plt
import networkx as nx
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

def boxplot(age_file, degree_file):
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

    plt.subplots(2, 1)
    plt.subplot(2, 1, 1)
    plt.boxplot([age_deaths, degree_deaths])
    plt.subplot(2, 1, 2)
    plt.boxplot([age_infected, degree_infected])

    plt.show()