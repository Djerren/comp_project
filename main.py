import networkx as nx
from code.helper_functions import facebook_network
from code.model import Model
from code.visualise import draw_graph_simple, print_network, boxplot

def main():
    # Model(network, infection_rate, incubation_rate, recovery_rate, mortality_rate, ages, vaccination_method, vaccination_rate, vaccination_start)

    # small world (with the right parameters)
    # test_network = nx.watts_strogatz_graph(1000, 6, 0.05, seed=None)

    # # scale-free (with the right parameters)
    # sf_network = nx.barabasi_albert_graph(1000, 7)

    # # scale-free highly clustered (with the right parameters)
    # sfhc_network = nx.powerlaw_cluster_graph(1000, 10, 0.05)

    # more models can be found here: https://networkx.org/documentation/stable/reference/generated/networkx.generators.random_graphs.powerlaw_cluster_graph.html
    # also has references

    test_network = facebook_network()
    # test_network = nx.watts_strogatz_graph(n, 6, 0.05, seed=None)
    n = len(test_network.nodes)

    # test_model = Model(test_network, 0.25, 0.2, 0.125, 0.125, ages, "degree", int(n/100), 20)
    # t = []
    # S = []
    # E = []
    # I = []
    # R = []
    # D = []
    # test_model.infect(1)
    # while not test_model.is_finished():
    #     test_model.step()
    #     t.append(test_model.get_time())
    #     S.append(len(test_model.get_susceptibles()) / n * 100)
    #     E.append(len(test_model.get_exposeds()) / n * 100)
    #     I.append(len(test_model.get_infecteds()) / n * 100)
    #     R.append(len(test_model.get_recovereds()) / n * 100)
    #     D.append(len(test_model.get_deads()) / n * 100)

    # print("infected:", n - len(test_model.get_susceptibles()))
    # print("dead:", len(test_model.get_deads()))
    # plt.plot(t, S, label="S")
    # plt.plot(t, E, label="E")
    # plt.plot(t, I, label="I")
    # plt.plot(t, R, label="R")
    # plt.plot(t, D, label="D")
    # plt.legend()
    # plt.show()

    iterations = 10

    test_model = Model(test_network, 0.5, 0.2, 7, int(n/100), "age")
    infected_age = 0
    dead_age = 0
    # susceptible, infected, dead, recovered, time = ([] for i in range(5))

    for i in range(iterations):
        print("age:", i)
        test_model.infect(5)
        while not test_model.is_finished():
            test_model.step()
            # time.append(test_model.get_time())
            # print(test_model.get_time())
            # susceptible.append(len(test_model.get_susceptibles()))
            # print(len(test_model.get_susceptibles()))
            # infected.append(len(test_model.get_infecteds()))
            # recovered.append(len(test_model.get_recovereds()))
            # dead.append(len(test_model.get_deads()))

        # draw_graph_simple(susceptible, infected, dead, recovered, time)
        print(len(test_model.get_deads()))
        print((n - len(test_model.get_susceptibles())))
        dead_age += len(test_model.get_deads()) / iterations
        infected_age += (n - len(test_model.get_susceptibles())) / iterations
        #print_network()
        test_model.reset(i+1)


    test_model = Model(test_network, 0.5, 0.2, 7, int(n/100), "degree")
    infected_degree = 0
    dead_degree = 0

    for i in range(iterations):
        print("degree:", i)
        test_model.infect(5)
        while not test_model.is_finished():
            test_model.step()
        print(len(test_model.get_deads()))
        print((n - len(test_model.get_susceptibles())))
        dead_degree += len(test_model.get_deads()) / iterations
        infected_degree += (n - len(test_model.get_susceptibles())) / iterations
        test_model.reset(i+1)

    print(f"age:\ninfected: {infected_age}\ndead: {dead_age}\ndegree:\ninfected: {infected_degree}\ndead: {dead_degree}")

if __name__ == "__main__":
    #main()
    boxplot("stats/fb_age_0.5_0.2_7_40.txt", "stats/fb_degree_0.5_0.2_7_40.txt",
            "stats/fb_random_0.5_0.2_7_40.txt", "stats/fb_none_0.5_0.2_7_40.txt")
