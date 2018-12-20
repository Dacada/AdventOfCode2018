import util

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
    def __init__(self):
        self.neighbors = {}

    def add_neighbor(self, direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            other = Room()
            self.neighbors[direction] = other
            other.neighbors[invert(direction)] = self
            return other

def unique(l):
    newl = []
    for e in l:
        if e not in newl:
            newl.append(e)
    l.clear()
    l.extend(newl)

def up(c):
    return (c[0],c[1]-1)
def down(c):
    return (c[0],c[1]+1)
def left(c):
    return (c[0]-1,c[1])
def right(c):
    return (c[0]+1,c[1])

def print_map(origin):
    l = [['.']*100 for __ in range(100)]

    for y in range(100):
        for x in range(100):
            if x % 2 != 0 or y % 2 != 0:
                l[y][x] = '#'

    nodes = [(origin,(50,50))]
    seen = []
    while nodes:
        node,coord = nodes.pop()
        
        if node in seen:
            continue
        seen.append(node)
        
        if 'W' in node.neighbors:
            wallcoord = right(coord)
            l[wallcoord[1]][wallcoord[0]] = '|'
            nodes.append((node,right(wallcoord)))
        if 'E' in node.neighbors:
            wallcoord = left(coord)
            l[wallcoord[1]][wallcoord[0]] = '|'
            nodes.append((node,left(wallcoord)))
        if 'N' in node.neighbors:
            wallcoord = up(coord)
            l[wallcoord[1]][wallcoord[0]] = '-'
            nodes.append((node,up(wallcoord)))
        if 'S' in node.neighbors:
            wallcoord = down(coord)
            l[wallcoord[1]][wallcoord[0]] = '-'
            nodes.append((node,down(wallcoord)))
            
    l[50][50] = 'X'

    for row in l:
        print(''.join(row))
        
@util.timing_wrapper
def star1():
    text = util.get_input_text(DAY)
    text = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"
    text = "^ENWWW(NEEE|SSE(EE|N))$"
    text = "^WNE$"
    
    origin = Room()
    stack = []
    rooms = [origin] # all the "leaf" rooms we're following
    
    for c in text:
        if c in 'NEWS':
            for i in range(len(rooms)):
                rooms[i] = rooms[i].add_neighbor(c)
            unique(rooms) # discard duplicates
        elif c == '(':
            stack.append((room,[])) # room from which we split and list of all the leaf rooms resulting
        elif c == '|':
            stack[-1][1].append(room) # leaf room created
            room = stack[-1][0] # back to the room to split from
        elif c == ')':
            stack[-1][1].append(room) # last leaf
            rooms.extend(stack[-1][1]) # add all leafs
            unique(rooms) # discard duplicates

    print(origin.neighbors['W'].neighbors)
    #print_map(origin)

@util.timing_wrapper
def star2():
    pass

if __name__ == '__main__':
    util.pretty_print(star1, star2)
