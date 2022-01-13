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
    def __init__(self, network, base_spread_prob):
        self.base_spread_prob = base_spread_prob
        self.network = network

        # We could give each edge its own unique spread probability
        # (to simulate for example whether people are family or just acquaintances)
        # nx.set_edge_attributes(self.network, self.base_spread_prob, "spread_probability")

        # we keep track of the status of each node (person)
        # currently there are two possibilities: S means susceptible, I means infected.
        nx.set_node_attributes(self.network, "S", "status")

        # added for efficiency, even though we can access the status of a node through the network itself.
        # one of the methods might be redundant, so we could remove one.
        # Also, maybe a method to infect certain people at the start would be cleaner.
        self.infecteds = np.array([0])
        self.network.nodes[0]["status"] = "I"

    # might be unnecessary
    def reset(self):
        nx.set_node_attributes(self.network, "S", "status")
        self.infecteds = np.array([0])
        self.network.nodes[0]["status"] = "I"

    def step(self):
        """
        This function simulates one timestep of the model.
        """
        # we keep track of which nodes get infected this step and append them at the end.
        newly_infected = np.array([])

        # We loop over all infected nodes and infect their neighbours with certain probability.
        # status of nodes is changed immediately to make sure we do not infect the same person twice.
        for infected in self.infecteds:
            for edge in self.network.edges(infected):

                target = find_other_node(edge, infected)
                if self.network.nodes[target]["status"] == "S":

                    # We can use the following if we decide to use a different spread probability for each edge:
                    # spread_probability = self.network[edge[0]][edge[1]]["spread_probability"]

                    gets_infected = np.random.choice([0,1], p=[1- self.base_spread_prob, self.base_spread_prob])
                    if gets_infected:
                        newly_infected = np.append(newly_infected, [target])
                        self.network.nodes[target]["status"] = "I"

        self.infecteds = np.append(self.infecteds, newly_infected)

    def get_infecteds(self):
        return self.infecteds

    def get_susceptibles(self):
        return [node for node in self.network.nodes if self.network.nodes[node]["status"] == "S"]


if __name__ == "__main__":
    base_spread_prob = 0.5
    test_network = nx.watts_strogatz_graph(1000, 6, 0.05, seed=None)

    test_model = Model(test_network, base_spread_prob)
    print(test_model.get_infecteds())
    for i in range(1):
        test_model.step()
    print(test_model.get_infecteds())
    #print(test_model.get_susceptibles())



