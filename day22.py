import heapq
import collections
import enum

import util
from day6 import manhattan

DAY = 22

class CaveSystem:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.mouth = (0,0)
        self.erosion_levels = {}
        self.types = {}
        
    def __str__(self):
        s = ''
        for y in range(self.target[1]+1):
            for x in range(self.target[0]+1):
                if (x,y) == self.mouth:
                    s += 'M'
                elif (x,y) == self.target:
                    s += 'T'
                else:
                    t = self.get_type(x,y)
                    if t == 0:
                        s += '.'
                    elif t == 1:
                        s += '='
                    elif t == 2:
                        s += '|'
            s += '\n'
        return s

    def get_risk_level(self):
        return sum(self.get_type(x,y) for y in range(self.target[1]+1) for x in range(self.target[0]+1))

    def get_type(self, x, y):
        c = (x,y)
        if c in self.types:
            return self.types[c]
        else:
            t = self.get_erosion_level(x, y) % 3
            self.types[c] = t
            return t

    def get_erosion_level(self, x, y):
        if (x,y) in self.erosion_levels:
            return self.erosion_levels[(x,y)]
        else:
            erosion_level = (self.get_geologic_index(x, y) + self.depth) % 20183
            self.erosion_levels[(x,y)] = erosion_level
            return erosion_level

    def get_geologic_index(self, x, y):
        if (x,y) == (0,0):
            return 0
        elif (x,y) == self.target:
            return 0
        elif y == 0:
            return x * 16807
        elif x == 0:
            return y * 48271
        else:
            return self.get_erosion_level(x-1, y) * self.get_erosion_level(x, y-1)

def parse_input(text):
    l1,l2 = text.split('\n')
    __,depth_str = l1.split()
    __,target_str = l2.split()
    return int(depth_str),tuple(int(x) for x in target_str.split(','))

def adjacent(coord):
    return ((coord[0]-1,coord[1]),
            (coord[0]+1,coord[1]),
            (coord[0],coord[1]-1),
            (coord[0],coord[1]+1))

def print_path(cave, history, position):
    xpos,ypos = position
    maxx = max(x for x,y,t in history)
    maxy = max(y for x,y,t in history)
    if xpos > maxx:
        maxx = xpos
    if ypos > maxy:
        maxy = ypos
    histdict = {(x,y):t for x,y,t in history}

    s = ''
    for y in range(maxy+5):
        for x in range(maxx+5):
            if (x,y) == cave.mouth:
                s += 'M'
            elif (x,y) == cave.target:
                s += 'T'
            elif x == xpos and y == ypos:
                s += '#'
            elif (x,y) in histdict:
                t = histdict[(x,y)]
                if t == Tool.NEITHER:
                    s += '%'
                elif t == Tool.TORCH:
                    s += '#'
                elif t == Tool.GEAR:
                    s += '@'
            else:
                t = cave.get_type(x,y)
                if t == 0:
                    s += '.'
                elif t == 1:
                    s += '='
                elif t == 2:
                    s += '|'
        s += '\n'
    print(s)
    

Agent = collections.namedtuple('Agent', ['distance_with_heuristic', 'minutes', 'agent_count', 'x', 'y', 'tools', 'history'])

class Tool(enum.Enum):
    NEITHER = enum.auto()
    TORCH = enum.auto()
    GEAR = enum.auto()

@util.timing_wrapper
def star1():
    depth,target = parse_input(util.get_input_text(DAY))
    #depth = 510
    #target = (10,10)
    cave = CaveSystem(depth, target)
    #print(cave)
    return cave.get_risk_level()

@util.timing_wrapper
def star2():
    depth,target = parse_input(util.get_input_text(DAY))
    #depth = 510
    #target = (10,10)
    targetx,targety = target
    
    cave = CaveSystem(depth, target)

    # A* Algorithm
    
    best = {}
    priority_queue = [
        Agent (
            distance_with_heuristic = manhattan((0,0),target),
            minutes = 0,
            agent_count = 1,
            x = 0,
            y = 0,
            tools = Tool.TORCH
            ,history = ()
        )
    ]
    count = 1
    while priority_queue:
        distance_with_heuristic,minutes,__,xpos,ypos,tools,history = heapq.heappop(priority_queue)
        position = (xpos,ypos)

        state = (xpos,ypos,tools)
        if state in best and best[state] <= minutes:
            continue
        best[state] = minutes

        if xpos == targetx and ypos == targety and tools == Tool.TORCH:
            history += (state,)
            break

        if tools != Tool.NEITHER:
            count += 1
            heapq.heappush(priority_queue, Agent (
                distance_with_heuristic = minutes + 14 + manhattan(position,target),
                minutes = minutes + 7,
                agent_count = count,
                x = xpos,
                y = ypos,
                tools = Tool.NEITHER
                ,history = history + (state,)
            ))
        if tools != Tool.TORCH:
            count += 1
            heapq.heappush(priority_queue, Agent (
                distance_with_heuristic = minutes + 7 + manhattan(position,target),
                minutes = minutes + 7,
                agent_count = count,
                x = xpos,
                y = ypos,
                tools = Tool.TORCH
                ,history = history + (state,)
            ))
        if tools != Tool.GEAR:
            count += 1
            heapq.heappush(priority_queue, Agent (
                distance_with_heuristic = minutes + 14 + manhattan(position,target),
                minutes = minutes + 7,
                agent_count = count,
                x = xpos,
                y = ypos,
                tools = Tool.GEAR
                ,history = history + (state,)
            ))
            
        for x,y in adjacent(position):
            if x >= 0 and y >= 0:
                current_type = cave.get_type(xpos,ypos)
                next_type = cave.get_type(x,y)

                if current_type == 0:
                    if next_type == 1:
                        if tools == Tool.TORCH:
                            continue
                    elif next_type == 2:
                        if tools == Tool.GEAR:
                            continue
                elif current_type == 1:
                    if next_type == 0:
                        if tools == Tool.NEITHER:
                            continue
                    elif next_type == 2:
                        if tools == Tool.GEAR:
                            continue
                elif current_type == 2:
                    if next_type == 0:
                        if tools == Tool.NEITHER:
                            continue
                    elif next_type == 1:
                        if tools == Tool.TORCH:
                            continue

                count += 1
                heapq.heappush(priority_queue, Agent (
                    distance_with_heuristic = minutes + 1 + manhattan(position,target),
                    minutes = minutes + 1,
                    agent_count = count,
                    x = x,
                    y = y,
                    tools = tools
                    ,history = history + (state,)
                ))

    print_path(cave, history, position)
    print(len(priority_queue), len(best))

    return minutes

if __name__ == '__main__':
    util.pretty_print(star1, star2)
