import networkx as nx
from code.helper_functions import facebook_network
from code.model import Model
from code.visualise import draw_graph_simple, get_average, graph_infection_rate, print_network, boxplot
from code.verification import verify_incubation_period_and_infection_time, verify_infect, verify_infection_rate, verify_vaccination_rate

if __name__ == "__main__":
    # main()
    # boxplot("stats/fb_age_0.5_0.2_7_40.txt", "stats/fb_degree_0.5_0.2_7_40.txt",
            # "stats/fb_random_0.5_0.2_7_40.txt", "stats/fb_none_0.5_0.2_7_40.txt")
    # graph_infection_rate("death")
    graph_infection_rate("infections")
    """
    file = open(f"stats/fb_age_1.0_0.20_7_40.txt")
    average_old = get_average(file, 3)
    file.close()

    file = open(f"stats/fb_age_1.0_0.21_7_40.txt")
    average_new = get_average(file, 3)
    file.close()

    print(average_old)
    print(average_new)
    """
#     sf_network = nx.barabasi_albert_graph(1000, 7)
#     verify_infect(1000, [250, 500, 750])
#     verify_infection_rate([0.25, 0.5, 0.75, 1], [250, 500, 750], 1000)
#     verify_incubation_period_and_infection_time(sf_network, 10, 4/7, 7)
#     verify_vaccination_rate(sf_network, 10, [10, 100, 200])

