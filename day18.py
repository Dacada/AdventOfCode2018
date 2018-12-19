import util

DAY = 18

def print_map(map):
    for row in map:
        print(''.join(row))
    input()

def resource_value(map):
    return sum(row.count('|') for row in map) * sum(row.count('#') for row in map)

def surrounding(x,y,map):
    l = []
    for i in (-1,0,1):
        for j in (-1,0,1):
            if i != 0 or j != 0:
                if y+j >= 0 and y+j < len(map):
                    if x+i >= 0 and x+i < len(map[y+j]):
                        l.append(map[y+j][x+i])
                        
    return l

def simulate(map):
    newmap = [row[::] for row in map]
    for y,row in enumerate(map):
        for x,yard in enumerate(row):
            neighborhood = surrounding(x,y,map)
            if yard == '.':
                if neighborhood.count('|') >= 3:
                    newmap[y][x] = '|'
            elif yard == '|':
                if neighborhood.count('#') >= 3:
                    newmap[y][x] = '#'
            elif yard == '#':
                if '#' not in neighborhood or '|' not in neighborhood:
                    newmap[y][x] = '.'
    return newmap

@util.timing_wrapper
def star1():
    lines = util.get_input_lines(DAY)
#    lines = """.#.#...|#.
#.....#|##|
#.|..|...#.
#..|#.....#
##.#|||#|#|
#...#.||...
#.|....|...
#||...#|.#|
#|.||||..|.
#...#.|..|.""".split('\n')
    
    map = [[acre for acre in line] for line in lines]    
    for minute in range(10):
        #print_map(map)
        map = simulate(map)
    #print_map(map)
    return resource_value(map)

@util.timing_wrapper
def star2():
    maps = {}
    seen_maps = []
    
    iterations = 1000000000
    
    lines = util.get_input_lines(DAY)
    map = [[acre for acre in line] for line in lines]    
    for minute in range(iterations):
        hashable_map = tuple(tuple(row) for row in map)
        if hashable_map in maps:
            break
        else:
            rval = resource_value(map)
            seen_maps.append(hashable_map)
            maps[hashable_map] = rval
        #print(minute,rval)
        
        map = simulate(map)

    i = seen_maps.index(hashable_map) # index of the first repeated map
    
    # from 0 to i-: Unique maps, if any
    # from i to len(seen_maps)-1: cyclic maps

    iterations -= i
    map = seen_maps[i:][iterations%(len(seen_maps)-i)]

    return maps[map]

if __name__ == '__main__':
    util.pretty_print(star1, star2)
