class Resource:
    def __init__(self, rid):
        self.held = False
        self.name = "R" + str(rid)

    def check_held(self):
        return self.held

    def hold_taken(self):
        self.held = True

    def hold_released(self):
        self.held = False


class Process:
    def __init__(self, pid):
        self.name = "P" + str(pid)
        self.holding = []

    def take_resource(self, res):
        if not res.check_held():
            res.hold_taken()
            self.holding.append(res)
            print(self.name + " has taken hold of resource " + res.name)
        else:
            print(self.name + " can't hold " + res.name + ", it is already being used by another process")

    def release_resource(self, res):
        if res in self.holding:
            res.hold_released()
            self.holding.remove(res)
            print(self.name + " has released resource " + res.name)
        else:
            print(self.name + " is not holding " + res.name)

    def print_resources(self):
        for r in self.holding:
            print(self.name + " is holding resource " + r.name)


class Resource_Manager:
    def __init__(self):
        r1 = Resource(1)
        p1 = Process(1)
        p1.take_resource(r1)
        p1.print_resources()
        p1.take_resource(r1)
        p1.release_resource(r1)
        p1.take_resource(r1)
        p1.print_resources()


rm = Resource_Manager()