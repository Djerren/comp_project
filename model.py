import networkx as nx
import numpy as np

# helper functions: (needs seperate file but was too lazy)
def find_other_node(edge, node):
    """
    This function finds the second node connected to a certain edge.
    (There might be a better way to do this.)
    """
    if edge[0] == node:
        return edge[1]
    else:
        return edge[0]

class Model:
    def __init__(self, network, infection_rate, incubation_period, recovery_rate, mortality_rate):
        self.infection_rate = infection_rate
        self.incubation_period = incubation_period
        self.recovery_rate = recovery_rate
        self.mortality_rate = mortality_rate

        self.network = network
        self.t = 0
        self.finished = False

        # we keep track of the status of each node (person)
        nx.set_node_attributes(self.network, "S", "status")

    def reset(self):
        """
        This function sets the status of every node in the network back to susceptible
        """
        nx.set_node_attributes(self.network, "S", "status")
        self.t = 0
        self.finished = False

    def infect(self, number):
        """
        this function infects people in the network. Currently does this randomly
        but could happen in different ways.
        """

        infected = np.random.choice(self.network.nodes, size=number)
        for i in infected:
            self.network.nodes[i]["status"] = "I"

    def step(self):
        """
        This function simulates one timestep of the model, using the simple method
        of computing probabilities for an entire day.
        """

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
                    exposed_prob = (infected_neighbours / len(self.network.edges(node))) * self.infection_rate

                if np.random.choice([0,1], p=[1 - exposed_prob, exposed_prob]):
                    newly_exposed = np.append(newly_exposed, [node])

            # If the current node is exposed, every day it has a chance to become infected/infectuous.
            elif self.network.nodes[node]["status"] == "E":
                if np.random.choice([0,1], p=[1 - self.incubation_period, self.incubation_period]):
                    newly_infected = np.append(newly_infected, [node])

            # If the current node is infected, every day it has a chance to recover and a chance to die.
            elif self.network.nodes[node]["status"] == "I":
                transition = np.random.choice([0,1,2], p=[1 - self.recovery_rate - self.mortality_rate, self.recovery_rate, self.mortality_rate])
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

        self.t += 1

    def step_complicated(self):
        """
        This function performs one timestep of the model using the complicated method.
        """

        if self.finished:
            return

        # These two values will help us to decide a time when the next event will happen.
        r = np.random.uniform()

        # we start with elements in the list to make the appends work, there might be a nicer way to do this.
        probabilities = np.array([0])
        events = np.array([(0,0)])
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
                    exposed_prob = (infected_neighbours / len(self.network.edges(node))) * self.infection_rate

                probabilities = np.append(probabilities, [exposed_prob])
                events = np.append(events, [(node, "E")], axis=0)

            # If the current node is exposed, every day it has a chance to become infected/infectuous.
            elif self.network.nodes[node]["status"] == "E":
                probabilities = np.append(probabilities, [self.incubation_period])
                events = np.append(events, [(node, "I")], axis=0)

            # If the current node is infected, every day it has a chance to recover and a chance to die.
            elif self.network.nodes[node]["status"] == "I":
                probabilities = np.append(probabilities, [self.recovery_rate])
                events = np.append(events, [(node, "R")], axis=0)

                probabilities = np.append(probabilities, [self.mortality_rate])
                events = np.append(events, [(node, "F")], axis=0)

        if np.sum(probabilities)>0:
            probability_of_event = 1 - np.prod(1 - probabilities)
            time_to_next_event = (1 / probability_of_event) * np.log(1 / r)
            self.t += time_to_next_event

            event = np.random.choice(np.arange(len(events)), p=probabilities/np.sum(probabilities))
            self.network.nodes[int(events[event][0])]["status"] = events[event][1]
        else:
            self.finished = True

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

    def get_time(self):
        return self.t


if __name__ == "__main__":
    test_network = nx.watts_strogatz_graph(100, 6, 0.05, seed=None)

    test_model = Model(test_network, 0.5, 0.5, 0.125, 0.125)
    test_model. infect(5)
    for i in range(100):
        print(test_model.get_time())
        print(test_model.get_susceptibles())
        print(test_model.get_exposeds())
        print(test_model.get_infecteds())
        print(test_model.get_deads())
        print(test_model.get_recovereds(),"\n")
        test_model.step_complicated()
    #print(test_model.get_susceptibles())



