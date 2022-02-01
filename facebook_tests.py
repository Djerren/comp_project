from os.path import exists
from code.helper_functions import facebook_network
from code.model import Model
import networkx as nx

def facebook_test(vax_strat, iterations, infection_rate=1.0, incubation_period=5, infection_time=10, vaccination_rate=25, vaccine_spread_effectiveness=0.05,
                 vaccine_mortality_effectiveness=0.05):
    """
    This method does iterations simulations on the facebook network and adds (!) the results to a possibly
    already existing file consisting of results with the same settings.
    """
    test_network = facebook_network()
    n = len(test_network.nodes)

    test_model = Model(test_network, infection_rate, incubation_period, infection_time, vaccination_rate, vax_strat, vaccine_spread_effectiveness, vaccine_mortality_effectiveness)
    lines = 0
    if exists(f"stats/fb_{vax_strat}_{format(infection_rate, '.1f')}_{incubation_period}_{infection_time}_{vaccination_rate}_{format(vaccine_spread_effectiveness, '.2f')}_{format(vaccine_mortality_effectiveness, '.2f')}.txt"):
        temp = open(f"stats/fb_{vax_strat}_{format(infection_rate, '.1f')}_{incubation_period}_{infection_time}_{vaccination_rate}_{format(vaccine_spread_effectiveness, '.2f')}_{format(vaccine_mortality_effectiveness, '.2f')}.txt")
        lines = sum(1 for line in temp)
        temp.close()
    stats = open(f"stats/fb_{vax_strat}_{format(infection_rate, '.1f')}_{incubation_period}_{infection_time}_{vaccination_rate}_{format(vaccine_spread_effectiveness, '.2f')}_{format(vaccine_mortality_effectiveness, '.2f')}.txt", "a")

    for i in range(lines, lines + iterations):
        print(f"{vax_strat} at iteration nr.", i)
        test_model.reset(i)
        test_model.infect(5)
        while not test_model.is_finished():
            test_model.step()
        stats.write(f"{i};{test_model.get_time()};{n - len(test_model.get_susceptibles())};{len(test_model.get_deads())}\n")
    stats.close()

def single_facebook_test(vax_strat, infection_rate, incubation_period, infection_time, vaccination_rate,
                         vaccine_spread_effectiveness, vaccine_mortality_effectiveness, random_seed):
    """
    This function does a single simulation on the facebook network, given the parameters. Should mostly be used to check the results.
    """
    test_network = facebook_network()
    n = len(test_network.nodes)
    test_model = Model(test_network, infection_rate, incubation_period, infection_time, vaccination_rate, vax_strat, vaccine_spread_effectiveness, vaccine_mortality_effectiveness, random_seed=random_seed)
    test_model.infect(5)
    while not test_model.is_finished():
        test_model.step()
    print(f"{random_seed};{test_model.get_time()};{n - len(test_model.get_susceptibles())};{len(test_model.get_deads())}")


# The next three functions have (currently) not been used for testing, so we skipped commenting them.
def ba_test(vax_strat, iterations, nr_nodes, nr_linking_edges, infection_rate, incubation_period, infection_time, vaccination_time):
    vaccination_rate = int(nr_nodes/vaccination_time)

    lines = 0
    if exists(f"stats/ba_{vax_strat}_{nr_nodes}_{nr_linking_edges}_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt"):
        temp = open(f"stats/ba_{vax_strat}_{nr_nodes}_{nr_linking_edges}_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt")
        lines = sum(1 for line in temp)
        temp.close()
    stats = open(f"stats/ba_{vax_strat}_{nr_nodes}_{nr_linking_edges}_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt", "a")

    for i in range(lines, lines + iterations):
        print("At iteration nr.", i)
        test_network = nx.barabasi_albert_graph(nr_nodes, nr_linking_edges)
        test_model = Model(test_network, infection_rate, incubation_period, infection_time, vaccination_rate, vaccination_method=vax_strat, random_seed=i)
        test_model.reset(i)
        test_model.infect(5)
        while not test_model.is_finished():
            test_model.step()
        stats.write(f"{i};{test_model.get_time()};{nr_nodes - len(test_model.get_susceptibles())};{len(test_model.get_deads())}\n")
    stats.close()

def ws_test(vax_strat, iterations, nr_nodes, avg_degree, rewiring_prob, infection_rate, incubation_period, infection_time, vaccination_time):
    vaccination_rate = int(nr_nodes/vaccination_time)

    lines = 0
    if exists(f"stats/ws_{vax_strat}_{nr_nodes}_{avg_degree}_{rewiring_prob}_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt"):
        temp = open(f"stats/ws_{vax_strat}_{nr_nodes}_{avg_degree}_{rewiring_prob}_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt")
        lines = sum(1 for line in temp)
        temp.close()
    stats = open(f"stats/ws_{vax_strat}_{nr_nodes}_{avg_degree}_{rewiring_prob}_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt", "a")

    for i in range(lines, lines + iterations):
        print("At iteration nr.", i)
        test_network = nx.watts_strogatz_graph(nr_nodes, avg_degree, rewiring_prob)
        test_model = Model(test_network, infection_rate, incubation_period, infection_time, vaccination_rate, vaccination_method=vax_strat, random_seed=i)
        test_model.reset(i)
        test_model.infect(5)
        while not test_model.is_finished():
            test_model.step()
        stats.write(f"{i};{test_model.get_time()};{nr_nodes - len(test_model.get_susceptibles())};{len(test_model.get_deads())}\n")
    stats.close()

def tests_for_figures():
    for infection_rate in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        facebook_test("none", 10, infection_rate=infection_rate)
        facebook_test("random", 10, infection_rate=infection_rate)
        facebook_test("degree", 10, infection_rate=infection_rate)
        facebook_test("age", 10, infection_rate=infection_rate)

def main():
    tests_for_figures()

if __name__ == "__main__":
    main()
