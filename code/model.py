import networkx as nx
import numpy as np
from code.helper_functions import find_other_node

class Model:
    def __init__(self, network, infection_rate, incubation_period, infection_time, ages, vaccination_rate, vaccination_method="random", vaccination_start=0, vaccine_spread_effectiveness=0.05, vaccine_mortality_effectiveness=0.1):
        self.infection_rate = infection_rate
        self.incubation_period = incubation_period
        self.infection_time = infection_time
        self.ages = ages
        self.vaccination_method = vaccination_method
        self.vaccination_rate = vaccination_rate
        self.vaccination_start = vaccination_start
        self.vaccine_spread_effectiveness = vaccine_spread_effectiveness
        self.vaccine_mortality_effectiveness = vaccine_mortality_effectiveness

        self.network = network
        self.t = 0
        self.finished = False

        # We keep track of the status, vaccination and age of each node (person)
        nx.set_node_attributes(self.network, "S", "status")
        nx.set_node_attributes(self.network, "NV", "vaccination")
        nx.set_node_attributes(self.network, 0, "age")
        for i in range(len(self.network.nodes)):
            self.network.nodes[i]["age"] = self.ages[i]

    def reset(self):
        """
        This function sets the status of every node in the network back to susceptible
        """
        nx.set_node_attributes(self.network, "S", "status")
        nx.set_node_attributes(self.network, "NV", "vaccination")
        nx.set_node_attributes(self.network, 0, "age")
        for i in range(len(self.network.nodes)):
            self.network.nodes[i]["age"] = self.ages[i]
        self.t = 0
        self.finished = False

    def infect(self, number):
        """
        this function infects people in the network. Currently does this randomly
        but could happen in different ways.
        """
        infected = np.copy(self.network.nodes)
        np.random.shuffle(infected)
        for i in infected[0:number]:
            self.network.nodes[i]["status"] = "I"

    def vaccinate(self):
        """
        This function vaccinated the nodes of the network based on the chosen method:
         - random: vaccination is done randomly
         - age:    vaccination is done in order of age (high to low)
         - degree: vaccination is done in order of node degree (high to low)
        """
        if len(self.get_unvaccinated()) < self.vaccination_rate:
            nx.set_node_attributes(self.network, "V", "vaccination")
            return
        # Random vaccination
        if self.vaccination_method == "random":
            vaccinated = np.copy(self.get_unvaccinated())
            np.random.shuffle(vaccinated)
            for i in vaccinated[0:self.vaccination_rate]:
                self.network.nodes[i]["vaccination"] = "V"
        # Age based vaccination
        elif self.vaccination_method == "age":
            counter = 0
            sorted_nodes = sorted(self.network.nodes(data=True), key=lambda x: x[1]["age"], reverse=True)
            for node in sorted_nodes:
                if counter == self.vaccination_rate:
                    return
                if self.network.nodes[node[0]]["vaccination"] == "NV":
                    self.network.nodes[node[0]]["vaccination"] = "V"
                    counter += 1
        # Degree based vaccination
        elif self.vaccination_method == "degree":
            counter = 0
            sorted_nodes = sorted(self.network.degree, key=lambda x: x[1], reverse=True)
            for node in sorted_nodes:
                if counter == self.vaccination_rate:
                    return
                if self.network.nodes[node[0]]["vaccination"] == "NV":
                    self.network.nodes[node[0]]["vaccination"] = "V"
                    counter += 1

    def step(self):
        """
        This function simulates one timestep of the model, using the simple method
        of computing probabilities for an entire day.
        """

        if self.finished:
            return

        if self.t >= self.vaccination_start:
            self.vaccinate()

        # We change the status of the nodes at the very end of one time step. This
        # way, we make sure that changes this time step do not affect others within the same
        # timestep.
        newly_exposed = np.array([])
        newly_infected = np.array([])
        newly_recovered = np.array([])
        newly_dead = np.array([])
        for node in self.network.nodes:
            # If the current node is susceptible it has a chance to be exposed to the virus via
            # its neighbours. The model this is based on also includes a probability to be exposed
            # via any other person in the network. We could add this later (or not).
            if self.network.nodes[node]["status"] == "S":
                infected_neighbours = 0
                for edge in self.network.edges(node):
                    neighbour = find_other_node(edge, node)
                    if self.network.nodes[neighbour]["status"] == "I":
                        if self.network.nodes[node]["vaccination"] == "NV":
                            infected_neighbours += 1
                        else:
                            infected_neighbours += self.vaccine_spread_effectiveness

                exposed_prob = 0
                if len(self.network.edges(node)):
                    if self.network.nodes[node]["vaccination"] == "NV":
                        exposed_prob = (infected_neighbours / len(self.network.edges(node))) * self.infection_rate
                    else:
                        exposed_prob = (infected_neighbours / len(self.network.edges(node))) * self.infection_rate * self.vaccine_spread_effectiveness

                if np.random.choice([0,1], p=[1 - exposed_prob, exposed_prob]):
                    newly_exposed = np.append(newly_exposed, [node])

            # If the current node is exposed, every day it has a chance to become infected/infectuous.
            elif self.network.nodes[node]["status"] == "E":
                if np.random.choice([0,1], p=[1 - self.incubation_period, self.incubation_period]):
                    newly_infected = np.append(newly_infected, [node])

            # If the current node is infected, every day it has a chance to recover and a chance to die.
            elif self.network.nodes[node]["status"] == "I":
                if self.network.nodes[node]["vaccination"] == "NV":
                    mortality_rate = (self.network.nodes[node]["age"] / 100) ** 5 / 5
                    p_temp = [self.infection_time - 1, 1 - mortality_rate, mortality_rate]
                    p = [rate / self.infection_time for rate in p_temp]
                    transition = np.random.choice([0,1,2], p=p)
                else:
                    mortality_rate = (self.network.nodes[node]["age"] / 100) ** 5 / 5 * self.vaccine_mortality_effectiveness
                    p_temp = [self.infection_time - 1, 1 - mortality_rate, mortality_rate]
                    p = [rate / self.infection_time for rate in p_temp]
                    transition = np.random.choice([0,1,2], p=p)

                if transition == 1:
                    newly_recovered = np.append(newly_recovered, [node])
                elif transition == 2:
                    newly_dead = np.append(newly_dead, [node])

        for node in newly_exposed:
            self.network.nodes[node]["status"] = "E"
        for node in newly_infected:
            self.network.nodes[node]["status"] = "I"
        for node in newly_recovered:
            self.network.nodes[node]["status"] = "R"
        for node in newly_dead:
            self.network.nodes[node]["status"] = "F"

        if len(self.get_exposeds()) + len(self.get_infecteds()) == 0:
            self.finished = True
        self.t += 1

    # def step_complicated(self):
    #     """
    #     This function performs one timestep of the model using the complicated method.
    #     """

    #     if self.finished:
    #         return

    #     # These two values will help us to decide a time when the next event will happen.
    #     r = np.random.uniform()

    #     # we start with elements in the list to make the appends work, there might be a nicer way to do this.
    #     probabilities = np.array([0])
    #     events = np.array([(0,0)])
    #     for node in self.network.nodes:
    #         # If the current node is susceptible it has a chance to be exposed to the virus via
    #         # its neighbours. The model this is based on also includes a probability to be exposed
    #         # via any other person in the network. We could add this later (or not).
    #         if self.network.nodes[node]["status"] == "S":
    #             infected_neighbours = 0
    #             for edge in self.network.edges(node):
    #                 neighbour = find_other_node(edge, node)
    #                 if self.network.nodes[neighbour]["status"] == "I":
    #                     if self.network.nodes[neighbour]["vaccination"] == "NV":
    #                         infected_neighbours += 1
    #                     else:
    #                         infected_neighbours += 0.2

    #             exposed_prob = 0
    #             if len(self.network.edges(node)):
    #                 if self.network.nodes[node]["vaccination"] == "NV":
    #                     exposed_prob = (infected_neighbours / len(self.network.edges(node))) * self.infection_rate
    #                 else:
    #                     exposed_prob = (infected_neighbours / len(self.network.edges(node))) * self.infection_rate * 0.2

    #             probabilities = np.append(probabilities, [exposed_prob])
    #             events = np.append(events, [(node, "E")], axis=0)

    #         # If the current node is exposed, every day it has a chance to become infected/infectuous.
    #         elif self.network.nodes[node]["status"] == "E":
    #             probabilities = np.append(probabilities, [self.incubation_period])
    #             events = np.append(events, [(node, "I")], axis=0)

    #         # If the current node is infected, every day it has a chance to recover and a chance to die.
    #         elif self.network.nodes[node]["status"] == "I":
    #             probabilities = np.append(probabilities, [self.recovery_rate])
    #             events = np.append(events, [(node, "R")], axis=0)

    #             probabilities = np.append(probabilities, [self.mortality_rate])
    #             events = np.append(events, [(node, "F")], axis=0)

    #     if np.sum(probabilities) > 0:
    #         probability_of_event = 1 - np.prod(1 - probabilities)
    #         time_to_next_event = (1 / probability_of_event) * np.log(1 / r)
    #         self.t += time_to_next_event

    #         event = np.random.choice(np.arange(len(events)), p=probabilities/np.sum(probabilities))
    #         self.network.nodes[int(events[event][0])]["status"] = events[event][1]
    #     else:
    #         self.finished = True

    def get_infecteds(self):
        return [node for node in self.network.nodes if self.network.nodes[node]["status"] == "I"]

    def get_susceptibles(self):
        return [node for node in self.network.nodes if self.network.nodes[node]["status"] == "S"]

    def get_exposeds(self):
        return [node for node in self.network.nodes if self.network.nodes[node]["status"] == "E"]

    def get_recovereds(self):
        return [node for node in self.network.nodes if self.network.nodes[node]["status"] == "R"]

    def get_deads(self):
        return [node for node in self.network.nodes if self.network.nodes[node]["status"] == "F"]

    def get_unvaccinated(self):
        return [node for node in self.network.nodes if self.network.nodes[node]["vaccination"] == "NV"]

    def get_vaccinated(self):
        return [node for node in self.network.nodes if self.network.nodes[node]["vaccination"] == "V"]

    def get_time(self):
        return self.t

    def is_finished(self):
        return self.finished
