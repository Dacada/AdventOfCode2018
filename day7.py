import util
import itertools

DAY = 7

class DependNode:
    created = {}
    
    def __new__(cls, name):
        if name in cls.created:
            return cls.created[name]
        else:
            r = super().__new__(cls)
            cls.created[name] = r
            r.name = name
            r.needs = []
            r.is_needed_by = []
            r.time_left = 60 + ord(name) - ord('A') + 1
            return r

    def depends_on(self, node):
        self.needs.append(node)
        node.is_needed_by.append(self)

    @classmethod
    def ready_nodes(cls):
        for node in [v for v in cls.created.values()]:
            if not node.needs:
                del cls.created[node.name]
                yield node

    def completed(self):
        for node in self.is_needed_by:
            node.needs.remove(self)
        self.is_needed_by = []

def parse_line(line):
    l = line.split()
    return l[1],l[7]

def populate_dependencies(input):
    for line in input:
        dependency,dependant = parse_line(line)
        dependency_node = DependNode(dependency)
        dependant_node = DependNode(dependant)
        dependant_node.depends_on(dependency_node)

@util.timing_wrapper
def star1():
    populate_dependencies(util.get_input_lines(DAY))
    
    result = []
    nodes = DependNode.ready_nodes()
    while nodes:
        nodes = list(set(nodes))
        nodes.sort(key=lambda n: n.name, reverse=True)
        n = nodes.pop()
        result.append(n.name)
        n.completed()
        nodes.extend(DependNode.ready_nodes())

    return ''.join(result)

@util.timing_wrapper
def star2():
    populate_dependencies(util.get_input_lines(DAY))
    seconds = 0

    workers = [None]*5
    #finished = []
    
    nodes = list(sorted(DependNode.ready_nodes(), key=lambda n: n.name, reverse=True))
    #print("Second  Worker1  Worker2  Worker3  Worker4  Worker5  Done")
    while nodes or any(workers):
        add_nodes = False
        
        for i in range(5):
            if workers[i] is not None:
                workers[i].time_left -= 1
                if workers[i].time_left == 0:
                    workers[i].completed()
                    #finished.append(workers[i].name)
                    workers[i] = None
                    add_nodes = True

        if add_nodes:
            nodes.extend(DependNode.ready_nodes())
            nodes = list(set(nodes))
            nodes.sort(key=lambda n: n.name, reverse=True)

        for i in range(5):
            if workers[i] is None and nodes:
                workers[i] = nodes.pop()
            
        #print("{0:6}  {1}  {2}  {3}  {4}  {5}  {6}".format(
        #    seconds,
        #    *('.'.rjust(7) if n is None else n.name.rjust(7) for n in workers),
        #    ','.join(finished)))
        
        seconds += 1

    return seconds - 1

if __name__ == '__main__':
    util.pretty_print(star1, star2)
