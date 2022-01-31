# This file consists of some functions with which one can test the model on correctness.
# only checks the basic model, the rest is more difficult to check and we do that just by
# checking if the results make sense.

import networkx as nx
import numpy as np
from code.model import Model

def verify_infect(nr_nodes, nr_infects):
    """
    This function verifies whether the right amount of nodes is infected after calling the infect function.
    """
    network = nx.complete_graph(nr_nodes)
    model = Model(network, 1, 1, 1, 0, "none", 0.05, 0.05)
    print("Is the right amount of nodes infected?")

    for number in nr_infects:
        model.infect(number)
        print(number == len(model.get_infecteds()))
        model.reset()

def verify_infection_rate(infection_rates, start_infections, nr_nodes):
    """
    With this function one can verify that the given infection rate is close to the measured infection rate.
    """
    print("In each test the measured infection rate should approximate the given infection rate. \n(note that it is possible for this number to exceed 1)")
    network = nx.complete_graph(nr_nodes)
    for infection_rate in infection_rates:
        print("\nCurrent infection rate is:", infection_rate)
        print("measured infection rates:")

        model = Model(network, infection_rate, 1, 1, 0, "none", 0.05, 0.05)

        for number in start_infections:
            model.infect(number)
            susceptibles = len(model.get_susceptibles())
            model.step()
            measured_infection_rate = len(model.get_exposeds()) * (nr_nodes - 1) / (susceptibles * number)
            print("with", number, "starting infections:", measured_infection_rate)
            model.reset()

def verify_incubation_period_and_infection_time(network, starting_infected, incubation_period, infection_time):
    """
    With this function one can verify that the expected incubation period and infection time are close to
    what given as a parameter.
    """
    model = Model(network, 1.0, incubation_period, infection_time, 0, "none", 0.05, 0.05)
    model.infect(starting_infected)

    exposed_period = 0
    infectious_period = 0
    while not model.is_finished():
        model.step()
        exposed_period += len(model.get_exposeds())
        infectious_period += len(model.get_infecteds())

    print("Given incubation period:", incubation_period)
    print("Average incubation period:", exposed_period / (len(model.get_recovereds()) + len(model.get_deads())))

    print("\n Given infection time:", infection_time)
    print("Averege infectious period:", infectious_period / (len(model.get_recovereds()) + len(model.get_deads())))

def verify_vaccination_rate(network, starting_infected, vaccination_rates):
    """
    This method checks if the right amount of people is vaccinated at each time step.
    """
    for vaccination_rate in vaccination_rates:
        for vax_mode in ["random", "age", "degree"]:
            print("Currently testing", vax_mode, "vaccination method. (if nothing else is printed all went well).")
            model = Model(network, 1, 5, 7, vaccination_rate, vax_mode, 0.05, 0.05)
            model.infect(starting_infected)

            vaccinations_per_day = []
            while not model.is_finished():
                vaccinated = len(model.get_vaccinated())
                model.step()
                vaccinations_per_day.append(len(model.get_vaccinated()) - vaccinated)


            for i in range(len(vaccinations_per_day) - 1):
                if vaccinations_per_day[i] != vaccination_rate and vaccinations_per_day[i + 1] != 0:
                    print("This was wrong")
                    print(vaccinations_per_day)
                    break






