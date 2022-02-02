"""
This file contains functions to generate plots from the data.
"""

import matplotlib.pyplot as plt
import numpy as np

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
