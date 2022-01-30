from tkinter import N
import networkx as nx
import numpy as np
from code.helper_functions import find_other_node, get_vulnerabilities

class Model:
    """
    The Model class runs a disease spread simulation based on data from covid-19. This model
    is based on the model described in https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0240878
    with added functionality for vaccinations and vulnerabilty. Vulnerability of a node is based on age, and affects
    the probability of dying. This probability is based on data of RIVM (source). vaccinations affect the probability
    of dying, the probability of getting exposed and the probability of spreading. The effects of vaccinations and
    the standard values are based on data of RIVM (source).
    """

    def __init__(self, network, infection_rate, incubation_period, infection_time,
                 vaccination_rate, vaccination_method, vaccine_spread_effectiveness,
                 vaccine_mortality_effectiveness, random_seed=0):
        """
        This function initializes the model with the following parameters:
         - network: The network on which the simulation will be run. nodes are people and edges are connections
           through which the disease can spread.
         - infection_rate: this parameter is the probability that a node is exposed to the disease if it has come
           into contact with an infected node. (so if every neighbour of a node is infected this parameter is
           exactly the probability that the node is exposed.)
         - incubation_period: this parameter is the probability for a node to go from the exposed state to infected on
           a given day. Can also be interpreted as the expected fraction of the total number number of exposed nodes
           that will become infected. 1/incubation_period gives the expected number of days before a node goes from
           exposed to infected.
         - infection_time: this parameter is the expected number of days before an infected node either dies or
           recovers. 1/infection_time is the probability that an infected node dies or recovers on a given day and
           can also be interpreted as the expected fraction of infected nodes that will either die or recover on
           a certain day.
         - vaccination_rate: the number of people that are vaccinated each day.
         - vaccination_method: this decides which people will be prioritized for vaccinations:
             - none: no vaccinations
             - random: vaccinations are decided randomly
             - age: old people (vulnerable people) are prioritized
             - degree: nodes with high degree are prioritized
         - vaccine_spread_effectiveness: This parameter represents the effect of vaccinations on the spread of the
           disease. If a node is vaccinated, the probability of getting exposed is multiplied by this parameter and
           the probability of getting exposed via a vaccinated person is also multiplied by this parameter.
         - vaccine_mortality_effectiveness: the probability of dying is multiplied by this parameter if the node is
           vaccinated.
         - random_seed: this parameter decides the randomness, so results can be repeated and checked.
        """
        self.network = network
        self.infection_rate = infection_rate
        self.incubation_period = 1 / incubation_period
        self.infection_time = infection_time
        self.vaccination_rate = vaccination_rate
        self.vaccination_method = vaccination_method
        self.vaccine_spread_effectiveness = vaccine_spread_effectiveness
        self.vaccine_mortality_effectiveness = vaccine_mortality_effectiveness

        # We call the reset function to set all the starting values of the nodes.
        self.reset(random_seed)

    def reset(self, random_seed=0):
        """
        This function sets the status of every node in the network back to susceptible
        """
        np.random.seed(random_seed)
        nx.set_node_attributes(self.network, "S", "status")
        nx.set_node_attributes(self.network, "NV", "vaccination")
        nx.set_node_attributes(self.network, 0, "age")

        vulnerabilities = get_vulnerabilities(len(self.network.nodes))
        for i in range(len(self.network.nodes)):
            self.network.nodes[i]["vulnerability"] = vulnerabilities[i]
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
        if self.vaccination_method == "none":
            return

        eligible = self.get_eligible()
        if len(eligible) < self.vaccination_rate:
            for node in eligible:
                self.network.nodes[node]["vaccination"] = "V"
            return

        # Random vaccination
        if self.vaccination_method == "random":
            vaccinated = np.copy(eligible)
            np.random.shuffle(vaccinated)
            for i in vaccinated[0:self.vaccination_rate]:
                self.network.nodes[i]["vaccination"] = "V"
        # Age based vaccination
        elif self.vaccination_method == "age":
            counter = 0
            sorted_nodes = sorted(self.network.nodes(data=True), key=lambda x: x[1]["vulnerability"], reverse=True)
            for node in sorted_nodes:
                if counter == self.vaccination_rate:
                    return
                if node[0] in eligible:
                    self.network.nodes[node[0]]["vaccination"] = "V"
                    counter += 1
        # Degree based vaccination
        elif self.vaccination_method == "degree":
            counter = 0
            sorted_nodes = sorted(self.network.degree, key=lambda x: x[1], reverse=True)
            for node in sorted_nodes:
                if counter == self.vaccination_rate:
                    return
                if node[0] in eligible:
                    self.network.nodes[node[0]]["vaccination"] = "V"
                    counter += 1

    def step(self):
        """
        This function simulates one timestep of the model, using the simple method
        of computing probabilities for an entire day.
        """
        if self.finished:
            return

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
                        infected_neighbours += 1

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
                # mortality rate is a function based on age that was fitted through a dataset from RIVM.
                if self.network.nodes[node]["vaccination"] == "NV":
                    mortality_rate = self.network.nodes[node]["vulnerability"]
                    p_temp = [self.infection_time - 1, 1 - mortality_rate, mortality_rate]
                    p = [rate / self.infection_time for rate in p_temp]
                    transition = np.random.choice([0,1,2], p=p)
                else:
                    mortality_rate = self.network.nodes[node]["vulnerability"] * self.vaccine_mortality_effectiveness
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

    def get_eligible(self):
        unvaccinated = [node for node in self.network.nodes if self.network.nodes[node]["vaccination"] == "NV"]
        eligible = [node for node in unvaccinated if self.network.nodes[node]["status"] == "S"
                                                  or self.network.nodes[node]["status"] == "E"]
        return eligible

    def get_vaccinated(self):
        return [node for node in self.network.nodes if self.network.nodes[node]["vaccination"] == "V"]

    def get_time(self):
        return self.t

    def is_finished(self):
        return self.finished
