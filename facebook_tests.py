from os.path import exists
from code.helper_functions import facebook_network
from code.model import Model

def test(iterations, infection_rate, incubation_period, infection_time, vaccination_time):
    test_network = facebook_network()
    n = len(test_network.nodes)
    vaccination_rate = int(n/vaccination_time)

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

def print_stats(age_file, degree_file):
    age_stats = open(age_file)
    lines = 0
    age_infected = 0
    age_dead = 0
    for line in age_stats:
        lines += 1
        line_split = line.split(";")
        age_infected += int(line_split[2])
        age_dead += int(line_split[3])
    age_stats.close()
    age_infected /= lines
    age_dead /= lines

    degree_stats = open(degree_file)
    lines = 0
    degree_infected = 0
    degree_dead = 0
    for line in degree_stats:
        lines += 1
        line_split = line.split(";")
        degree_infected += int(line_split[2])
        degree_dead += int(line_split[3])
    degree_stats.close()
    degree_infected /= lines
    degree_dead /= lines

    print("age:")
    print(f"infected: {round(age_infected, 2)}, dead: {round(age_dead, 2)}")
    print("degree:")
    print(f"infected: {round(degree_infected, 2)}, dead: {round(degree_dead, 2)}")


def main():
    #test(20, 0.5, 0.2, 7, 100)
    print_stats("stats/fb_age_0.5_0.2_7_40.txt", "stats/fb_degree_0.5_0.2_7_40.txt")

if __name__ == "__main__":
    main()
