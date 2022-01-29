from os.path import exists
from code.helper_functions import facebook_network
from code.model import Model
import networkx as nx

def facebook_test(vax_strat, iterations, infection_rate, incubation_period, infection_time, vaccination_time):
    """
    This method does iterations simulations on the facebook network and adds (!) the results to a possibly
    already existing file consisting of results with the same settings.
    """
    test_network = facebook_network()
    n = len(test_network.nodes)
    vaccination_rate = int(n/vaccination_time)

    test_model = Model(test_network, infection_rate, incubation_period, infection_time, vaccination_rate, vaccination_method=vax_strat)
    lines = 0
    if exists(f"stats/fb_{vax_strat}_{format(infection_rate, '.1f')}_{format(incubation_period, '.2f')}_{infection_time}_{vaccination_rate}.txt"):
        temp = open(f"stats/fb_{vax_strat}_{format(infection_rate, '.1f')}_{format(incubation_period, '.2f')}_{infection_time}_{vaccination_rate}.txt")
        lines = sum(1 for line in temp)
        temp.close()
    stats = open(f"stats/fb_{vax_strat}_{format(infection_rate, '.1f')}_{format(incubation_period, '.2f')}_{infection_time}_{vaccination_rate}.txt", "a")

    for i in range(lines, lines + iterations):
        print("At iteration nr.", i)
        test_model.reset(i)
        test_model.infect(5)
        while not test_model.is_finished():
            test_model.step()
        stats.write(f"{i};{test_model.get_time()};{n - len(test_model.get_susceptibles())};{len(test_model.get_deads())}\n")
    stats.close()

def single_facebook_test(vaccination_method, infection_rate, incubation_period, infection_time, vaccination_rate, random_seed):
    """
    This function does a single simulation on the facebook network, given the parameters. Should mostly be used to check the results.
    """
    test_network = facebook_network()
    n = len(test_network.nodes)
    test_model = Model(test_network, infection_rate, incubation_period, infection_time, vaccination_rate, vaccination_method, random_seed=random_seed)
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

def print_stats(age_file, degree_file):
    age_stats = open(age_file)
    lines, age_time, age_infected, age_dead = [0] * 4
    for line in age_stats:
        lines += 1
        line_split = line.split(";")
        age_time += int(line_split[1])
        age_infected += int(line_split[2])
        age_dead += int(line_split[3])
    age_stats.close()
    age_time /= lines
    age_infected /= lines
    age_dead /= lines

    degree_stats = open(degree_file)
    lines, degree_time, degree_infected, degree_dead = [0] * 4
    for line in degree_stats:
        lines += 1
        line_split = line.split(";")
        degree_time += int(line_split[1])
        degree_infected += int(line_split[2])
        degree_dead += int(line_split[3])
    degree_stats.close()
    degree_time /= lines
    degree_infected /= lines
    degree_dead /= lines

    print(f"age: {age_time} steps")
    print(f"infected: {round(age_infected, 2)}, dead: {round(age_dead, 2)}")
    print(f"degree: {degree_time} steps")
    print(f"infected: {round(degree_infected, 2)}, dead: {round(degree_dead, 2)}")


def main():
    single_facebook_test("age", 1.0, 0.21, 7, 40, 2)
    # facebook_test("random", 10, 0.5, 0.1, 7, 100)
    # facebook_test("random", 10, 0.5, 0.5, 7, 100)
    # facebook_test("random", 10, 0.5, 0.7, 7, 100)

    # facebook_test("none", 10, 0.5, 0.1, 7, 100)
    # facebook_test("none", 10, 0.5, 0.5, 7, 100)
    # facebook_test("none", 10, 0.5, 0.7, 7, 100)

    # facebook_test("age", 10, 0.5, 0.1, 7, 100)
    # facebook_test("age", 10, 0.5, 0.5, 7, 100)
    # facebook_test("age", 10, 0.5, 0.7, 7, 100)

    # facebook_test("degree", 10, 0.5, 0.1, 7, 100)
    # facebook_test("degree", 10, 0.5, 0.5, 7, 100)
    # facebook_test("degree", 10, 0.5, 0.7, 7, 100)


if __name__ == "__main__":
    main()
