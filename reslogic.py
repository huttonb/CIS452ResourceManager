# Reslogic is the file that contains all of the internal logic of the resource manager. It contains three classes,
# Resource, which simulates a resource in the manager. Process, which simulates a process. And Resource_manager, which
# Controls the actual logic, executes commands, and finds deadlocks.

# The resource file is meant to represent a Resource, and holds the value of who is holding it, and who wants it.
class Resource:
    def __init__(self, rid):
        self.held = False
        self.heldby = False
        print("Resource " + str(rid) + " initialized")
        self.name = "r" + str(rid)
        self.process_queue = []

    # Waiting_processes is a list of processes that are currently waiting to get the resource.
    def waiting_processes(self, proc):
        self.process_queue.append(proc)

    # Check_held checks to see if the resource is currently being used by a process.
    def check_held(self):
        return self.held

    # Hold_taken updates who the resource is held by, and states that it is currently being held.
    def hold_taken(self, proc):
        self.heldby = proc
        self.held = True

    # Hold_released is activated when the resource is released by a process.
    def hold_released(self):
        self.held = False

    # Check_proc_queue checks the current queue of processes waiting to get the resource, if it has an entry
    # then that process gets the resource.
    def check_proc_queue(self):
        if (len(self.process_queue) > 0):
            return self.process_queue.pop(0).take_resource(self)



# Process is meant to simulate a process, and has several functions. It can list who it's waiting for,
# Request a resource, take a resource, release a resource, and print out the resources that it's holding.
class Process:
    def __init__(self, pid):
        self.name = "p" + str(pid)
        print("Process " + str(pid) + " initialized")
        self.requesting = False
        self.resource_queue = []
        self.holding = []

    # wanted_resource tells the resource that the process wants it.
    def wanted_resources(self, res):
        self.resource_queue.append(res)

    # Take_resource checks to see if the process can take resource, if it can, it does.
    # There are two reasons for why the resource can't be taken:
    # 1. The process is currently requesting another resource
    # 2. The resource is already being used by a different process.
    # The process returns false if the process is unable to get the resource.
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

    # release_resource releases the resource that the process is currently holding. If it's at a hold and wait, it's
    # unable to release the resource by itself.
    def release_resource(self, res):
        if self.requesting == False:
            if res in self.holding:
                res.hold_released()
                self.holding.remove(res)
                print(self.name + " has released resource " + res.name)
                return res.check_proc_queue()
            else:
                print(self.name + " is not holding " + res.name)

    # print_resources prints the resources that the process is holding.
    def print_resources(self):
        for r in self.holding:
            print(self.name + " is holding resource " + r.name)

# Resource_Manager simulates and controls the resources. It reads and commits actions on the processes and resources,
# As well as check for deadlocks.
class Resource_Manager:
    def __init__(self, obs):
        self.observer = obs
        self.processes = {}
        self.resources = {}
        self.load_file()

    # load_file loads the file that the user specifies, and then adds the processes to a dictionary where the key
    # is the name of the process/resource.
    def load_file(self):
        file = input("Enter filename:")
        self.list = self.read_file(file)
        numProcesses = self.list[0]
        numResources = self.list[1]
        for i in range (0, int(numProcesses[0])):
            p1 = Process(i)
            self.processes[("p" + str(i))] = p1
        for i in range(0, int(numResources[0])):
            r1 = Resource(i)
            self.resources[("r" + str(i))] = r1

    # commit_actions takes the action list from the file, sorts them, and commits the actions. It also checks
    # for deadlocks, and alerts the user if there is a deadlock.
    def commit_actions(self):
        for action in self.list:
            # If the action has three fields (such as p1 requests r0), then it is an action.
            if len(action) == 3:
                process_name = action[0]
                resource_name = action[2]
                # If the action is requests, then the program checks to see if the resource is already taken.
                if action[1] == "requests":
                    # The program checks to see if the process was able to get the resource. If it wasn't,
                    # then the process is added to the resources waiting list, and the resource is added to
                    # the processes want list, and the process is on wait and hold, and the graph is updated.
                    # If the process does acquire the resource, the graph is updated with that new connection.
                    if not self.processes.get(process_name).take_resource(self.resources.get(resource_name)):
                        self.processes.get(process_name).wanted_resources(self.resources.get(resource_name))
                        self.resources.get(resource_name).waiting_processes(self.processes.get(process_name))
                        self.update(process_name, resource_name, "requests")
                    else:
                        self.update(process_name, resource_name, "connects")
                # After a process has released a resource, check to see if next acquisition is successful
                # for the graph. Either way update the graph by removing released edge.
                elif action[1] == "releases":
                    # If the resource is immediately grabbed by another process after release, then update the graph.
                    if (self.processes.get(process_name).release_resource(self.resources.get(resource_name))):
                        # When releasing this one we send the resource and process in opposite order.
                        self.update(self.resources.get(resource_name).heldby.name, resource_name, "reqrelease")
                        self.update(self.resources.get(resource_name).heldby.name, resource_name, "connects")
                    self.update(process_name, resource_name, "releases")
                # Check to see if there are more than two processes waiting, if there is
                # check for a deadlock.
                waiting_proc = 0
                for i in self.processes.values():
                    if i.requesting != False:
                        waiting_proc += 1
                    if waiting_proc >= 2:
                        self.deadlock_check()
                        break;


    # Update sends an update to the controller, contains the resource, process, and type of connection
    def update(self, process, resource, connection):
        self.observer.update(process,resource,connection)

    # deadlock_check goes through each process, if it's holding it starts a deadlock check by calling to lock_check.
    def deadlock_check(self):
        for i in self.processes.values():
            if i.requesting:
                lockedProcesses = [i.name]
                if not self.lock_check(i, len(self.processes.values()), lockedProcesses):
                    print ("Deadlock detected for: " )
                    print(*lockedProcesses)
                    break;

    # lock_check recursively checks for a deadlock
    # It goes down by going to the process the current processes requested resource is being held by
    # If that process is free, it's not a deadlock and returns false, if it's in hold as well it continues
    # the recursion, once loops hits 0, it comes back as a deadlock, as that means it is impossible for the cycle
    # to be anything but a deadlock.
    # True: No deadlock
    # False: Deadlock
    # lockedprocs keeps track of which processes are deadlocked.
    def lock_check(self, proc, loops, lockedprocs):
        #if requested resources current process is free
        if not proc.requesting.heldby.requesting:
            return True
        elif loops == 0:
            return False
        else:
            if proc.name not in lockedprocs:
                lockedprocs.append(proc.name)
            return self.lock_check(proc.requesting.heldby, loops-1, lockedprocs)




    # read_file reads the file and returns the actions as a list of lists.
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

