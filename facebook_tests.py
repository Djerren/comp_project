from os.path import exists
from code.helper_functions import facebook_network
from code.model import Model

def main():
    test_network = facebook_network()
    n = len(test_network.nodes)
    iterations = 2
    infection_rate = 0.5
    incubation_period = 0.2
    infection_time = 7
    vaccination_rate = int(n/100)

    test_model = Model(test_network, infection_rate, incubation_period, infection_time, vaccination_rate, "age")
    lines = 0
    if exists(f"stats/fb_age_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt"):
        temp = open(f"stats/fb_age_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt")
        lines = sum(1 for line in temp)
        temp.close()
    age_stats = open(f"stats/fb_age_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt", "a")

    for i in range(lines, lines + iterations):
        print("age:", i)
        test_model.reset(i)
        test_model.infect(5)
        while not test_model.is_finished():
            test_model.step()
        age_stats.write(f"{i};{test_model.get_time()};{n - len(test_model.get_susceptibles())};{len(test_model.get_deads())}\n")
    age_stats.close()

    test_model = Model(test_network, infection_rate, incubation_period, infection_time, vaccination_rate, "degree")
    lines = 0
    if exists(f"stats/fb_degree_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt"):
        temp = open(f"stats/fb_degree_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt")
        lines = sum(1 for line in temp)
        temp.close()
    degree_stats = open(f"stats/fb_degree_{infection_rate}_{incubation_period}_{infection_time}_{vaccination_rate}.txt", "a")

    for i in range(lines, lines + iterations):
        print("degree:", i)
        test_model.reset(i)
        test_model.infect(5)
        while not test_model.is_finished():
            test_model.step()
        degree_stats.write(f"{i};{test_model.get_time()};{n - len(test_model.get_susceptibles())};{len(test_model.get_deads())}\n")
    degree_stats.close()

if __name__ == "__main__":
    main()
