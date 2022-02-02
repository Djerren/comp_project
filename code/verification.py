"""
This file consists of some functions with which one can test the model on correctness.
only checks the basic model, the rest is more difficult to check and we do that just by
checking if the results make sense.
"""

import networkx as nx
from code.model import Model

def verify_infect(nr_nodes, nr_infects):
    """
    This function verifies whether the right amount of nodes is infected after calling the infect function.
    """
    # does not matter which graph we test this on.
    network = nx.complete_graph(nr_nodes)
    model = Model(network, 1, 1, 1, 0, "none", 0.05, 0.05)
    print("Testing if the right number of nodes is infected each time:")

    for i, number in enumerate(nr_infects):
        model.infect(number)
        print(f"with {number} infections: {number == len(model.get_infecteds())}")
        model.reset(i)

def verify_infection_rate(infection_rates, start_infections, nr_nodes):
    """
    With this function one can verify that the given infection rate is close to the measured infection rate.
    """
    print("Testing if the infection_rate parameter does what it is supposed to do.")
    print("In each test the measured infection rate should approximate the given infection rate.")
    print("(note that it is possible for the measured infection rate to exceed 1)")

    # We use a complete graph for this test, such that calculating the measured infection rate after
    # one time step is "easy".(Since each node will have the same number of infected neighbours.)
    network = nx.complete_graph(nr_nodes)
    for infection_rate in infection_rates:
        print("\nCurrent infection rate is:", infection_rate)
        print("measured infection rates:")

        model = Model(network, infection_rate, 1, 1, 0, "none", 0.05, 0.05)

        for i, number in enumerate(start_infections):
            model.infect(number)
            susceptibles = len(model.get_susceptibles())
            model.step()
            measured_infection_rate = (len(model.get_exposeds()) * (nr_nodes - 1)) / (susceptibles * number)
            print("with", number, "starting infections:", measured_infection_rate)
            model.reset(i)

def verify_incubation_period_and_infection_time(network, starting_infected, incubation_period, infection_time):
    """
    With this function one can verify that the expected incubation period and infection time are close to
    what given as a parameter.
    """
    model = Model(network, 1.0, incubation_period, infection_time, 0, "none", 0.05, 0.05)
    model.infect(starting_infected)

    exposed_period = 0
    infectious_period = 0
    # measured average incumbation period/infection time will be calculated using the sum of times each
    # node is exposed/infected
    while not model.is_finished():
        model.step()
        exposed_period += len(model.get_exposeds())
        infectious_period += len(model.get_infecteds())

    print("Testing if measured average incubation period/infection time approximate the given values\n")
    print("Given incubation period:", incubation_period)
    print("Average incubation period:", exposed_period / (len(model.get_recovereds()) + len(model.get_deads())))

    print("\n Given infection time:", infection_time)
    print("Averege infectious period:", infectious_period / (len(model.get_recovereds()) + len(model.get_deads())))

def verify_vaccination_rate(network, starting_infected, vaccination_rates):
    """
    This method checks if the right amount of people is vaccinated at each time step.
    """
    print("Testing if the right amount of nodes is vaccinated each day.\n")
    for vaccination_rate in vaccination_rates:
        for vax_mode in ["random", "age", "degree"]:
            print(f"Currently testing {vax_mode} vaccination method with vaccination rate {vaccination_rate}. (if nothing else is printed all went well).")
            model = Model(network, 1, 5, 7, vaccination_rate, vax_mode, 0.05, 0.05)
            model.infect(starting_infected)

            vaccinations_per_day = []
            while not model.is_finished():
                vaccinated = len(model.get_vaccinated())
                model.step()
                vaccinations_per_day.append(len(model.get_vaccinated()) - vaccinated)

            # If there is a day on which less then vaccination_rate amount of nodes are vaccinated and this is not
            # because all people are already vaccinated, then something went wrong
            for i in range(len(vaccinations_per_day) - 1):
                if vaccinations_per_day[i] != vaccination_rate and vaccinations_per_day[i + 1] != 0:
                    print("This was wrong")
                    print(vaccinations_per_day)
                    break






