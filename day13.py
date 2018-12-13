import util

DAY = 13

def insert_cart(carts, x, y, direction, memory):
    if x in carts:
        carts[x].append((x,y,direction,memory))
    else:
        carts[x] = [(x,y,direction,memory)]

def advance(x,y,direction):
    if direction == '>':
        x += 1
    elif direction == '<':
        x -= 1
    elif direction == 'v':
        y += 1
    elif direction == '^':
        y -= 1
    else:
        raise Exception()

    return x,y

def init_from_map(map):
    carts = {}
    cartcoords = set()
    for j,row in enumerate(map):
        for i,c in enumerate(row):
            if c == '^' or c == 'v':
                map[j][i] = '|'
                insert_cart(carts, i, j, c, 'left')
                cartcoords.add((i,j))
            elif c == '<' or c == '>':
                map[j][i] = '-'
                insert_cart(carts, i, j, c, 'left')
                cartcoords.add((i,j))
    return carts,cartcoords

def tick(map, carts, cartcoords, return_on_collision):
    newcarts = {}
    collision = None
    for y in sorted(carts.keys()):
        row = carts[y]
        for cart in sorted(row, key=lambda n: n[1]):
            x,y,direction,memory = cart

            if collision is not None:
                if collision == (x,y):
                    continue
            
            cartcoords.remove((x,y))
            track = map[y][x]
            if track == '-' or track == '|':
                pass
            elif track == '/':
                if direction == '^':
                    direction = '>'
                elif direction == '>':
                    direction = '^'
                elif direction == 'v':
                    direction = '<'
                elif direction == '<':
                    direction = 'v'
            elif track == '\\':
                if direction == '^':
                    direction = '<'
                elif direction == '>':
                    direction = 'v'
                elif direction == 'v':
                    direction = '>'
                elif direction == '<':
                    direction = '^'
            elif track == '+':
                if memory == 'left':
                    memory = 'straight'
                    if direction == '^':
                        direction = '<'
                    elif direction == '>':
                        direction = '^'
                    elif direction == 'v':
                        direction = '>'
                    elif direction == '<':
                            direction = 'v'
                elif memory == 'straight':
                    memory = 'right'
                elif memory == 'right':
                    memory = 'left'
                    if direction == '^':
                        direction = '>'
                    elif direction == '>':
                        direction = 'v'
                    elif direction == 'v':
                        direction = '<'
                    elif direction == '<':
                        direction = '^'
            else:
                raise Exception(str((track,cart)))

            x,y = advance(x,y,direction)
            if x < 0 or y < 0:
                raise Exception(str((track,cart)))
            if ((x,y)) in cartcoords:
                collision = (x,y)
                if return_on_collision:
                    return collision,None
                else:
                    if x in newcarts: # it has already moved this tick
                        found = False
                        l = []
                        for cart in newcarts[x]:
                            if cart[1] == y:
                                found = True
                            else:
                                l.append(cart)
                        if not found:
                            raise Exception()
                        newcarts[x] = l
                    else: # it has not moved this tick, it'll be removed when next processed by checking collision
                        found = False
                        for cart in carts[x]:
                            if cart[1] == y:
                                found = True
                        if not found:
                            raise Exception()
                    cartcoords.remove((x,y))
            else:
                cartcoords.add((x,y))
                insert_cart(newcarts, x, y, direction, memory)
                
    return collision,newcarts

def print_map(map, cartcoords):
    for y in range(len(map)):
        row = map[y]
        for x in range(len(row)):
            track = row[x]
            if (x,y) in cartcoords:
                print('X',end='')
            else:
                print(track,end='')
        print()
        
@util.timing_wrapper
def star1():
    map = [list(row) for row in util.get_input_text_notrim(DAY).split('\n')]
    carts,cartcoords = init_from_map(map)

    collision = None
    while collision is None:
        collision,carts = tick(map,carts,cartcoords,True)

    return ','.join(str(n) for n in collision)
            
@util.timing_wrapper
def star2():
    map = [list(row) for row in util.get_input_text_notrim(DAY).split('\n')]
    carts,cartcoords = init_from_map(map)

    while len(cartcoords) > 1:
        #print_map(map, cartcoords)
        #input()
        collision,carts = tick(map,carts,cartcoords,False)

    return ','.join(str(n) for n in cartcoords.pop())

if __name__ == '__main__':
    util.pretty_print(star1, star2)
