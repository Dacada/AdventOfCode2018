import util

DAY = 6

def parse_coord(c):
    return (int(x) for x in c.split(','))

def manhattan(p, q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])

#gridx = gridy = 10
gridx = gridy = 400
    
@util.timing_wrapper
def star1():
    grid = [[None for ___ in range(gridx)] for __ in range(gridy)]
    for coord_i,coord_str in enumerate(util.get_input_lines(DAY)):
    #for coord_i,coord_str in enumerate(['1, 1', '1, 6', '8, 3', '3, 4', '5, 5', '8, 9']):
        x,y = parse_coord(coord_str)
        for j in range(gridy):
            for i in range(gridx):
                if grid[j][i] is None:
                    grid[j][i] = [coord_i], manhattan((x,y),(i,j))
                else:
                    dist = manhattan((x,y),(i,j))
                    curr_dist = grid[j][i][1]
                    if dist == curr_dist:
                        grid[j][i][0].append(coord_i)
                    elif dist < curr_dist:
                        grid[j][i] = [coord_i], dist

    to_ignore = set(row[0][0] for row in grid[0])\
         .union(set(row[0][0] for row in grid[-1]))\
         .union(set(grid[i][0][0][0] for i in range(gridy)))\
         .union(set(grid[i][-1][0][0] for i in range(gridy)))

    counts = [0]*(coord_i+1)
    for j in range(gridy):
        for i in range(gridx):
            l = grid[j][i][0]
            if len(l) == 1:
                k = l[0]
                counts[k] += 1

    return max(c for i,c in enumerate(counts) if i not in to_ignore)

@util.timing_wrapper
def star2():
    #limit = 32
    limit = 10000
    grid = [[0 for ___ in range(gridx)] for __ in range(gridy)]
    for coord_i,coord_str in enumerate(util.get_input_lines(DAY)):
    #for coord_i,coord_str in enumerate(['1, 1', '1, 6', '8, 3', '3, 4', '5, 5', '8, 9']):
        x,y = parse_coord(coord_str)
        for j in range(gridy):
            for i in range(gridx):
                grid[j][i] += manhattan((x,y),(i,j))

    largest = 0
    for j in range(gridy):
        for i in range(gridx):
            a = grid[j][i]
            if a is not None and a < limit:
                current = 1
                grid[j][i] = None
                stack = [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]
                while stack:
                    x,y = stack.pop()
                    if x >= 0 and x < gridx and y >= 0 and y < gridy:
                        a = grid[x][y]
                        grid[x][y] = None
                        if a is not None and a < limit:
                            current += 1
                            stack.extend([(x+1,y), (x-1,y), (x,y+1), (x,y-1)])
                if current > largest:
                    largest = current

    return largest
                            
if __name__ == '__main__':
    util.pretty_print(star1, star2)
