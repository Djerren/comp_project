"""
This file contains functions to generate plots from the data.
"""

import matplotlib.pyplot as plt
from code.helper_functions import get_average

def compare_methods(data, parameter):
    """
    This function plots the average data of age based vaccination and degree based
    vaccination next to each other. The parameters decide what is plotted:
     - data:      this parameter decides which data to plot (time, infections or deaths).
     - parameter: this parameter decides which parameter of the model is on the y-axis.
    """
    # Generate index of data
    if data == "time":
        index = 1
    elif data == "infections":
        index = 2
    else:
        index = 3

    # Generate file name and list of values for correct parameter
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

    # Find averages and standard deviations of data
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

    # Plot graphs
    plt.subplot(121)
    plt.ylim(0,max(max(age_avg),max(degree_avg))+max(max(age_std),max(degree_std)))
    plt.errorbar(parameters, age_avg, yerr=age_std, label="age", marker="o", markersize=3, linestyle="dotted", linewidth=0.5, elinewidth=1)
    plt.subplot(122)
    plt.ylim(0,max(max(age_avg),max(degree_avg))+max(max(age_std),max(degree_std)))
    plt.errorbar(parameters, degree_avg, yerr=degree_std, label="degree", marker="o", markersize=3, linestyle="dotted", linewidth=0.5, elinewidth=1)
    plt.show()

def graph_methods(data, parameter):
    """
    This function plots the data for all vaccination methods in one graph.
    The parameters decide what is plotted:
     - data:      this parameter decides which data to plot (time, infections or deaths).
     - parameter: this parameter decides which parameter of the model is on the y-axis.
    """
    # Generate index of data
    if data == "time":
        title = "Time taken for virus to die out for different values of " + parameter + "."
        ylabel = "time (days)"
        index = 1
    elif data == "infections":
        title = "Total infections for different values of " + parameter + "."
        ylabel = "number of infections"
        index = 2
    else:
        title = "Death toll for different values of " + parameter + "."
        ylabel = "death toll"
        index = 3

    # Generate file name and list of values for correct parameter
    none_method = True
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
        none_method = False
        parameters = [15, 20, 25, 30, 35]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_10_{p}_0.05_0.05.txt")
    elif parameter == "vaccine_spread_effectiveness":
        none_method = False
        parameters = [0.03, 0.04, 0.05, 0.06, 0.07]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_10_25_{format(p, '.2f')}_0.05.txt")
    else:
        none_method = False
        parameters = [0.03, 0.04, 0.05, 0.06, 0.07]
        file_names = []
        for p in parameters:
            file_names.append(f"1.0_5_10_25_0.05_{format(p, '.2f')}.txt")

    # Find averages and standard deviations of data
    diff = 0.05 * (parameters[1] - parameters[0])
    if none_method:
        none_avg, none_std = [[],[]]
        for file_name in file_names:
            file = open("stats/fb_none_" + file_name)
            avg, std = get_average(file, index)
            none_avg += [avg]
            none_std += [std]
        parameters1 = [p - diff for p in parameters]
        plt.errorbar(parameters1, none_avg, yerr=none_std, label="none", marker="o", markersize=3, linestyle="dotted", linewidth=0.5, elinewidth=1)

    random_avg, age_avg, degree_avg = [[] for i in range(3)]
    random_std, age_std, degree_std = [[] for i in range(3)]
    for file_name in file_names:
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

    # Plot graphs
    diff = 0.05 * (parameters[1] - parameters[0])
    parameters2 = [p + diff for p in parameters]
    parameters3 = [p + 2 * diff for p in parameters]
    plt.errorbar(parameters, random_avg, yerr=random_std, label="random", marker="o", markersize=3, linestyle="dotted", linewidth=0.5, elinewidth=1)
    plt.errorbar(parameters2, age_avg, yerr=age_std, label="age", marker="o", markersize=3, linestyle="dotted", linewidth=0.5, elinewidth=1)
    plt.errorbar(parameters3, degree_avg, yerr=degree_std, label="degree", markersize=3, marker="o", linestyle="dotted", linewidth=0.5, elinewidth=1)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(parameter)
    plt.legend()
    plt.show()

def sensitivity(parameter):
    """
    This function prints the sensitivity for each parameter.
    """
    # Get averages of 20% deviations
    if parameter == "incubation_period":
        file = open("stats/fb_random_1.0_4_10_25_0.05_0.05.txt")
        avg_infected_1 = get_average(file, 2)[0]
        avg_death_1 = get_average(file, 3)[0]
        file = open("stats/fb_random_1.0_6_10_25_0.05_0.05.txt")
        avg_infected_2 = get_average(file, 2)[0]
        avg_death_2 = get_average(file, 3)[0]
    elif parameter == "infection_time":
        file = open("stats/fb_random_1.0_5_8_25_0.05_0.05.txt")
        avg_infected_1 = get_average(file, 2)[0]
        avg_death_1 = get_average(file, 3)[0]
        file = open("stats/fb_random_1.0_5_12_25_0.05_0.05.txt")
        avg_infected_2 = get_average(file, 2)[0]
        avg_death_2 = get_average(file, 3)[0]
    elif parameter == "vaccination_rate":
        file = open("stats/fb_random_1.0_5_10_20_0.05_0.05.txt")
        avg_infected_1 = get_average(file, 2)[0]
        avg_death_1 = get_average(file, 3)[0]
        file = open("stats/fb_random_1.0_5_10_30_0.05_0.05.txt")
        avg_infected_2 = get_average(file, 2)[0]
        avg_death_2 = get_average(file, 3)[0]
    elif parameter == "vaccine_spread_effectiveness":
        file = open("stats/fb_random_1.0_5_10_25_0.04_0.05.txt")
        avg_infected_1 = get_average(file, 2)[0]
        avg_death_1 = get_average(file, 3)[0]
        file = open("stats/fb_random_1.0_5_10_25_0.06_0.05.txt")
        avg_infected_2 = get_average(file, 2)[0]
        avg_death_2 = get_average(file, 3)[0]
    else:
        file = open("stats/fb_random_1.0_5_10_25_0.05_0.04.txt")
        avg_infected_1 = get_average(file, 2)[0]
        avg_death_1 = get_average(file, 3)[0]
        file = open("stats/fb_random_1.0_5_10_25_0.05_0.06.txt")
        avg_infected_2 = get_average(file, 2)[0]
        avg_death_2 = get_average(file, 3)[0]
    
    # Calculate differences on deviations
    diff_infected = abs(avg_infected_1 - avg_infected_2) / 2
    diff_death = abs(avg_death_1 - avg_death_2) / 2
    center_infected = (avg_infected_1 + avg_infected_2) / 2
    center_death = (avg_death_1 + avg_death_2) / 2
    
    print(parameter)
    print(" - 20% difference infected:", round(100 * diff_infected / center_infected, 1), "%")
    print(" - 20% difference deaths:  ", round(100 * diff_death / center_death, 1), "%")
