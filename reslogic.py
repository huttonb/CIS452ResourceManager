class Resource:
    def __init__(self, rid):
        self.held = False
        self.heldby = False
        print("Resource " + str(rid) + " initialized")
        self.name = "r" + str(rid)
        self.process_queue = []

    def waiting_processes(self, proc):
        self.process_queue.append(proc)

    def check_held(self):
        return self.held

    def hold_taken(self, proc):
        self.heldby = proc
        self.held = True

    def hold_released(self):
        self.held = False

    def check_proc_queue(self):
        if (len(self.process_queue) > 0):
            return self.process_queue.pop(0).take_resource(self)




class Process:
    def __init__(self, pid):
        self.name = "p" + str(pid)
        print("Process " + str(pid) + " initialized")
        self.requesting = False
        self.resource_queue = []
        self.holding = []
    def wanted_resources(self, res):
        self.resource_queue.append(res)
    # Checks to see if the process can take resource, if it can, it does
    # There are two reasons for why the resource can't be taken
    # 1. The process is currently requesting another resource
    # 2. The resource is already being used by a different process.
    def take_resource(self, res):
        if self.requesting == res:
            if (res.check_held() == False):
                res.hold_taken(self)
                self.holding.append(res)
                print(self.name + " has taken hold of newly released resource " + res.name)
                self.requesting = False
            else:
                print(self.name + " can't hold " + res.name + ", it is already being used by another process")
                return False

        elif (self.requesting != False):
            res.waiting_processes(self)
            return False
        else:
            self.requesting = res
            if (res.check_held() == False):
                res.hold_taken(self)
                self.holding.append(res)
                print(self.name + " has taken hold of resource " + res.name)
                self.requesting = False
            else:
                print(self.name + " can't hold " + res.name + ", it is already being used by another process")
                return False
        return True

    def release_resource(self, res):
        if self.requesting == False:
            if res in self.holding:
                res.hold_released()
                self.holding.remove(res)
                print(self.name + " has released resource " + res.name)
                return res.check_proc_queue()
            else:
                print(self.name + " is not holding " + res.name)

    def print_resources(self):
        for r in self.holding:
            print(self.name + " is holding resource " + r.name)


class Resource_Manager:
    def __init__(self, obs):
        self.list = self.read_file(r'testinput3.data')
        self.observer = obs
        numProcesses = self.list[0]
        numResources = self.list[1]
        self.processes = {}
        self.resources = {}
        for i in range (0, int(numProcesses[0])):
            p1 = Process(i)
            self.processes[("p" + str(i))] = p1
        for i in range(0, int(numResources[0])):
            r1 = Resource(i)
            self.resources[("r" + str(i))] = r1

    def commit_actions(self):
        for action in self.list:
            if len(action) == 3:
                process_name = action[0]
                resource_name = action[2]
                if action[1] == "requests":
                    f1 = self.processes.get(process_name).take_resource(self.resources.get(resource_name))
                    if (not f1):
                        self.processes.get(process_name).wanted_resources(self.resources.get(resource_name))
                        self.resources.get(resource_name).waiting_processes(self.processes.get(process_name))
                        self.update(process_name, resource_name, "requests")
                    else:
                        self.update(process_name, resource_name, "connects")
                # After a process has released a resource, check to see if next acquisition is successful
                # for the graph
                elif action[1] == "releases":
                    if (self.processes.get(process_name).release_resource(self.resources.get(resource_name))):
                        # When releasing this one we send the resource and process in opposite order.
                        self.update(self.resources.get(resource_name).heldby.name, resource_name, "reqrelease")
                        self.update(self.resources.get(resource_name).heldby.name, resource_name, "connects")
                    self.update(process_name, resource_name, "releases")
                # Check to see if there are more than two processes waiting, if there is
                # check for a deadlock.
                waiting_proc = 0
                for i in self.processes.values():
                    if i.requesting == True:
                        waiting_proc += 1
                    if waiting_proc >= 2:
                        self.lock_check()
                        break;


    #Update sends an update to the controller, contains the resource, process, and type of connection
    def update(self, process, resource, connection):
        self.observer.update(process,resource,connection)

    def lock_check(self):
        for i in self.processes.values():
            if i.holding:
               if not self.lock_check(i, len(self.processes.values())):
                    print ("Deadlock detected.")
                    break;


    # lock_check recursively checks for a deadlock
    # It goes down by going to the process the current processes requested resource is being held by
    # If that process is free, it's not a deadlock and returns false, if it's in hold as well it continues
    # the recursion, once loops hits 0, it comes back as a deadlock, as that means it is impossible for the cycle
    # to be anything but a deadlock.
    # True: No deadlock
    # False: Deadlock
    def lock_check(self, proc, loops):
        #if requested resources current process is free
        if not proc.requesting.heldby.requesting:
            return True
        elif loops == 0:
            return False
        else:
            return self.lock_check(proc.requesting.heldby, loops-1)




    def read_file(self, string):
        resourcefile = open(string, "r")
        print("--File opened:--")
        list = resourcefile.readlines()
        list2 = []

        for line in list:
            print(line, end='')
            list2.append(line.split())
        print("--File closed--")
        resourcefile.close()
        return list2

