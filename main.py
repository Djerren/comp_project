import networkx as nx
from code.visualise import graph_methods, compare_methods, sensitivity
from code.verification import verify_incubation_period_and_infection_time, verify_infect, verify_infection_rate, verify_vaccination_rate

def poster_figures():
    """
    This function creates the figures in the poster and the report from pre-computed data.
    """
    graph_methods("infections", "infection_rate")
    graph_methods("deaths", "infection_rate")

def alternative_figures(parameter):
    """
    This function creates figures similar to the poster figures, but for other parameters as well.
    Figures are created using pre-computed data
    """
    graph_methods("infections", parameter)
    graph_methods("deaths", parameter)
    graph_methods("time", parameter)

def compare_figures(parameter):
    """
    With this code, degree and age based vaccination can be compared in different metrics
    (infections, deaths and time) for changes in different parameters. Figures are created
    using pre-computed data.
    """
    compare_methods("infections", parameter)
    compare_methods("deats", parameter)
    compare_methods("time", parameter)

def verifications():
    """
    This code runs a few verification tests on the base model, we verified the more complicated additions
    just by checking if the results made sense.
    """
    # we use a Barabasi-albert graph for some of these simple tests.
    sf_network = nx.barabasi_albert_graph(1000, 7)
    verify_infect(1000, [250, 500, 750])
    print()
    print("---------------------------------------------------")
    print()
    verify_infection_rate([0.25, 0.5, 0.75, 1], [250, 500, 750], 1000)
    print()
    print("---------------------------------------------------")
    print()
    verify_incubation_period_and_infection_time(sf_network, 10, 5, 7)
    print()
    print("---------------------------------------------------")
    print()
    verify_vaccination_rate(sf_network, 10, [10, 100, 200])

if __name__ == "__main__":
    # poster_figures()
    # alternative_figures("vaccine_mortality_effectiveness")
    # compare_figures("incubation_period")
    # verifications()
    sensitivity("incubation_period")
    sensitivity("infection_time")
    sensitivity("vaccination_rate")
    sensitivity("vaccine_spread_effectiveness")
    sensitivity("vaccine_mortality_effectiveness")



