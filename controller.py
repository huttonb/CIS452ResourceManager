# Author: Bryce Hutton
# Date: 11/8/2018
# This program is a pseudo resource-manager that utilizes the MVP structure to create a graph depicting
# the status of processes, resources, and their connections.


import graphui
import reslogic

# The controller class is more aptly a presenter. It takes the logic from reslogic, and uses that to
# draw and present the graph ui.
class controller:
    def __init__(self):
        self.resmanager = reslogic.Resource_Manager(self)
        self.resgraph = graphui.resource_graph()

        # Takes the resources and processes from the logic and adds them to the graph.
        for i in self.resmanager.processes.keys():
            self.resgraph.add_proc_node(i)
        for i in self.resmanager.resources.keys():
            self.resgraph.add_res_node(i)
        # Draw the initial graph
        self.resgraph.draw_graph()
        # Go through actions listed in file provided.
        self.resmanager.commit_actions()


    # Update is an observer, that watches for when the state of a resource changes.
    # Depending on the type of connection, it adds or delets a node. The connection reqrelease
    # is for the release of a request edge.
    def update(self, process, resource, connection):
        if connection == "releases":
            self.resgraph.add_releases_edge(process, resource)
        elif connection == "connects":
            self.resgraph.add_connects_edge(process, resource)
        elif connection == "requests":
            self.resgraph.add_requests_edge(process, resource)
        elif connection == "reqrelease":
            self.resgraph.add_releases_edge(resource, process)
        self.resgraph.draw_graph()

c = controller()