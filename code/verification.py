import networkx as nx
import numpy as np
from model import Model
from helper_functions import get_ages

def verify_infect(nr_nodes, nr_infects):
    network = nx.complete_graph(nr_nodes)
    model = Model(network, 1, 1, 1, get_ages(nr_nodes), 0)
    print("Is the right amount of nodes infected?")

    for number in nr_infects:
        model.infect(number)
        print(number == len(model.get_infecteds()))
        model.reset()

def verify_infection_rate(infection_rates, start_infections, nr_nodes):
    print("In each test the measured infection rate should approximate the given infection rate. \n(note that it is possible for this number to exceed 1)")
    network = nx.complete_graph(nr_nodes)
    for infection_rate in infection_rates:
        print("\nCurrent infection rate is:", infection_rate)
        print("measured infection rates:")

        model = Model(network, infection_rate, 1, 1, get_ages(nr_nodes), 0)

        for number in start_infections:
            model.infect(number)
            susceptibles = len(model.get_susceptibles())
            model.step()
            measured_infection_rate = len(model.get_exposeds()) * (nr_nodes - 1) / (susceptibles * number)
            print("with", number, "starting infections:", measured_infection_rate)
            model.reset()

def verify_incubation_period_and_infection_time(network, starting_infected, incubation_period, infection_time):
    model = Model(network, 1, incubation_period, infection_time, get_ages(len(network.nodes)), 0)
    model.infect(starting_infected)

    exposed_period = 0
    infectious_period = 0
    while not model.is_finished():
        model.step()
        exposed_period += len(model.get_exposeds())
        infectious_period += len(model.get_infecteds())

    print("Expected incubation period, based on given variable:", 1/incubation_period)
    print("Average incubation period:", exposed_period / (len(model.get_recovereds()) + len(model.get_deads())))

    print("\n Given infection time:", infection_time)
    print("Averege infectious period:", infectious_period / (len(model.get_recovereds()) + len(model.get_deads())))

def verify_vaccination_rate(network, starting_infected, vaccination_rates):
    for vaccination_rate in vaccination_rates:
        for vax_mode in ["random", "age", "degree"]:
            print("Currently testing", vax_mode, "vaccination method.")
            model = Model(network, 1, 1/5, 7, get_ages(len(network.nodes)), vaccination_rate, vaccination_method=vax_mode)
            model.infect(starting_infected)

            vaccinations_per_day = []
            while not model.is_finished():
                vaccinated = len(model.get_vaccinated())
                model.step()
                vaccinations_per_day.append(len(model.get_vaccinated()) - vaccinated)


            for i in range(len(vaccinations_per_day) - 1):
                if vaccinations_per_day[i] != vaccination_rate and vaccinations_per_day[i] != 0:
                    print("This was wrong")
                    print(vaccinations_per_day)
                    break

if __name__ == "__main__":
    sf_network = nx.barabasi_albert_graph(1000, 7)
    verify_infect(1000, [250, 500, 750])
    verify_infection_rate([0.25, 0.5, 0.75, 1], [250, 500, 750], 1000)
    verify_incubation_period_and_infection_time(sf_network, 10, 4/7, 7)
    verify_vaccination_rate(sf_network, 10, [10, 100, 200])






