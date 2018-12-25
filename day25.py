import util
from day23 import manhattan

import networkx as nx

DAY = 25

def parse(lines):
    return [tuple(map(int,l.split(','))) for l in lines]

@util.timing_wrapper
def star1():
    lines = util.get_input_lines(DAY)
#     lines = """
# 1,-1,-1,-2
# -2,-2,0,1
# 0,2,1,3
# -2,3,-2,1
# 0,2,3,-2
# -1,-1,1,-2
# 0,-2,-1,0
# -2,2,3,-1
# 1,2,2,0
# -1,-2,0,-2
#     """.strip().splitlines()

    g = nx.Graph()
    coords = parse(lines)
    for c1 in coords:
        for c2 in coords:
            if manhattan(c1,c2) <= 3:
                g.add_edge(c1,c2)
    return nx.number_connected_components(g)

@util.timing_wrapper
def star2():
    return "Merry Christmas"

if __name__ == '__main__':
    util.pretty_print(star1, star2)
