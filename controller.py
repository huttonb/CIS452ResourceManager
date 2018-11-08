import graphui
import reslogic
class controller:
    def __init__(self):
        self.rm = reslogic.Resource_Manager(self)
        self.resgraph = graphui.resource_graph()

        for i in self.rm.processes.keys():
            self.resgraph.add_proc_node(i)

        for i in self.rm.resources.keys():
            self.resgraph.add_res_node(i)
      #  self.resgraph.draw_graph()
        self.rm.commit_actions()
  #      self.resgraph.draw_graph()

    def update(self, process, resource, connection):
        return
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