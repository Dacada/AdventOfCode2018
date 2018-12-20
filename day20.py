import util
import networkx as nx

DAY = 20

def invert(direction):
    if direction == 'N':
        return 'S'
    elif direction == 'E':
        return 'W'
    elif direction == 'W':
        return 'E'
    elif direction == 'S':
        return 'N'

class Room:
    def __init__(self, graph):
        self.graph = graph
        self.neighbors = {}
        graph.add_node(self)

    def add_neighbor(self, direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            other = Room(self.graph)
            self.neighbors[direction] = other
            other.neighbors[invert(direction)] = self
            self.graph.add_edge(self, other)
            return other

    def eccentricity(self):
        return nx.eccentricity(self.graph, self)

    def shortest_paths_length(self, doors):
        return sum(x >= 1000 for x in nx.shortest_path_length(self.graph, source=self).values())

def up(c):
    return (c[0],c[1]-1)
def down(c):
    return (c[0],c[1]+1)
def left(c):
    return (c[0]-1,c[1])
def right(c):
    return (c[0]+1,c[1])

def print_map(origin):
    maxx = 10
    maxy = 10

    def tophys(c):
        return (c[0]*2+1,c[1]*2+1)

    maxxphys,maxyphys = tophys((maxx,maxy))
    
    l = [['.']*maxxphys for __ in range(maxyphys)]

    for y in range(maxyphys):
        for x in range(maxxphys):
            if x % 2 == 0 or y % 2 == 0:
                l[y][x] = '#'

    origincoords = (maxx//2,maxy//2)

    nodes = [(origin,origincoords)]
    seen = []
    while nodes:
        node,coord = nodes.pop()
        
        if node in seen:
            continue
        seen.append(node)

        m = {
            'W': left,
            'E': right,
            'N': up,
            'S': down
        }

        for d in m:
            if d in node.neighbors:
                wallcoord = m[d](tophys(coord))
                l[wallcoord[1]][wallcoord[0]] = '|' if d in 'WE' else '-'
                nodes.append((node.neighbors[d],m[d](coord)))

    x,y = tophys(origincoords)
    l[y][x] = 'X'

    for row in l:
        print(''.join(row))


def make_graph(text):
    """
    origin = Room()
    stack = []
    rooms = [origin] # all the "leaf" rooms we're following

    for c in text:
        if c in 'NEWS':
            for i in range(len(rooms)):
                rooms[i] = rooms[i].add_neighbor(c)
            rooms = unique(rooms) # discard duplicates
        elif c == '(':
            stack.append((unique(rooms),[])) # rooms from which we split and list of all the leaf rooms resulting
        elif c == '|':
            stack[-1][1].extend(rooms) # leaf rooms created
            stack[-1] = (stack[-1][0],unique(stack[-1][1]))
            rooms = unique(stack[-1][0]) # back to the rooms we split from
        elif c == ')':
            stack[-1][1].extend(rooms) # last leaf group
            rooms.extend(stack[-1][1]) # add all leafs to our rooms
            rooms = unique(rooms)
    """
    
    #And then I checked Reddit. Oh joy, all groups end up in the same spot. I could've used the simple stack all this time.
    #If you're reading this, Advent of Code guy, learn to write problem descriptions.

    origin = Room(nx.Graph())
    stack = []
    room = origin

    for c in text:
        if c in 'NEWS':
            room = room.add_neighbor(c)
        elif c == '(':
            stack.append(room)
        elif c == '|':
            room = stack[-1]
        elif c == ')':
            stack.pop()

    return origin
        
@util.timing_wrapper
def star1():
    text = util.get_input_text(DAY)
    #text = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$" #31
    #text = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$" #23
    #text = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$" #18
    #text = "^ENWWW(NEEE|SSE(EE|N))$" #10
    #text = "^WNE$" #3

    origin = make_graph(text)

    #print_map(origin)
    return origin.eccentricity()

@util.timing_wrapper
def star2():
    return make_graph(util.get_input_text(DAY)).shortest_paths_length(1000)

if __name__ == '__main__':
    util.pretty_print(star1, star2)
