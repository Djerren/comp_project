import networkx as nx
from code.visualise import draw_graph_simple, get_average, graph_methods, compare_methods, print_network, boxplot
from code.verification import verify_incubation_period_and_infection_time, verify_infect, verify_infection_rate, verify_vaccination_rate

if __name__ == "__main__":
    # boxplot("stats/fb_age_0.5_0.2_7_40.txt", "stats/fb_degree_0.5_0.2_7_40.txt",


    compare_methods("infections", "infection_rate")
    compare_methods("deaths", "infection_rate")
    compare_methods("time", "infection_rate")


    # sf_network = nx.barabasi_albert_graph(1000, 7)
    # verify_infect(1000, [250, 500, 750])
    # verify_infection_rate([0.25, 0.5, 0.75, 1], [250, 500, 750], 1000)
    # verify_incubation_period_and_infection_time(sf_network, 10, 4/7, 7)
    # verify_vaccination_rate(sf_network, 10, [10, 100, 200])

